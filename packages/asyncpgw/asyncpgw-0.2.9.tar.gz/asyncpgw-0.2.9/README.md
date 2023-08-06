# asyncpgw
これはdiscord.pyとasyncpgを使用し、POSTTGRESQLにデータを保存する処理があるBOTを作ってる日本人向けに作成したものです。


# 使い方

### asyncpgwをインストール
```
python3 -m pip install asyncpg
```

### 基本的な使い方

ソースコードがかなり長くなってしまうので、
[testsフォルダー](https://github.com/furimu1234/asyncpgw/tree/main/tests)
にまとめてあります。

尚、このコードは`COG`を使用しています。

テキストチャットで発言するとユーザーのレベルがあがるコードを例にしてます。


# 変更ログ

0.0.1

・テスト

0.0.2

・descriptionの変更

0.0.3

・カラムが空だった場合に対応

0.0.4

・bug fix

0.0.5

・bug fix

0.0.6

・bug fix

0.0.7

・bug fix

0.0.8

・　ListpgクラスのTypeErrorが出るバグを直した。

0.0.9

・　Listpgクラスの)の位置を直した

0.1.0

・　Listpgクラスのbugを直した

0.1.1

・limit_fetchsのbugを直した

0.1.2

・同じ

0.1.3

・ListPgをPgにまとめた
・sortfetchとlimitfetchを追加

0.1.4

・sort_fetchのバグを直した

0.1.5

・sort_fetchのバグを直した

0.1.6

・sort_fetchのバグを直した

0.1.7 ~ 0.2.5

・カラムが指定されない時に対応した。

0.2.6

・カラムの追加削除関数を追加

0.2.7

・カラム削除関数のバグを直した