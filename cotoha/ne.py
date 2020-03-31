import requests

from api import Cotoha
from api import RequestsError
from api import check_dic_class, check_sentence_class


class CotohaNe(Cotoha):
    """固有表現抽出に関するクラス.

    """

    def __init__(self, sentence: str, sentence_class='default', dic_class=[]):
        super().__init__()
        self.sentence = sentence

        if check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise NeError('sentence_classにエラーがあります.')

        if check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise NeError('dic_classにエラーがあります.')

    def get_response_dict(self) -> dict:
        pass


class NeError(Exception):
    """固有表現抽出に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


if __name__ == '__main__':
    cotoha_ne = CotohaNe('昨日は東京駅を利用した。')
    print(cotoha_ne)
