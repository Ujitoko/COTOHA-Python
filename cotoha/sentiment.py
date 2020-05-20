from cotoha.api import Cotoha


class CotohaSentiment(Cotoha):
    """感情分析についてのクラス.

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
            relative_url='nlp/v1/sentiment',
            request_body=request_json)
        self.message = response_dict['message']
        self.status = response_dict['status']
        self.sentiment_result = SentimentResult(response_dict['result'])

    def __str__(self) -> str:
        string = super().__str__()
        string += 'sentence:{}\n'.format(self.sentence)
        string += 'message:{}\n'.format(self.message)
        string += 'status:{}\n'.format(self.status)
        string += self.sentiment_result.__str__()
        return string


class SentimentResult(object):
    """感情分析結果についてのクラス.

    """

    def __init__(self, result_dict: dict):
        self.sentiment = result_dict['sentiment']
        self.score = result_dict['score']
        self.emotional_phrase_list = []
        for emotional_phrase_result in result_dict['emotional_phrase']:
            self.emotional_phrase_list.append(
                EmotionalPhrase(emotional_phrase_result))

    def __str__(self) -> str:
        string = 'sentiment:{}\n'.format(self.sentiment)
        string += 'score:{}\n'.format(self.score)
        for emotional_phrase in self.emotional_phrase_list:
            string += emotional_phrase.__str__()
        return string


class EmotionalPhrase(object):
    """感情フレーズオブジェクトに関するクラス.

    """

    def __init__(self, candidate_dict: dict):
        self.form = candidate_dict['form']
        self.emotion = candidate_dict['emotion']

    def __str__(self) -> str:
        string = 'form:{}\n'.format(self.form)
        string += 'emotion:{}\n'.format(self.emotion)
        return string
