from cotoha.api import Cotoha
from cotoha.api import get_sentence_class


class CotohaSentenceType(Cotoha):
    """文タイプ判定についてのクラス.

    """

    def __init__(self, sentence: str, kuzure_flag=False):
        """
        Args:
            sentence (str): 解析対象文.
            kuzure_flag (bool, optional): 崩れ文かどうか. Defaults to False.

        Raises:
            SentenceTypeError: dic_classにエラーがあります.
        """
        super().__init__()
        self.sentence = sentence

        self.sentence_class = get_sentence_class(kuzure_flag)

        request_json = {'sentence': self.sentence,
                        'type': self.sentence_class,
                        }
        response_dict = self.get_response_dict(
            relative_url='nlp/v1/sentence_type', request_body=request_json)
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
