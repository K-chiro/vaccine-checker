from flask import Flask

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 他のモジュール（ルートやビュー関数など）をインポート
from app import routes  # 例えば、routes.pyファイルがある場合のインポート

