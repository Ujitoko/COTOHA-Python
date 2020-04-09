import requests

from api import Cotoha
from api import RequestsError
from api import check_sentence_class, check_dic_class


class CotohaSimilarity(Cotoha):
    """類似度算出に関するクラス.

    """

    def __init__(self, s1: str, s2: str,
                 sentence_class='default', dic_class=[]):
        super().__init__()
        self.s1 = s1
        self.s2 = s2
        if check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise SimilarityError('sentence_classにエラーがあります.')

        if check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise SimilarityError('dic_classにエラーがあります.')

        response_dict = self.get_response_dict()
        self.message = response_dict['message']
        self.status = response_dict['status']
        self.similarity_result = SimilarityResult(response_dict['result'])

    def __str__(self) -> str:
        string = super().__str__()
        string += 's1:{}\n'.format(self.s1)
        string += 's2:{}\n'.format(self.s2)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'dic_class:{}\n'.format(self.dic_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        string += self.similarity_result.__str__()
        return string

    def get_response_dict(self) -> dict:
        """postを実行して,レスポンスを取得する.

        Raises:
            RequestsError: 通信エラーの場合.オフライン状態など.
            RequestsError: レスポンスエラー.アクセストークンが間違っている場合など.

        Returns:
            dict: レスポンスを取得する.
        """
        requests_json = {'s1': self.s1,
                         's2': self.s2,
                         'type': self.sentence_class,
                         'dic_type': self.dic_class}
        url = self.auth.base_url+'nlp/v1/similarity'
        try:
            response_dict = requests.post(url=url, json=requests_json,
                                          headers=self.requests_headers).json()
            if response_dict['status'] == 0:
                return response_dict
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')


class SimilarityError(Exception):
    """類似度算出に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


class SimilarityResult(object):
    """類似度算出結果についてのクラス.

    """

    def __init__(self, result_dict: dict):
        self.score = result_dict['score']

    def __str__(self) -> str:
        return 'score:{}\n'.format(self.score)


if __name__ == '__main__':
    cotoha_similarity = CotohaSimilarity(
        '近くのレストランはどこですか？', 'このあたりの定食屋はどこにありますか？')
    print(cotoha_similarity)
