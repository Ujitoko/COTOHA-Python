from cotoha.api import Cotoha


class CotohaSummary(Cotoha):
    """要約についてのクラス.

    """

    def __init__(self, document: str, sent_len: int):
        """
        Args:
            document (str): 要約対象文.5文字から5000文字まで.
            sent_len (int): 要約文数.1文から100文まで.

        Raises:
            SummaryError: 入力文章サイズが適していません.
            SummaryError: 要約文数が適していません.
        """
        super().__init__()
        if (5 <= len(document))and(len(document) <= 5000):
            self.document = document
        else:
            raise SummaryError('入力文章サイズが適していません.')

        if (1 <= sent_len)and(sent_len <= 100):
            self.sent_len = sent_len
        else:
            raise SummaryError('要約文数が適していません.')

        request_json = {'document': self.document,
                        'sent_len': self.sent_len
                        }
        response_dict = self.get_response_dict(
            relative_url='nlp/beta/summary',
            request_body=request_json)
        self.status = response_dict['status']
        self.summary_result = response_dict['result']

    def __str__(self) -> str:
        string = super().__str__()
        string += 'document:{}\n'.format(self.document)
        string += 'sent_len:{}\n'.format(self.sent_len)
        string += 'status:{}\n'.format(self.status)
        string += 'summary_result:{}\n'.format(self.summary_result)
        return string


class SummaryError(Exception):
    """要約に関する例外クラス.
    入力パラメータに関するエラーがある場合に呼ばれる.

    """
