from cotoha.api import Cotoha


class CotohaRemoveFiller(Cotoha):
    """ユーザ属性推定についてのクラス.

    """

    def __init__(self, text: str, do_segment=False):
        """
        Args:
            text (str): 解析対象文.
            do_segment (bool, optional): 文区切りをするかどうか. Defaults to False.
        """
        super().__init__()
        self.text = text
        self.do_segment = do_segment

        request_json = {'text': self.text,
                        'do_segment': self.do_segment}
        response_dict = self.get_response_dict(
            relative_url='nlp/beta/remove_filler', request_body=request_json)
        self.message = response_dict['message']
        self.status = response_dict['status']

        self.remove_filler_result_list = []
        for result_dict in response_dict['result']:
            self.remove_filler_result_list.append(
                RemoveFillerResult(result_dict))

    def __str__(self) -> str:
        string = super().__str__()
        string += 'text:{}\n'.format(self.text)
        string += 'do_segment:{}\n'.format(self.do_segment)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        for remove_filler_result in self.remove_filler_result_list:
            string += remove_filler_result.__str__()
        return string


class RemoveFillerResult(object):
    """言い淀み除去の結果に関するクラス.

    """

    def __init__(self, result_dict: dict):
        self.filler_info_list = []
        for filler_result in result_dict['fillers']:
            self.filler_info_list.append(FillerInfo(filler_result))
        self.normalized_sentence = result_dict['normalized_sentence']
        self.fixed_sentence = result_dict['fixed_sentence']

    def __str__(self) -> str:
        string = 'normalized_sentence:{}\n'.format(self.normalized_sentence)
        string += 'fixed_sentence:{}\n'.format(self.fixed_sentence)
        for filler_info in self.filler_info_list:
            string += filler_info.__str__()
        return string


class FillerInfo(object):
    """言い淀み除去範囲オブジェクトに関するクラス.

    """

    def __init__(self, filler_dict: dict):
        self.begin_pos = filler_dict['begin_pos']
        self.end_pos = filler_dict['end_pos']
        self.form = filler_dict['form']

    def __str__(self) -> str:
        string = 'begin_pos:{}\n'.format(self.begin_pos)
        string += 'end_pos:{}\n'.format(self.end_pos)
        string += 'form:{}\n'.format(self.form)
        return string
