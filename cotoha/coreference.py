import requests

from api import Cotoha
from api import RequestsError
from api import check_sentence_class


class CotohaCoreference(Cotoha):
    def __init__(self, document: str, sentence_class='default',
                 do_segment=False):
        super().__init__()
        self.document = document
        if check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise CoreferenceError('sentence_classにエラーがあります.')

        self.do_segment = do_segment
        if type(self.document) == list:
            self.do_segment = False

        response_dict = self.get_response_dict()
        self.message = response_dict['message']
        self.coreference_result = CoreferenceResult(response_dict['result'])
        self.status = response_dict['status']

    def __str__(self) -> str:
        string = super().__str__()
        string += 'document:{}\n'.format(self.document)
        string += 'do_segment:{}\n'.format(self.do_segment)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        string += self.coreference_result.__str__()
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
                         'do_segment': self.do_segment}
        url = self.auth.base_url+'nlp/v1/coreference'
        try:
            response_dict = requests.post(url=url, json=requests_json,
                                          headers=self.requests_headers).json()
            if response_dict['status'] == 0:
                return response_dict
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')


class CoreferenceError(Exception):
    """照応解析に関する例外クラス.
    sentence_classなどにエラーがある場合に呼ばれる.

    """


class CoreferenceResult(object):
    """照応解析の結果に関するクラス.

    """

    def __init__(self, result_dict: dict):
        self.coreference_info_list = []
        for result in result_dict['coreference']:
            self.coreference_info_list.append(CoreferenceInfo(result))

        self.token_list = []
        for token in result_dict['tokens']:
            self.token_list.append(token)

    def __str__(self) -> str:
        string = ''
        for coreference_info in self.coreference_info_list:
            string += coreference_info.__str__()

        for token in self.token_list:
            string += token.__str__()
        return string


class CoreferenceInfo(object):
    """照応解析情報オブジェクトに関するクラス.

    """

    def __init__(self, result_dict: dict):
        self.representative_id = result_dict['representative_id']

        self.referent_info_list = []
        for result in result_dict['referents']:
            self.referent_info_list.append(ReferentInfo(result))

    def __str__(self) -> str:
        string = 'representative_id:{}\n'.format(self.representative_id)
        for referent_info in self.referent_info_list:
            string += referent_info.__str__()
        return string


class ReferentInfo(object):
    """エンティティオブジェクトに関するクラス.

    """

    def __init__(self, referent_dict: dict):
        self.referent_id = referent_dict['referent_id']
        self.sentence_id = referent_dict['sentence_id']
        self.token_id_from = referent_dict['token_id_from']
        self.token_id_to = referent_dict['token_id_to']

    def __str__(self) -> str:
        string = 'referent_id:{}\n'.format(self.referent_id)
        string += 'sentence_id:{}\n'.format(self.sentence_id)
        string += 'token_id_from:{}\n'.format(self.token_id_from)
        string += 'token_id_to:{}\n'.format(self.token_id_to)
        return string


if __name__ == '__main__':
    cotoha_coreference = CotohaCoreference('太郎は友人です。彼は焼肉を食べた。')
    print(cotoha_coreference)
