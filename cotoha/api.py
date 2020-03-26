import requests

from auth import Auth
from parse import ParseInfo


class Cotoha(object):
    """COTOHA-APIに関する基底クラス.

    """

    def __init__(self) -> None:
        self.auth = Auth()
        self.requests_headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': self.auth.token}

    def __str__(self) -> str:
        string = self.auth.__str__()
        string += 'requests_headers:{}\n'.format(self.requests_headers)
        return string

    def check_dic_class(self, dic_class_list: list) -> bool:
        """dic_classに指定以外のクラス(タイプ)がないかどうかを判定する.

        Args:
            dic_class_list (list): __init__の引数,dic_class.

        Returns:
            bool: 指定以外の場合がある場合はFalse.問題なければTrue.
        """
        check_list = ['IT', 'automobile',
                      'chemistry', 'company', 'construction',
                      'economy', 'energy', 'institution',
                      'machinery', 'medical', 'metal']
        for dic_class in dic_class_list:
            if not(dic_class in check_list):
                return False
        return True

    def check_sentence_class(self, sentence_class: str) -> bool:
        """sentence_classが正当かどうか確認する.

        Args:
            sentence_class (str): __init__の引数,sentence_class.

        Returns:
            bool: sentence_classがdefaultかkuzureの場合True,他はFalse.
        """
        if (sentence_class == 'default')or(sentence_class == 'kuzure'):
            return True
        else:
            return False


class CotohaParse(Cotoha):
    """構文解析についてのクラス.

    """

    def __init__(self, sentence: str, sentence_class='default', dic_class=[]):
        super().__init__()
        self.sentence = sentence

        if self.check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise ParseError('sentence_classにエラーがあります.')

        if self.check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise ParseError('dic_classにエラーがあります.')

        response_dict = self.get_response_dict()
        self.message = response_dict['message']
        self.parse_list = self.get_parse_list(response_dict['result'])
        self.status = response_dict['status']

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{}\n'.format(self.sentence)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'dic_class:{}\n'.format(self.dic_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        for parse in self.parse_list:
            string += parse.__str__()
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

    def get_parse_list(self, result_list: list) -> list:
        """response jsonからparse_listを取得する.

        Args:
            result_list (list): response jsonのresult項目のlist

        Returns:
            list: ParseInfoクラスのリスト.
        """
        parse_list = []
        for result in result_list:
            parse_list.append(ParseInfo(result))
        return parse_list


class RequestsError(Exception):
    """APIに関する例外クラス.
    通信エラーやAPIに関するエラーがある場合に呼ばれる.

    """


class ParseError(Exception):
    """構文解析に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


if __name__ == '__main__':
    cotoha_parse = CotohaParse('犬は歩く。')
    print(cotoha_parse)
