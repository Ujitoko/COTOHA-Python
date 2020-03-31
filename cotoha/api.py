from abc import ABCMeta, abstractmethod

from auth import Auth


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

    @abstractmethod
    def get_response_dict(self) -> dict:
        pass


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


def check_sentence_class(sentence_class: str) -> bool:
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


class RequestsError(Exception):
    """APIに関する例外クラス.
    通信エラーやAPIに関するエラーがある場合に呼ばれる.

    """
