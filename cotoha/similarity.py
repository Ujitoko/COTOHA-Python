from cotoha.api import Cotoha
from cotoha.api import get_sentence_class, check_dic_class


class CotohaSimilarity(Cotoha):
    """類似度算出に関するクラス.

    """

    def __init__(self, s1: str, s2: str,
                 kuzure_flag=False, dic_class=[]):
        """
        Args:
            s1 (str): 解析対象文1.
            s2 (str): 解析対象文2.
            kuzure_flag (bool, optional): 崩れ文かどうか. Defaults to False.
            dic_class (list, optional): 専門用語辞書. Defaults to [].

        Raises:
            SimilarityError: dic_classにエラーがあります.
        """
        super().__init__()
        self.s1 = s1
        self.s2 = s2
        self.sentence_class = get_sentence_class(kuzure_flag)

        if check_dic_class(dic_class):
            self.dic_class = dic_class
        else:
            raise SimilarityError('dic_classにエラーがあります.')

        request_json = {'s1': self.s1,
                        's2': self.s2,
                        'type': self.sentence_class,
                        'dic_type': self.dic_class}
        response_dict = self.get_response_dict(
            relative_url='nlp/v1/similarity', request_body=request_json)
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
