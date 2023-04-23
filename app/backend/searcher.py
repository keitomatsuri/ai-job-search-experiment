import os
import re
import json
from dotenv import load_dotenv
import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# azure search
search_service = os.getenv("AZURE_SEARCH_SERVICE_NAME")
api_key = os.getenv("AZURE_SEARCH_SERVICE_API_KEY")
index_name = os.getenv("AZURE_SEARCH_SERVICE_INDEX_NAME")

# prompt
system_prompt_for_search = """質問を元に、Azure Cognitive SearchのPython用クライアントライブラリで使用するためのjson形式のクエリパラメータを生成してください。
質問履歴が存在する場合は、それを考慮して適切なクエリパラメータを生成してください。

このプロンプトに対するあなたの回答は、json形式の文字列のみとします。

# 使用可能なクエリパラメータ
- search_text
- filter

# サンプルデータ
{"id":"000001","company_name":"クリエイティブフュージョン株式会社","job_category":"フロントエンドエンジニア","employment_type":"正社員","location":"神奈川県横浜市西区","number_of_employees":"80","years_in_business":"10","job_description":"ウェブアプリケーションのフロントエンド開発を担当し、UI/UX設計から実装、保守・運用まで一貫して行っていただきます。チームと協力して使いやすく魅力的なプロダクトを開発し、ユーザーエクスペリエンスの向上に貢献してください。また、新技術の研究やチーム内でのナレッジシェアも期待されます。","required_experience_and_skills":"React, TypeScriptを必須とし、HTML5, CSS3, Git, コードレビュー、チームでの開発経験が求められます。","min_annual_salary":"550","max_annual_salary":"1000","business_start_hour":"9","business_end_hour":"18","overtime_working_hours":"20","holiday_and_vacation":"週休二日制（土・日）、祝日、年末年始、有給休暇、慶弔休暇、リフレッシュ休暇","benefits":"各種社会保険完備、交通費支給、定期健康診断、社内イベント、研修制度、資格取得支援制度、育児・介護休暇制度"}

# 出力例
{"search_text":"フロントエンドエンジニア"}
{"filter":"max_annual_salary ge 500"}
{"search_text":"バックエンドエンジニア","filter": "overtime_working_hours lt 20"}
"""

prompt_for_question = """
# 質問履歴
{}

# 質問
{}
"""


class Searcher:
    def __init__(self, model: str):
        self.model = model

    def search(self, question: str, history: list):
        # 質問履歴を取得
        former_questions_arr = []
        for message in history:
            if message["role"] == "user":
                former_questions_arr.append(message["content"])
        former_questions = '/'.join(former_questions_arr)

        # プロンプトを作成
        messages = [{"role": "system", "content": system_prompt_for_search}]
        messages.append({"role": "user", "content": prompt_for_question.format(
            former_questions, question)})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        answer = response.choices[0]["message"]["content"].strip()

        # 文字列内の最初のJSON構造の文字列を抽出
        match = re.search(r'\{.*?\}', answer, re.DOTALL)
        first_json_string = match.group()

        # JSON文字列をパース
        try:
            input_dict = json.loads(first_json_string)
        except json.JSONDecodeError:
            raise Exception("Invalid json format")

        search_text = input_dict.get("search_text", "")
        filter = input_dict.get("filter", "")

        # Azure Search
        credential = AzureKeyCredential(api_key)
        search_client = SearchClient(endpoint=f"https://{search_service}.search.windows.net/",
                                     index_name=index_name,
                                     credential=credential)

        return search_client.search(
            search_text,
            filter=filter,
        )
