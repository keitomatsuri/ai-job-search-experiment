import openai

initial_prompt_for_propose = """あなたは転職エージェントです。
これまでの会話を踏まえ、検索結果を元にユーザーに対して求人を提案してください。
日本語で分かりやすく説明してください。
"""

prompt_for_search_result = """
# 検索結果
{}
"""


class Proposer:
    def __init__(self, model: str):
        self.model = model

    def _format_result(self, result):
        """
        Format the result from Azure Cognitive Search.
        """
        target_keys = [key for key in result.keys() if key != "id"]
        formatted_result = ""
        for key in target_keys:
            formatted_result += f"{key}: {result.get(key, 'N/A')}\n"

        return formatted_result

    def propose(self, search_results, question: str, history: list):
        # プロンプトを作成
        messages = [{"role": "system", "content": initial_prompt_for_propose}]
        for message in history:
            messages.append(
                {"role": message["role"], "content": message["content"]})
        messages.append({"role": "user", "content": question})

        first_result = next(search_results, None)
        if first_result:
            formatted_result = self._format_result(first_result)
            messages.append(
                {"role": "system", "content": prompt_for_search_result.format(formatted_result)})

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0]["message"]["content"].strip()

        else:
            return "検索結果が見つかりませんでした。"
