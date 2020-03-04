import datetime
import json
import requests


class Auth(object):
    def __init__(self):
        with open('./json/access.json', 'r', encoding='utf-8') as rf:
            access_json = json.load(rf)
            self.limit_time = access_json['limit_time']
            if not(self.check_token()):
                self.update_token()
        

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
        with open('./json/client.json', 'r', encoding='utf-8') as rf:
            requests_json = json.load(rf)
            publish_url = requests_json.pop('publish_url')
            requests_headers = {'Content-Type': 'application/json'}
            r = requests.post(url=publish_url, json=requests_json,
                              headers=requests_headers)
            response_json = r.json()
            expires_in = int(response_json['expires_in'])
            issued_at = int(response_json['issued_at'][:-3])
            token = response_json['access_token']
        
        with open('./json/access.json', mode='w', encoding='utf-8') as wf:
            json.dump(access_json, fp=wf, indent=4)


if __name__ == '__main__':
    Auth()
