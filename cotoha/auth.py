import datetime
import json
import os
from json import JSONDecodeError

import requests


class Auth(object):
    """認証に関するクラス.
    access_tokenの更新や有効時間の確認を行う.

    """

    def __init__(self):
        self.base_url = 'https://api.ce-cotoha.com/api/dev/'
        self.limit_time = 0
        self.token = ''
        if os.path.exists('./json/access.json'):
            with open('./json/access.json', 'r', encoding='utf-8') as rf:
                try:
                    access_json = json.load(rf)
                    self.token = access_json['access_token']
                    self.limit_time = access_json['limit_time']
                    # 有効期限が切れている場合
                    if not(self.check_token()):
                        self.update_token()
                # access.jsonにエラーがある場合
                except (JSONDecodeError, KeyError):
                    self.update_token()
        # access.jsonが存在しない場合
        else:
            self.update_token()

    def __str__(self) -> str:
        """クラスの概要を文字列で返す.

        Returns:
            str: クラス概要.
        """
        string = 'base_url:{}\n'.format(self.base_url)
        string += 'limit_time:{}\n'.format(self.limit_time)
        string += 'token:{}\n'.format(self.token)
        return string

    def check_token(self) -> bool:
        """
        アクセストークンの有効期限を確認する.

        Returns:
            bool: 有効期限内ならばTrue,そうでなければFalse.
        """
        now_datetime = datetime.datetime.now()
        now_time = now_datetime.timestamp()
        if now_time < self.limit_time:
            return True
        else:
            return False

    def update_token(self) -> None:
        """アクセストークンの更新を行う.

        Raises:
            AuthError: 通信エラーがある場合.オフラインの場合など.
            AuthError: client.jsonに問題がある場合.keyが間違っている場合など.
            AuthError: client.jsonが存在しない場合.
        """
        if os.path.exists('./json/client.json'):
            with open('./json/client.json', 'r', encoding='utf-8') as rf:
                try:
                    requests_json = json.load(rf)
                    publish_url = requests_json.pop('publish_url')
                    requests_headers = {'Content-Type': 'application/json'}
                    r = requests.post(url=publish_url, json=requests_json,
                                      headers=requests_headers)
                    if r.status_code == 201:
                        response_json = r.json()
                        expires_in = int(response_json['expires_in'])
                        issued_at = int(response_json['issued_at'][:-3])
                        self.token = 'Bearer '+response_json['access_token']
                        self.limit_time = expires_in+issued_at
                    else:
                        raise AuthError('通信エラーです.')
                except ConnectionError:
                    raise AuthError('通信エラーです.')
                except (JSONDecodeError, KeyError):
                    raise AuthError('client.jsonに問題があります.')
        else:
            raise AuthError('client.jsonが存在しません.')
        with open('./json/access.json', mode='w', encoding='utf-8') as wf:
            access_json = {}
            access_json['access_token'] = self.token
            access_json['limit_time'] = self.limit_time
            json.dump(access_json, fp=wf, indent=4)


class AuthError(Exception):
    """認証に関する例外クラス.
    通信エラーやclient.jsonに不備がある場合に呼ばれる.

    """


if __name__ == '__main__':
    auth = Auth()
    print(auth)
