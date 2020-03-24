class parse_info(object):
    def __init__(self, parse_dict: dict):
        self.chunk_info = parse_dict['chunk_info']
        self.tokens = []
        for parse in parse_dict['tokens']:
            self.tokens.append(token(parse))


class chunk_info(object):
    def __init__(self, chunk_dict: dict):
        self.id = chunk_dict['id']
        self.head = chunk_dict['head']
        self.dep = chunk_dict['dep']
        self.chunk_head = chunk_dict['chunk_head']
        self.chunk_func = chunk_dict['chunk_func']
        self.links = []
        for link in chunk_dict['links']:
            self.links.append(link_info(link))


class link_info(object):
    def __init__(self, link_dict: dict):
        self.link = link_dict['link']
        self.label = link_dict['label']


class token(object):
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
                self.dependency_labels.append(dependency(dependency_label))
        self.attributes = token_dict['attributes']


class dependency(object):
    def __init__(self, dependency_dict: dict):
        self.token_id = dependency_dict['token_id']
        self.label = dependency_dict['label']
