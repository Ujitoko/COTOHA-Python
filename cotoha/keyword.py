from cotoha.api import Cotoha
from cotoha.api import get_sentence_class, check_dic_class


class CotohaKeyword(Cotoha):
    """キーワード抽出に関するクラス.

    """

    def __init__(self, document: str, kuzure_flag=False,
                 do_segment=False, max_keyword_num=5, dic_class=[]):
        """
        Args:
            document (str): 解析対象文.
            sentence_class (str, optional): 崩れ文かどうか. Defaults to 'default'.
            do_segment (bool, optional): 文区切りするかどうか. Defaults to False.
            max_keyword_num (int, optional): 抽出する単語上限. Defaults to 5.
            dic_class (list, optional): 専門用語辞書. Defaults to [].

        Raises:
            KeywordError: dic_classにエラーがある場合.
        """
        super().__init__()
        self.document = document
        self.sentence_class = get_sentence_class(kuzure_flag)

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

        request_json = {'document': self.document,
                        'type': self.sentence_class,
                        'do_segment': self.do_segment,
                        'max_keyword_num': self.max_keyword_num,
                        'dic_type': self.dic_class}
        response_dict = self.get_response_dict(
            relative_url='nlp/v1/keyword', request_body=request_json)
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
