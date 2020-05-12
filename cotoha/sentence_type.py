import requests

from api import Cotoha
from api import RequestsError
from api import check_sentence_class


class CotohaSentenceType(Cotoha):
    """文タイプ判定についてのクラス.

    """

    def __init__(self, sentence: str, sentence_class='default'):
        super().__init__()
        self.sentence = sentence

        if check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise SentenceTypeError('sentence_classにエラーがあります.')

        response_dict = self.get_response_dict()
        self.message = response_dict['message']
        self.status = response_dict['status']
        self.sentence_type_result = SentenceTypeResult(response_dict['result'])

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{}\n'.format(self.sentence)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        string += self.sentence_type_result.__str__()
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
                         }
        url = self.auth.base_url+'nlp/v1/sentence_type'
        try:
            response_dict = requests.post(url=url, json=requests_json,
                                          headers=self.requests_headers).json()
            if response_dict['status'] == 0:
                return response_dict
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')


class SentenceTypeError(Exception):
    """文タイプ判定に関する例外クラス.
    sentence_classに関するエラーがある場合に呼ばれる.

    """


class SentenceTypeResult(object):
    """文タイプ判定結果についてのクラス.

    """

    def __init__(self, result_dict: dict):
        self.modality = result_dict['modality']
        self.dialog_act_list = result_dict['dialog_act']

    def __str__(self) -> str:
        string = 'modality:{}\n'.format(self.modality)
        string += 'dialog_act_list:{}\n'.format(self.dialog_act_list)
        return string


if __name__ == '__main__':
    cotoha_sentence_type = CotohaSentenceType('あなたの名前は何ですか？')
    print(cotoha_sentence_type)
