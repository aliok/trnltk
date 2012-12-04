"""
Copyright  2012  Ali Ok (aliokATapacheDOTorg)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
class MockMorphemeContainer(object):
    def __init__(self):
        self.parse_result_str = None
        self.surface_str = None
        self.surface_syntactic_category = None
        self.surface_secondary_syntactic_category = None
        self.stem_str = None
        self.stem_syntactic_category = None
        self.stem_secondary_syntactic_category = None
        self.lemma_root_str = None
        self.lemma_root_syntactic_category = None
        self.lemma_root_secondary_syntactic_category = None

    def get_parse_result(self):
        return self.parse_result_str

    def get_surface(self):
        return self.surface_str

    def get_surface_syntactic_category(self):
        return self.surface_syntactic_category

    def get_surface_secondary_syntactic_category(self):
        return self.surface_secondary_syntactic_category

    def get_surface_with_syntactic_categories(self):
        surface = self.get_surface()
        syntactic_category = self.get_surface_syntactic_category()
        secondary_category = self.get_surface_secondary_syntactic_category()

        if secondary_category:
            return u"{}+{}+{}".format(surface, syntactic_category, secondary_category)
        else:
            return u"{}+{}".format(surface, syntactic_category)

    def get_stem(self):
        return self.stem_str

    def get_stem_syntactic_category(self):
        return self.stem_syntactic_category

    def get_stem_secondary_syntactic_category(self):
        return self.stem_secondary_syntactic_category

    def get_stem_with_syntactic_categories(self):
        stem = self.get_stem()
        syntactic_category = self.get_stem_syntactic_category()
        secondary_category = self.get_stem_secondary_syntactic_category()

        if secondary_category:
            return u"{}+{}+{}".format(stem, syntactic_category, secondary_category)
        else:
            return u"{}+{}".format(stem, syntactic_category)

    def get_lemma_root(self):
        return self.lemma_root_str

    def get_lemma_root_syntactic_category(self):
        return self.lemma_root_syntactic_category

    def get_lemma_root_secondary_syntactic_category(self):
        return self.lemma_root_secondary_syntactic_category

    def get_lemma_root_with_syntactic_categories(self):
        lemma_root = self.get_lemma_root()
        syntactic_category = self.get_lemma_root_syntactic_category()
        secondary_category = self.get_lemma_root_secondary_syntactic_category()

        if secondary_category:
            return u"{}+{}+{}".format(lemma_root, syntactic_category, secondary_category)
        else:
            return u"{}+{}".format(lemma_root, syntactic_category)

    def format(self, add_space=False):
        return self.parse_result_str

class MockMorphemeContainerBuilder(object):
    def __init__(self, parse_result_str, surface_str, surface_syntactic_category, surface_secondary_syntactic_category=None):
        self.parse_result_str = parse_result_str
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
        self.lemma_root_secondary_syntactic_category = lemma_root_secondary_syntactic_category

        return self

    def build(self):
        """
        @rtype: MockMorphemeContainer
        """
        mock = MockMorphemeContainer()

        mock.parse_result_str = self.parse_result_str

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
    def builder(cls, parse_result_str, surface_str, surface_syntactic_category, surface_secondary_syntactic_category=None):
        return MockMorphemeContainerBuilder(parse_result_str, surface_str, surface_syntactic_category, surface_secondary_syntactic_category)
