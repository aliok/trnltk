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
from xml.dom.minidom import Element, Text

NAMESPACE = "http://trnltk.org/parseset"

class Binding(object):
    @classmethod
    def build(cls, node):
        raise NotImplementedError()

    def to_dom(self):
        raise NotImplementedError()

class ParseSetBinding(Binding):
    def __init__(self):
        self.sentences = []

    @classmethod
    def build(cls, node):
        binding = ParseSetBinding()
        for sentence_node in node.getElementsByTagName("sentence"):
            binding.sentences.append(SentenceBinding.build(sentence_node))

        return binding

    def to_dom(self):
        parseset_node = Element("parseset", namespaceURI=NAMESPACE)
        for sentence in self.sentences:
            parseset_node.appendChild(sentence.to_dom())

        return parseset_node

class SentenceBinding (Binding):
    def __init__(self):
        self.words = []

    @classmethod
    def build(cls, node):
        binding = SentenceBinding()
        for child_node in node.childNodes:
            if not isinstance(child_node, Element):
                continue

            if child_node.tagName=='word':
                binding.words.append(WordBinding.build(child_node))
            elif child_node.tagName=='unparsable_word':
                binding.words.append(UnparsableWordBinding.build(child_node))
            else:
                raise Exception("Unknown tag type : " + child_node.tagName)

        return binding

    def to_dom(self):
        sentence_node = Element("sentence", namespaceURI=NAMESPACE)
        for word in self.words:
            sentence_node.appendChild(word.to_dom())

        return sentence_node

class WordBinding (Binding):
    def __init__(self, str, parse_result, root, syntactic_category, secondary_syntactic_category=None, suffixes=None):
        self.str = str
        self.parse_result = parse_result
        self.root = root
        self.syntactic_category = syntactic_category
        self.secondary_syntactic_category = secondary_syntactic_category
        self.suffixes = suffixes or []

    @classmethod
    def build(cls, node):
        str = node.getAttribute("str")
        parse_result = node.getAttribute("parse_result")
        syntactic_category = node.getAttribute("syntactic_category")
        secondary_syntactic_category = node.getAttribute("secondary_syntactic_category")
        root = RootBinding.build(node.getElementsByTagName("root")[0])
        suffixes = []

        suffixes_nodes = node.getElementsByTagName("suffixes")
        if suffixes_nodes and suffixes_nodes[0]:
            suffixes_node = suffixes_nodes[0]
            for suffix_node in suffixes_node.childNodes:
                if isinstance(suffix_node, Text):
                    continue

                if suffix_node.tagName=='inflectionalSuffix':
                    suffixes.append(InflectionalSuffixBinding.build(suffix_node))
                elif suffix_node.tagName=='derivationalSuffix':
                    suffixes.append(DerivationalSuffixBinding.build(suffix_node))
                else:
                    raise Exception("Unknown suffix type : " + suffix_node.tagName)

        return WordBinding(str, parse_result, root, syntactic_category, secondary_syntactic_category, suffixes)

    def to_dom(self):
        word_node = Element("word", namespaceURI=NAMESPACE)
        word_node.setAttribute("str", self.str)
        word_node.setAttribute("parse_result", self.parse_result)
        word_node.setAttribute("syntactic_category", self.syntactic_category)
        if self.secondary_syntactic_category:
            word_node.setAttribute("secondary_syntactic_category", self.secondary_syntactic_category)

        word_node.appendChild(self.root.to_dom())

        if self.suffixes:
            suffixes_node = Element("suffixes", namespaceURI=NAMESPACE)
            for suffix in self.suffixes:
                suffixes_node.appendChild(suffix.to_dom())
            word_node.appendChild(suffixes_node)

        return word_node

    def format(self):
        return self.parse_result


class SuffixBinding (Binding):
    def __init__(self, id, name, form, application, actual, word, matched_word, to_syntactic_category):
        self.id = id
        self.name = name
        self.form = form
        self.application = application
        self.actual = actual
        self.word = word
        self.matched_word = matched_word
        self.to_syntactic_category = to_syntactic_category

    @classmethod
    def build(cls, node):
        id = node.getAttribute("id")
        name = node.getAttribute("name")
        form = node.getAttribute("form")
        application = node.getAttribute("application")
        actual = node.getAttribute("actual")
        word = node.getAttribute("word")
        matched_word = node.getAttribute("matched_word")
        to_syntactic_category = node.getAttribute("to_syntactic_category")

        return SuffixBinding(id, name, form, application, actual, word, matched_word, to_syntactic_category)

    def to_dom(self):
        suffix_node = Element("suffix", namespaceURI=NAMESPACE)
        suffix_node.setAttribute("id", self.id)
        suffix_node.setAttribute("name", self.name)
        suffix_node.setAttribute("form", self.form)
        suffix_node.setAttribute("application", self.application)
        suffix_node.setAttribute("actual", self.actual)
        suffix_node.setAttribute("word", self.word)
        suffix_node.setAttribute("matched_word", self.matched_word)
        suffix_node.setAttribute("to_syntactic_category", self.to_syntactic_category)
        return suffix_node


class InflectionalSuffixBinding(SuffixBinding):
    def __init__(self, id, name, form, application, actual, word, matched_word, to_syntactic_category):
        super(InflectionalSuffixBinding, self).__init__(id, name, form, application, actual, word, matched_word, to_syntactic_category)

    @classmethod
    def build(cls, node):
        suffix_binding = super(InflectionalSuffixBinding, cls).build(node)
        return InflectionalSuffixBinding(suffix_binding.id, suffix_binding.name, suffix_binding.form, suffix_binding.application, suffix_binding.actual, suffix_binding.word, suffix_binding.matched_word, suffix_binding.to_syntactic_category)

    def to_dom(self):
        node = super(InflectionalSuffixBinding, self).to_dom()
        node.tagName = "inflectionalSuffix"
        return node

class DerivationalSuffixBinding(SuffixBinding):
    def __init__(self, id, name, form, application, actual, word, matched_word, to_syntactic_category):
        super(DerivationalSuffixBinding, self).__init__(id, name, form, application, actual, word, matched_word, to_syntactic_category)

    @classmethod
    def build(cls, node):
        suffix_binding = super(DerivationalSuffixBinding, cls).build(node)
        return DerivationalSuffixBinding(suffix_binding.id, suffix_binding.name, suffix_binding.form, suffix_binding.application, suffix_binding.actual, suffix_binding.word, suffix_binding.matched_word, suffix_binding.to_syntactic_category)

    def to_dom(self):
        node = super(DerivationalSuffixBinding, self).to_dom()
        node.tagName = "derivationalSuffix"
        return node


class UnparsableWordBinding(Binding):
    def __init__(self, str):
        self.str = str

    @classmethod
    def build(cls, node):
        str = node.getAttribute("str")
        return UnparsableWordBinding(str)

    def to_dom(self):
        unparsable_word_node = Element("unparsable_word", namespaceURI=NAMESPACE)
        unparsable_word_node.setAttribute("str", self.str)
        return unparsable_word_node

class RootBinding (Binding):
    def __init__(self, root, lemma, lemma_root, syntactic_category, secondary_syntactic_category=None):
        self.str = root
        self.lemma = lemma
        self.lemma_root = lemma_root
        self.syntactic_category = syntactic_category
        self.secondary_syntactic_category = secondary_syntactic_category

    @classmethod
    def build(cls, node):
        str = node.getAttribute("str")
        lemma = node.getAttribute("lemma")
        lemma_root = node.getAttribute("lemma_root")
        syntactic_category = node.getAttribute("syntactic_category")
        secondary_syntactic_category = node.getAttribute("secondary_syntactic_category")

        return RootBinding(str, lemma, lemma_root, syntactic_category, secondary_syntactic_category)

    def to_dom(self):
        root_node = Element("root", namespaceURI=NAMESPACE)
        root_node.setAttribute("str", self.str)
        root_node.setAttribute("lemma", self.lemma)
        root_node.setAttribute("lemma_root", self.lemma_root)
        root_node.setAttribute("syntactic_category", self.syntactic_category)
        if self.secondary_syntactic_category:
            root_node.setAttribute("secondary_syntactic_category", self.secondary_syntactic_category)
        return root_node