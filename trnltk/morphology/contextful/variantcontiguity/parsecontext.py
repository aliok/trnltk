class MockMorphemeContainer(object):
    def __init__(self):
        self.surface_str = None
        self.surface_syntactic_category = None
        self.surface_secondary_syntactic_category = None
        self.stem_str = None
        self.stem_syntactic_category = None
        self.stem_secondary_syntactic_category = None
        self.lemma_root_str = None
        self.lemma_root_syntactic_category = None
        self.lemma_root_secondary_syntactic_category = None

    def get_surface(self):
        return self.surface_str

    def get_surface_syntactic_category(self):
        return self.surface_syntactic_category

    def get_surface_secondary_syntactic_category(self):
        return self.surface_secondary_syntactic_category

    def get_stem(self):
        return self.stem_str

    def get_stem_syntactic_category(self):
        return self.stem_syntactic_category

    def get_stem_secondary_syntactic_category(self):
        return self.stem_secondary_syntactic_category

    def get_lemma_root(self):
        return self.lemma_root_str

    def get_lemma_root_syntactic_category(self):
        return self.lemma_root_syntactic_category

    def get_lemma_root_secondary_syntactic_category(self):
        return self.lemma_root_secondary_syntactic_category


class MockMorphemeContainerBuilder(object):
    def __init__(self, surface_str, surface_syntactic_category, surface_secondary_syntactic_category=None):
        self.surface_str = surface_str
        self.surface_syntactic_category = surface_syntactic_category
        self.surface_secondary_syntactic_category = surface_secondary_syntactic_category
        self.stem_str = None
        self.stem_syntactic_category = None
        self.stem_secondary_syntactic_category = None
        self.lemma_root_str = None
        self.lemma_root_syntactic_category = None
        self.lemma_root_secondary_syntactic_category = None

    def stem(self, stem_str, stem_syntactic_category=None, stem_secondary_syntactic_category=None):
        self.stem_str = stem_str
        self.stem_syntactic_category = stem_syntactic_category
        self.stem_secondary_syntactic_category = stem_secondary_syntactic_category

        return self

    def lexeme(self, lemma_root_str, lemma_root_syntactic_category=None, lemma_root_secondary_syntactic_category=None):
        self.lemma_root_str = lemma_root_str
        self.lemma_root_syntactic_category = lemma_root_syntactic_category
        self.lemma_root_secondary_syntactic_category = lemma_root_syntactic_category

        return self

    def build(self):
        """
        @rtype: MockMorphemeContainer
        """
        mock = MockMorphemeContainer()

        mock.surface_str = self.surface_str
        mock.surface_syntactic_category = self.surface_syntactic_category
        mock.surface_secondary_syntactic_category = self.surface_secondary_syntactic_category

        mock.stem_str = self.stem_str if self.stem_str else self.surface_str
        mock.stem_syntactic_category = self.stem_syntactic_category if self.stem_syntactic_category else self.surface_syntactic_category
        mock.stem_secondary_syntactic_category = self.stem_secondary_syntactic_category if self.stem_syntactic_category else self.surface_secondary_syntactic_category

        mock.lemma_root_str = self.lemma_root_str if self.lemma_root_str else self.surface_str
        mock.lemma_root_syntactic_category = self.lemma_root_syntactic_category if self.lemma_root_syntactic_category else self.surface_syntactic_category
        mock.lemma_root_secondary_syntactic_category = self.lemma_root_secondary_syntactic_category if self.lemma_root_syntactic_category else self.surface_secondary_syntactic_category

        return mock

    @classmethod
    def builder(cls, surface_str, surface_syntactic_category, surface_secondary_syntactic_category=None):
        return MockMorphemeContainerBuilder(surface_str, surface_syntactic_category, surface_secondary_syntactic_category)
