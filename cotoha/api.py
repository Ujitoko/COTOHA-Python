from abc import ABCMeta

import requests

from cotoha.auth import Auth


class Cotoha(metaclass=ABCMeta):
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

    def get_response_dict(self, relative_url: str,
                          request_body: dict) -> dict:
        """postを実行して,レスポンスを取得する.

        Args:
            relative_url (str): Base URLからの相対パス.
            requests_json (dict): リクエストボディ.

        Raises:
            RequestsError: 通信エラーの場合.オフライン状態など.
            RequestsError: レスポンスエラー.アクセストークンが間違っている場合など.

        Returns:
            dict: レスポンスを取得する.
        """
        url = self.auth.base_url+relative_url
        try:
            response_dict = requests.post(url=url, json=request_body,
                                          headers=self.requests_headers).json()
            if response_dict['status'] == 0:
                return response_dict
            else:
                raise RequestsError('レスポンスエラー.')
        except ConnectionError:
            raise RequestsError('通信エラーです.')


def check_dic_class(dic_class_list: list) -> bool:
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


def get_sentence_class(kuzure_flag: bool) -> str:
    """kuzure_flagによってsentence_classを返す.

    Args:
        kuzure_flag (bool): 崩れ文かどうか.

    Returns:
        str: kuzure_flagがTrueの場合はkuzure,Falseの場合はdefault.
    """
    if (kuzure_flag):
        return 'kuzure'
    else:
        return 'default'


class RequestsError(Exception):
    """APIに関する例外クラス.
    通信エラーやAPIに関するエラーがある場合に呼ばれる.

    """
