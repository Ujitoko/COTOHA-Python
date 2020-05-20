from cotoha.api import Cotoha
from cotoha.api import check_dic_class, get_sentence_class


class CotohaNe(Cotoha):
    """固有表現抽出に関するクラス.

    """

    def __init__(self, sentence: str, kuzure_flag=False, dic_class=[]):
        """
        Args:
            sentence (str): 解析対象文.
            sentence_class (bool, optional): 崩れ文かどうか. Defaults to False.
            dic_class (list, optional): 専門用語辞書. Defaults to [].

        Raises:
            NeError: dic_classにエラーがある場合.
        """
        super().__init__()
        self.sentence = sentence
        self.sentence_class = get_sentence_class(kuzure_flag)

        if check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise NeError('dic_classにエラーがあります.')

        request_json = {'sentence': self.sentence,
                        'type': self.sentence_class,
                        'dic_type': self.dic_class}
        response_dict = self.get_response_dict(
            relative_url='nlp/v1/ne', request_body=request_json)
        self.message = response_dict['message']
        self.status = response_dict['status']

        self.ne_result_list = []
        for result_dict in response_dict['result']:
            self.ne_result_list.append(NeResult(result_dict))

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{}\n'.format(self.sentence)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'dic_class:{}\n'.format(self.dic_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        for ne_result in self.ne_result_list:
            string += ne_result.__str__()
        return string


class NeError(Exception):
    """固有表現抽出に関する例外クラス.
    dic_classやsentence_classに関するエラーがある場合に呼ばれる.

    """


class NeResult(object):
    """固有表現抽出の結果に関するクラス.

    """

    def __init__(self, result_dict: dict):
        self.begin_pos = result_dict['begin_pos']
        self.end_pos = result_dict['end_pos']
        self.form = result_dict['form']
        self.std_form = result_dict['std_form']
        self.ne_class = result_dict['class']
        self.extended_class = result_dict['extended_class']
        self.source = result_dict['source']

    def __str__(self):
        string = 'begin_pos:{}\n'.format(self.begin_pos)
        string += 'end_pos:{}\n'.format(self.end_pos)
        string += 'form:{}\n'.format(self.form)
        string += 'std_form:{}\n'.format(self.std_form)
        string += 'ne_class:{}\n'.format(self.ne_class)
        string += 'extended_class:{}\n'.format(self.extended_class)
        string += 'source:{}\n'.format(self.source)
        return string
