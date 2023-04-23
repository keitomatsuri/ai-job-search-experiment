# 概要
ChatGPT APIとAzure Cognitive Searchを使用した求人検索システムの試作版です。

# 環境構築
## ChatGPT API
API Keyを取得する。

## Azure Cognitive Search
検索サービスを作成する。
参考：[チュートリアル:Azure Storage に格納されている JSON BLOB のインデックスを REST で作成する](https://learn.microsoft.com/ja-jp/azure/search/search-semi-structured-data)

## frontend
npm install
npm run dev

## backend
pip install -r requirements.txt
.env作成
python main.py