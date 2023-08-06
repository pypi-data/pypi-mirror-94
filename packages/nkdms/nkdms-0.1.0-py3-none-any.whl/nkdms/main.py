class CollectionSelector:
    def __init__(self, collection):
        self.collection = collection

    def select_by_size(self, *args):
        return None

    def select_by_name(self, *args):
        return None

    def select_by_piece_size(self, *args):
        return None

    def select_by_name_regex(self, *args):
        return None


class DocumentCollection:
    def __init__(self, name, creator, created, modified, content_type, size):
        self.documents = {}
        self.name = name
        self.creator = creator
        self.created = created
        self.modified = modified
        self.content_type = content_type
        self.length = len(self.documents)
        self.size = size
        self.locked = False

    def __repr__(self):
        return f'{self.name} {self.creator} {self.created} {self.modified} {self.content_type} {self.length} {self.size} {self.locked} ' \
               '{self.documents}'

    def append(self, document):
        if not self.locked:
            self.documents.append(document)

    def remove(self, document):
        if not self.locked:
            self.documents.remove(document)

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def merge(self, another):
        self.documents = {self.documents | another.documents}  # TODO check this merge

    def split(self):
        collection_splitter = CollectionSelector(self.documents)
        return collection_splitter.select_by_name()

    def take_part(self, rule):
        return self.documents[:5]  # TODO make taking part by rule

    def export(self):
        # TODO RAR TE KOLEKCIJE
        pass

    def load(self):
        pass


class AdvancedCollection:
    def __init__(self, root: DocumentCollection, *children: DocumentCollection):
        """

        :type children: DocumentCollection set
        """
        self.root = root
        self.children = children


class Document:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f'{self.name} {self.type}'


class User:
    def __init__(self, name):
        self.name = name


def add(a, b):
    return a + b
