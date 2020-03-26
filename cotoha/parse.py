class ParseInfo(object):
    """構文解析結果についてのクラス.

    """

    def __init__(self, parse_dict: dict):
        self.chunk_info = ChunkInfo(parse_dict['chunk_info'])
        self.token_list = []
        for parse in parse_dict['tokens']:
            self.token_list.append(Token(parse))

    def __str__(self) -> str:
        string = self.chunk_info.__str__()
        for token in self.token_list:
            string += token.__str__()
        return string


class ChunkInfo(object):
    """chunk_infoに関するクラス.

    """

    def __init__(self, chunk_dict: dict):
        self.id = chunk_dict['id']
        self.head = chunk_dict['head']
        self.dep = chunk_dict['dep']
        self.chunk_head = chunk_dict['chunk_head']
        self.chunk_func = chunk_dict['chunk_func']
        self.links = []
        for link in chunk_dict['links']:
            self.links.append(LinkInfo(link))

    def __str__(self) -> str:
        string = 'id:{}\n'.format(self.id)
        string += 'head:{}\n'.format(self.head)
        string += 'dep:{}\n'.format(self.dep)
        string += 'chunk_head:{}\n'.format(self.chunk_head)
        string += 'chunk_func:{}\n'.format(self.chunk_func)
        for link in self.links:
            string += link.__str__()
        return string


class LinkInfo(object):
    """chunk_infoのlinksに関するクラス.

    """

    def __init__(self, link_dict: dict):
        self.link = link_dict['link']
        self.label = link_dict['label']

    def __str__(self) -> str:
        string = 'link:{}\n'.format(self.link)
        string += 'label:{}\n'.format(self.label)
        return string


class Token(object):
    """tokensのtokenに関するクラス.

    """

    def __init__(self, token_dict: dict):
        self.id = token_dict['id']
        self.form = token_dict['form']
        self.kana = token_dict['kana']
        self.lemma = token_dict['lemma']
        self.pos = token_dict['pos']
        self.features = token_dict['features']
        self.dependency_labels = []
        if 'dependency_labels' in token_dict.keys():
            for dependency_label in token_dict['dependency_labels']:
                self.dependency_labels.append(Dependency(dependency_label))
        self.attributes = token_dict['attributes']

    def __str__(self) -> str:
        string = 'id:{}\n'.format(self.id)
        string += 'form:{}\n'.format(self.form)
        string += 'kana:{}\n'.format(self.kana)
        string += 'lemma:{}\n'.format(self.lemma)
        string += 'pos:{}\n'.format(self.pos)
        string += 'features:{}\n'.format(self.features)
        string += 'attributes:{}\n'.format(self.attributes)
        for dependency_label in self.dependency_labels:
            string += dependency_label.__str__()
        return string


class Dependency(object):
    """tokenのDependency_labelsに関するクラス.

    """

    def __init__(self, dependency_dict: dict):
        self.token_id = dependency_dict['token_id']
        self.label = dependency_dict['label']

    def __str__(self) -> str:
        string = 'token_id:{}\n'.format(self.token_id)
        string += 'label:{}\n'.format(self.label)
        return string
