# COTOHA-Python
NTTコミュニケーションズさんが提供している[COTOHA API](https://api.ce-cotoha.com/contents/index.html)を少しだけ使いやすくするラッパーです。

## [COTOHA API](https://api.ce-cotoha.com/contents/index.html)とは
NTTコミュニケーションズさんが提供している自然言語処理APIです。構文解析や照応解析などを利用することができます。

## 詳細
for Developersで使うことができるAPIに対応しています。アクセストークンの更新およびリクエストをして、リファレンスに基づいて解析結果を取得します。

## 使い方
1. 任意のディレクトリにこのリポジトリをcloneする。
```git clone https://github.com/hatopoppoK3/COTOHA-Python.git```

2. cotohaディレクトリの中に「json」という名前でフォルダを作成する。
3. jsonディレクトリの中に以下のようなclient.jsonを作成する。
cotohaディレクトリが本体なので、任意のところに配置してください。

```json:client.json
{
    "grantType": "client_credentials",
    "clientId": "取得したclientId",
    "clientSecret": "取得したclientSecret",
    "publish_url": "取得したpublish_url"
}
```

## サンプル(形態素解析)

```python:sample.py
from cotoha.parse import CotohaParse

parse = CotohaParse('犬は歩く。')
print(parse)
```

解析結果はほとんど[リファレンス](https://api.ce-cotoha.com/contents/reference/apireference.html)に基づいているはずです。