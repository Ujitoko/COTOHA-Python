import requests

from api import Cotoha
from api import RequestsError
from api import check_sentence_class, check_dic_class


class CotohaKeyword(Cotoha):
    """キーワード抽出に関するクラス.

    """

    def __init__(self, document: str, sentence_class='default',
                 do_segment=False, max_keyword_num=5, dic_class=[]):
        super().__init__()
        self.document = document
        if check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise KeywordError('sentence_classにエラーがあります.')

        self.do_segment = do_segment
        if type(self.document) == list:
            self.do_segment = False

        if max_keyword_num >= 1:
            self.max_keyword_num = max_keyword_num
        else:
            self.max_keyword_num = 5

        if check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise KeywordError('dic_classにエラーがあります.')

        response_dict = self.get_response_dict()
        self.message = response_dict['message']
        self.status = response_dict['status']

        self.keyword_result_list = []
        for result_dict in response_dict['result']:
            self.keyword_result_list.append(KeywordResult(result_dict))

    def __str__(self) -> str:
        string = super().__str__()
        string += 'document:{}\n'.format(self.document)
        string += 'do_segment:{}\n'.format(self.do_segment)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'max_keyword_num:{}\n'.format(self.max_keyword_num)
        string += 'dic_class:{}\n'.format(self.dic_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        for keyword_result in self.keyword_result_list:
            string += keyword_result.__str__()
        return string

    def get_response_dict(self) -> dict:
        """postを実行して,レスポンスを取得する.

        Raises:
            RequestsError: 通信エラーの場合.オフライン状態など.
            RequestsError: レスポンスエラー.アクセストークンが間違っている場合など.

        Returns:
            dict: レスポンスを取得する.
        """
        requests_json = {'document': self.document,
                         'type': self.sentence_class,
                         'do_segment': self.do_segment,
                         'max_keyword_num': self.max_keyword_num,
                         'dic_type': self.dic_class}
        url = self.auth.base_url+'nlp/v1/keyword'
        try:
            response_dict = requests.post(url=url, json=requests_json,
                                          headers=self.requests_headers).json()
            if response_dict['status'] == 0:
                return response_dict
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')


class KeywordError(Exception):
    """キーワード抽出に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


class KeywordResult(object):
    """キーワード抽出結果についてのクラス.

    """

    def __init__(self, result_dict: dict):
        self.form = result_dict['form']
        self.score = result_dict['score']

    def __str__(self) -> str:
        string = 'form:{}\n'.format(self.form)
        string += 'score:{}\n'.format(self.score)
        return string


if __name__ == '__main__':
    cotoha_keyword = CotohaKeyword('レストランで昼食を食べた。', do_segment=True,
                                   max_keyword_num=2)
    print(cotoha_keyword)
