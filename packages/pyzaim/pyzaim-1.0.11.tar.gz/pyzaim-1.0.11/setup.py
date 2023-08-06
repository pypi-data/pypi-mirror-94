# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzaim']

package_data = \
{'': ['*'], 'pyzaim': ['.vscode/*']}

install_requires = \
['requests-oauthlib>=1.3.0,<2.0.0',
 'selenium>=3.141.0,<4.0.0',
 'tqdm>=4.43.0,<5.0.0']

setup_kwargs = {
    'name': 'pyzaim',
    'version': '1.0.11',
    'description': 'Zaimのデータを取得・操作するPythonパッケージ',
    'long_description': '# pyzaim\n<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->\n[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)\n<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\n[Zaim](https://zaim.net/)のデータを取得・操作するPythonパッケージ\n\n## 概要\n\n大きくわけて2つの処理を行うパッケージです。\n\n- [Zaim API](https://dev.zaim.net/)のラッパークラス\n  - Zaim APIのアクセストークンの発行\n  - Rest APIとして提供されている処理の実行\n- [Selenium](https://github.com/SeleniumHQ/selenium/tree/master/py)を用いたデータ取得\n  - Zaimにはクレジットカードや銀行口座から自動でデータ取得する機能があるが、APIではそれらのデータにはアクセスできない\n  - これらの情報を取得するため、Seleniumのwebdriver(Chrome)を用いてデータを取得\n\n## インストール\n\n```bash\npip install pyzaim\n```\n\n## 準備\n\n- Zaimアカウントの作成\n- Zaim Developersでのアプリケーションの登録 (コンシューマID、コンシューマシークレットの発行)\n- Google Chromeおよびseleniumの導入\n\n## 使い方\n\n### Zaim APIのラッパークラスの使い方\n\n- アクセストークンの発行\n\n```python\nfrom pyzaim import get_access_token\n\nget_access_token()\n\n# コンシューマIDとコンシューマシークレットを聞かれるので入力\n# 認証ページのURLが表示されるので、アクセスして許可\n# 遷移先ページのソースコードから「oauth_verifier」と書いてあるコードをコピーして入力\n# 問題なければアクセストークンとアクセスシークレットが表示される\n```\n\n- APIを利用してデータを取得・操作\n\n```python\nfrom pyzaim import ZaimAPI\n\napi = ZaimAPI(\'コンシューマID\', \'コンシューマシークレット\',\n              \'アクセストークン\', \'アクセスシークレット\', \'verifier\')\n\n# 動作確認 (ユーザーID等のデータが取得されて、表示されればOK)\nprint(api.verify())\n\n# データの取得\ndata = api.get_data()\n\n# 支払いデータの登録\napi.insert_payment_simple(\'日付(datetime.date型)\', \'金額(int)\', \'ジャンル名\',\n                          \'口座名\', \'コメント\', \'品名\', \'店舗名\') # 後半4つは任意入力\n\n# 使用できるジャンル名は以下で確認できる\nprint(api.genre_itos)\n\n# 使用できる口座名は以下で確認できる\nprint(api.account_itos)\n\n# 支払いデータの更新 (更新対象データのIDはapi.get_data()で確認)\napi.update_payment_simple(\'更新対象データのID\', \'日付(datetime.date型)\', \'金額(int)\',\n                          \'ジャンル名\', \'口座名\', \'コメント\', \'品名\', \'店舗名\') # 後半4つは任意入力\n\n# 支払いデータの削除\napi.delete_payment(\'削除対象のデータのID\')\n```\n\n### seleniumを用いたデータ取得\n\n```python\nfrom pyzaim import ZaimCrawler\n\n# Chrome Driverの起動とZaimへのログイン、ログインには少し時間がかかります\ncrawler = ZaimCrawler(\'ログインID\', \'ログインパスワード\',\n                    driver_path=\'Chrome Driverのパス\'(PATHが通っていれば省略可),\n                    headless=False) # headlessをTrueにするとヘッドレスブラウザで実行できる\n\n# データの取得 (データの取得には少し時間がかかります、時間はデータ件数による)\ndata = crawler.get_data(\'取得する年(int)\', \'取得する月(int)\', progress=True) # progressをFalseにするとプログレスバーを非表示にできる\n\n# 終了処理\ncrawler.close()\n```\n\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://fe-notes.work/"><img src="https://avatars.githubusercontent.com/u/38152917?v=4?s=100" width="100px;" alt=""/><br /><sub><b>reeve0930</b></sub></a><br /><a href="#projectManagement-reeve0930" title="Project Management">📆</a> <a href="https://github.com/reeve0930/pyzaim/pulls?q=is%3Apr+reviewed-by%3Areeve0930" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/reeve0930/pyzaim/commits?author=reeve0930" title="Code">💻</a> <a href="https://github.com/reeve0930/pyzaim/commits?author=reeve0930" title="Documentation">📖</a></td>\n    <td align="center"><a href="https://github.com/Ponk02"><img src="https://avatars.githubusercontent.com/u/24751394?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ponk02</b></sub></a><br /><a href="https://github.com/reeve0930/pyzaim/commits?author=Ponk02" title="Code">💻</a></td>\n    <td align="center"><a href="http://zenjiro.wordpress.com/"><img src="https://avatars.githubusercontent.com/u/1298249?v=4?s=100" width="100px;" alt=""/><br /><sub><b>zenjiro</b></sub></a><br /><a href="https://github.com/reeve0930/pyzaim/commits?author=zenjiro" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/omatsu555"><img src="https://avatars.githubusercontent.com/u/40729996?v=4?s=100" width="100px;" alt=""/><br /><sub><b>omatsu555</b></sub></a><br /><a href="https://github.com/reeve0930/pyzaim/commits?author=omatsu555" title="Code">💻</a></td>\n    <td align="center"><a href="https://github.com/kagemomiji"><img src="https://avatars.githubusercontent.com/u/5343692?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Y.Tory</b></sub></a><br /><a href="https://github.com/reeve0930/pyzaim/commits?author=kagemomiji" title="Code">💻</a></td>\n    <td align="center"><a href="https://knoow.jp/@/Omatsu?preview"><img src="https://avatars.githubusercontent.com/u/7794917?v=4?s=100" width="100px;" alt=""/><br /><sub><b>o-matsu</b></sub></a><br /><a href="https://github.com/reeve0930/pyzaim/commits?author=o-matsu" title="Code">💻</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'reeve0930',
    'author_email': 'reeve0930@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reeve0930/pyzaim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
