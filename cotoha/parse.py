import requests

from api import Cotoha
from api import RequestsError
from api import check_dic_class, check_sentence_class


class CotohaParse(Cotoha):
    """構文解析についてのクラス.

    """

    def __init__(self, sentence: str, sentence_class='default', dic_class=[]):
        super().__init__()
        self.sentence = sentence

        if check_sentence_class(sentence_class):
            self.sentence_class = sentence_class
        else:
            raise ParseError('sentence_classにエラーがあります.')

        if check_dic_class(dic_class):
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


class ParseError(Exception):
    """構文解析に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


class ParseInfo(object):
    """構文解析結果についてのクラス.

    """

    def __init__(self, parse_dict: dict):
        self.chunk_info = ChunkInfo(parse_dict['chunk_info'])
        self.token_list = []
        for parse in parse_dict['tokens']:
            self.token_list.append(Token(parse))

    def __str__(self) -> str:
        string = self.chunk_info.__str__()
        for token in self.token_list:
            string += token.__str__()
        return string


class ChunkInfo(object):
    """chunk_infoに関するクラス.

    """

    def __init__(self, chunk_dict: dict):
        self.id = chunk_dict['id']
        self.head = chunk_dict['head']
        self.dep = chunk_dict['dep']
        self.chunk_head = chunk_dict['chunk_head']
        self.chunk_func = chunk_dict['chunk_func']
        self.links = []
        for link in chunk_dict['links']:
            self.links.append(LinkInfo(link))

    def __str__(self) -> str:
        string = 'id:{}\n'.format(self.id)
        string += 'head:{}\n'.format(self.head)
        string += 'dep:{}\n'.format(self.dep)
        string += 'chunk_head:{}\n'.format(self.chunk_head)
        string += 'chunk_func:{}\n'.format(self.chunk_func)
        for link in self.links:
            string += link.__str__()
        return string


class LinkInfo(object):
    """chunk_infoのlinksに関するクラス.

    """

    def __init__(self, link_dict: dict):
        self.link = link_dict['link']
        self.label = link_dict['label']

    def __str__(self) -> str:
        string = 'link:{}\n'.format(self.link)
        string += 'label:{}\n'.format(self.label)
        return string


class Token(object):
    """tokensのtokenに関するクラス.

    """

    def __init__(self, token_dict: dict):
        self.id = token_dict['id']
        self.form = token_dict['form']
        self.kana = token_dict['kana']
        self.lemma = token_dict['lemma']
        self.pos = token_dict['pos']
        self.features = token_dict['features']
        self.dependency_labels = []
        if 'dependency_labels' in token_dict.keys():
            for dependency_label in token_dict['dependency_labels']:
                self.dependency_labels.append(Dependency(dependency_label))
        self.attributes = token_dict['attributes']

    def __str__(self) -> str:
        string = 'id:{}\n'.format(self.id)
        string += 'form:{}\n'.format(self.form)
        string += 'kana:{}\n'.format(self.kana)
        string += 'lemma:{}\n'.format(self.lemma)
        string += 'pos:{}\n'.format(self.pos)
        string += 'features:{}\n'.format(self.features)
        string += 'attributes:{}\n'.format(self.attributes)
        for dependency_label in self.dependency_labels:
            string += dependency_label.__str__()
        return string


class Dependency(object):
    """tokenのDependency_labelsに関するクラス.

    """

    def __init__(self, dependency_dict: dict):
        self.token_id = dependency_dict['token_id']
        self.label = dependency_dict['label']

    def __str__(self) -> str:
        string = 'token_id:{}\n'.format(self.token_id)
        string += 'label:{}\n'.format(self.label)
        return string


if __name__ == '__main__':
    cotoha_parse = CotohaParse('犬は歩く。')
    print(cotoha_parse)
