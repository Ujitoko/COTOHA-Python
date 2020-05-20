from cotoha.api import Cotoha


class CotohaDetectMisrecognition(Cotoha):
    """音声認識誤り検知についてのクラス.

    """

    def __init__(self, sentence: str):
        """
        Args:
            sentence (str): 解析対象文.
        """
        super().__init__()
        self.sentence = sentence

        request_json = {'sentence': self.sentence}
        response_dict = self.get_response_dict(
            relative_url='nlp/beta/detect_misrecognition',
            request_body=request_json)
        self.message = response_dict['message']
        self.status = response_dict['status']
        self.detect_misrecognition_result = DetectMisrecognitionResult(
            response_dict['result'])

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{}\n'.format(self.sentence)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        string += self.detect_misrecognition_result.__str__()
        return string


class DetectMisrecognitionResult(object):
    """音声認識誤り検知結果についてのクラス.

    """

    def __init__(self, result_dict: dict):
        self.candidate_info_list = []
        for candidate_result in result_dict['candidates']:
            self.candidate_info_list.append(CandidateInfo(candidate_result))
        self.score = result_dict['score']

    def __str__(self) -> str:
        string = 'score:{}\n'.format(self.score)
        for candidate_info in self.candidate_info_list:
            string += candidate_info.__str__()
        return string


class CandidateInfo(object):
    """音声認識誤り検知部分オブジェクトに関するクラス.

    """

    def __init__(self, candidate_dict: dict):
        self.begin_pos = candidate_dict['begin_pos']
        self.end_pos = candidate_dict['end_pos']
        self.form = candidate_dict['form']
        self.detect_score = candidate_dict['detect_score']
        self.correction_info_list = []
        for correction_result in candidate_dict['correction']:
            self.correction_info_list.append(CorrectionInfo(correction_result))

    def __str__(self) -> str:
        string = 'begin_pos:{}\n'.format(self.begin_pos)
        string += 'end_pos:{}\n'.format(self.end_pos)
        string += 'form:{}\n'.format(self.form)
        string += 'detect_score:{}\n'.format(self.detect_score)
        for correction_info in self.correction_info_list:
            string += correction_info.__str__()
        return string


class CorrectionInfo(object):
    """音声認識誤り訂正結果オブジェクトに関するクラス.

    """

    def __init__(self, correction_dict: dict):
        self.form = correction_dict['form']
        self.correct_score = correction_dict['correct_score']

    def __str__(self) -> str:
        string = 'form:{}\n'.format(self.form)
        string += 'correct_score:{}\n'.format(self.correct_score)
        return string
