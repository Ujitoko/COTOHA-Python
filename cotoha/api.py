import requests

from auth import Auth
from parse.parse import parse_info


class Cotoha(object):
    """COTOHA-APIに関する基底クラス

    """

    def __init__(self) -> None:
        self.auth = Auth()
        self.requests_headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': self.auth.token}

    def __str__(self) -> str:
        string = self.auth.__str__()
        string += 'requests_headers:{0}\n'\
            .format(self.requests_headers)
        return string


class CotohaParse(Cotoha):
    """構文解析についてのクラス.

    """

    def __init__(self, sentence: str, sentence_class='default', dic_class=[]):
        super().__init__()
        self.sentence = sentence
        self.sentence_class = sentence_class
        self.dic_class = dic_class
        response_dict = self.get_response_dict()
        self.message = response_dict['message']
        self.parse_list = self.get_parse_list(response_dict['result'])
        self.status = response_dict['status']

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{0}\nsentence_class:{1}\ndic_class:{2}\n'\
            .format(self.sentence, self.sentence_class, self.dic_class)
        return string

    def get_response_dict(self) -> dict:
        """postを実行して,レスポンスを取得する.

        Raises:
            RequestsError: 通信エラーの場合.オフライン状態など.
            RequestsError: レスポンスエラー.アクセストークンが間違っている場合など.

        Returns:
            dict: レスポンスを取得する.
        """
        requests_json = {'sentence': self.sentence,
                         'type': self.sentence_class,
                         'dic_type': self.dic_class}
        url = self.auth.base_url+'nlp/v1/parse'
        try:
            response_json = requests.post(url=url, json=requests_json,
                                          headers=self.requests_headers).json()
            if response_json['status'] == 0:
                return response_json
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')

    def get_parse_list(self, result_list: list):
        parse_list = []
        for result in result_list:
            parse_list.append(parse_info(result))
        return parse_list


class RequestsError(Exception):
    """APIに関する例外クラス.
    通信エラーやAPIに関するエラーがある場合に呼ばれる.

    """


if __name__ == '__main__':
    cotoha_parse = CotohaParse('犬は歩く。')
    print(cotoha_parse)
