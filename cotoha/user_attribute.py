from cotoha.api import Cotoha
from cotoha.api import get_sentence_class


class CotohaUserAttribute(Cotoha):
    """ユーザ属性推定についてのクラス.

    """

    def __init__(self, document: str, kuzure_flag=False,
                 do_segment=False):
        """
        Args:
            document (str): 解析対象文.
            sentence_class (bool, optional): 崩れ文かどうか. Defaults to False.
            do_segment (bool, optional): 文区切りをするかどうか. Defaults to False.
        """
        super().__init__()
        self.document = document
        self.sentence_class = get_sentence_class(kuzure_flag)

        self.do_segment = do_segment
        if type(self.document) == list:
            self.do_segment = False

        request_json = {'document': self.document,
                        'type': self.sentence_class,
                        'do_segment': self.do_segment}
        response_dict = self.get_response_dict(
            relative_url='nlp/beta/user_attribute', request_body=request_json)
        self.message = response_dict['message']
        self.user_attribute_result = UserAttributeResult(
            response_dict['result'])
        self.status = response_dict['status']

    def __str__(self) -> str:
        string = super().__str__()
        string += 'document:{}\n'.format(self.document)
        string += 'do_segment:{}\n'.format(self.do_segment)
        string += 'sentence_class:{}\n'.format(self.sentence_class)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        string += self.user_attribute_result.__str__()
        return string


class UserAttributeError(Exception):
    """ユーザ属性推定に関する例外クラス.
    sentence_classなどにエラーがある場合に呼ばれる.

    """


class UserAttributeResult(object):
    """ユーザ属性推定の結果に関するクラス.

    """

    def __init__(self, result_dict: dict):
        key_list = result_dict.keys()
        if 'age' in key_list:
            self.age = result_dict['age']
        else:
            self.age = None

        if 'civilstatus' in key_list:
            self.civilstatus = result_dict['civilstatus']
        else:
            self.civilstatus = None

        if 'earnings' in key_list:
            self.earnings = result_dict['earnings']
        else:
            self.earnings = None

        if 'gender' in key_list:
            self.gender = result_dict['gender']
        else:
            self.gender = None

        if 'habit' in key_list:
            self.habit_list = result_dict['habit']
        else:
            self.habit_list = []

        if 'hobby' in key_list:
            self.hobby_list = result_dict['hobby']
        else:
            self.hobby_list = []

        if 'kind_of_bussiness' in key_list:
            self.kind_of_bussiness = result_dict['kind_of_bussiness']
        else:
            self.kind_of_bussiness = None

        if 'kind_of_occupation' in key_list:
            self.kind_of_occupation = result_dict['kind_of_occupation']
        else:
            self.kind_of_occupation = None

        if 'location' in key_list:
            self.location = result_dict['location']
        else:
            self.location = None

        if 'moving' in key_list:
            self.moving_list = result_dict['moving']
        else:
            self.moving_list = []

        if 'occupation' in key_list:
            self.occupation = result_dict['occupation']
        else:
            self.occupation = None

        if 'position' in key_list:
            self.position = result_dict['position']
        else:
            self.position = None

    def __str__(self) -> str:
        string = 'age:{}\n'.format(self.age)
        string += 'civilstatus:{}\n'.format(self.civilstatus)
        string += 'earnings:{}\n'.format(self.earnings)
        string += 'gender:{}\n'.format(self.gender)
        string += 'habit_list:{}\n'.format(self.habit_list)
        string += 'hobby_list:{}\n'.format(self.hobby_list)
        string += 'kind_of_bussiness:{}\n'.format(self.kind_of_bussiness)
        string += 'kind_of_occupation:{}\n'.format(self.kind_of_occupation)
        string += 'location:{}\n'.format(self.location)
        string += 'moving_list:{}\n'.format(self.moving_list)
        string += 'occupation:{}\n'.format(self.occupation)
        string += 'position:{}\n'.format(self.position)
        return string
