import requests

from api import Cotoha
from api import RequestsError


class CotohaRemoveFiller(Cotoha):
    """ユーザ属性推定についてのクラス.

    """

    def __init__(self, text: str, do_segment=False):
        super().__init__()
        self.text = text
        self.do_segment = do_segment

        response_dict = self.get_response_dict()
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

    def get_response_dict(self) -> dict:
        """postを実行して,レスポンスを取得する.

        Raises:
            RequestsError: 通信エラーの場合.オフライン状態など.
            RequestsError: レスポンスエラー.アクセストークンが間違っている場合など.

        Returns:
            dict: レスポンスを取得する.
        """
        requests_json = {'text': self.text,
                         'do_segment': self.do_segment}
        url = self.auth.base_url+'nlp/beta/remove_filler'
        try:
            response_dict = requests.post(url=url, json=requests_json,
                                          headers=self.requests_headers).json()
            if response_dict['status'] == 0:
                return response_dict
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')


class RemoveFillerResult(object):
    """言い淀み除去の結果に関するクラス.

    """

    def __init__(self, result_dict: dict):
        self.filler_info_list = []
        for result_filler in result_dict['fillers']:
            self.filler_info_list.append(FillerInfo(result_filler))
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


if __name__ == '__main__':
    cotoha_remove_filler = CotohaRemoveFiller(
        'えーーっと、あの、今日の打ち合わせでしたっけ。すみません、ちょっと、急用が入ってしまって。', do_segment=True)
    print(cotoha_remove_filler)
