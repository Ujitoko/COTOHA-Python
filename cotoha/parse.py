from cotoha.api import Cotoha
from cotoha.api import check_dic_class, get_sentence_class


class CotohaParse(Cotoha):
    """構文解析についてのクラス.

    """

    def __init__(self, sentence: str, kuzure_flag=False, dic_class=[]):
        """
        Args:
            sentence (str): 解析対象文.
            sentence_class (bool, optional): 崩れ文かどうか. Defaults to False.
            dic_class (list, optional): 専門用語辞書. Defaults to [].

        Raises:
            ParseError: dic_classにエラーがある場合.
        """
        super().__init__()
        self.sentence = sentence
        self.sentence_class = get_sentence_class(kuzure_flag)

        if check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise ParseError('dic_classにエラーがあります.')

        request_json = {'sentence': self.sentence,
                        'type': self.sentence_class,
                        'dic_type': self.dic_class}
        response_dict = self.get_response_dict(
            relative_url='nlp/v1/parse', request_body=request_json)
        self.message = response_dict['message']
        self.status = response_dict['status']
        self.parse_result_list = []
        for result_dict in response_dict['result']:
            self.parse_result_list.append(ParseResult(result_dict))

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{}\n'.format(self.sentence)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'dic_class:{}\n'.format(self.dic_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        for parse_result in self.parse_result_list:
            string += parse_result.__str__()
        return string


class ParseError(Exception):
    """構文解析に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


class ParseResult(object):
    """構文解析結果についてのクラス.

    """

    def __init__(self, result_dict: dict):
        self.chunk_info = ChunkInfo(result_dict['chunk_info'])
        self.token_info_list = []
        for token_result in result_dict['tokens']:
            self.token_info_list.append(TokenInfo(token_result))

    def __str__(self) -> str:
        string = self.chunk_info.__str__()
        for token_info in self.token_info_list:
            string += token_info.__str__()
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
        self.link_info_list = []
        for link_result in chunk_dict['links']:
            self.link_info_list.append(LinkInfo(link_result))

    def __str__(self) -> str:
        string = 'id:{}\n'.format(self.id)
        string += 'head:{}\n'.format(self.head)
        string += 'dep:{}\n'.format(self.dep)
        string += 'chunk_head:{}\n'.format(self.chunk_head)
        string += 'chunk_func:{}\n'.format(self.chunk_func)
        for link_info in self.link_info_list:
            string += link_info.__str__()
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


class TokenInfo(object):
    """tokensのtokenに関するクラス.

    """

    def __init__(self, token_dict: dict):
        self.id = token_dict['id']
        self.form = token_dict['form']
        self.kana = token_dict['kana']
        self.lemma = token_dict['lemma']
        self.pos = token_dict['pos']
        self.features = token_dict['features']
        self.dependency_label_list = []
        if 'dependency_labels' in token_dict.keys():
            for dependency_label in token_dict['dependency_labels']:
                self.dependency_label_list.append(
                    DependencyLabel(dependency_label))
        self.attributes = token_dict['attributes']

    def __str__(self) -> str:
        string = 'id:{}\n'.format(self.id)
        string += 'form:{}\n'.format(self.form)
        string += 'kana:{}\n'.format(self.kana)
        string += 'lemma:{}\n'.format(self.lemma)
        string += 'pos:{}\n'.format(self.pos)
        string += 'features:{}\n'.format(self.features)
        string += 'attributes:{}\n'.format(self.attributes)
        for dependency_label in self.dependency_label_list:
            string += dependency_label.__str__()
        return string


class DependencyLabel(object):
    """tokenのDependency_labelsに関するクラス.

    """

    def __init__(self, dependency_dict: dict):
        self.token_id = dependency_dict['token_id']
        self.label = dependency_dict['label']

    def __str__(self) -> str:
        string = 'token_id:{}\n'.format(self.token_id)
        string += 'label:{}\n'.format(self.label)
        return string
