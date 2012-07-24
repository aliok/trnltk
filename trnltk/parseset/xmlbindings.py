from xml.dom.minidom import Element

NAMESPACE = "http://trnltk.org/parseset"

class Binding(object):
    @classmethod
    def build(cls, node):
        raise NotImplementedError()

    def to_dom(self):
        raise NotImplementedError()

class SentenceBinding (Binding):
    def __init__(self):
        self.words = []

    @classmethod
    def build(cls, node):
        binding = SentenceBinding()
        for child_node in node.childNodes:
            if child_node.tagName=='word':
                binding.words.append(WordBinding.build(child_node))
            elif child_node.tagName=='unparsable_word':
                binding.words.append(UnparsableWordBinding(child_node))
            else:
                raise Exception("Unknown tag type : " + child_node.tagName)

        return binding

    def to_dom(self):
        sentence_node = Element("sentence", namespaceURI=NAMESPACE)
        for word in self.words:
            sentence_node.appendChild(word.to_dom())

        return sentence_node

class WordBinding (Binding):
    def __init__(self, str, parse_result, stem, suffixes=None):
        self.str = str
        self.parse_result = parse_result
        self.stem = stem
        self.suffixes = suffixes or []

    @classmethod
    def build(cls, node):
        str = node.getAttribute("str")
        parse_result = node.getAttribute("parse_result")
        stem = StemBinding.build(node.getElementsByTagName("stem")[0])
        suffixes = []

        suffixes_nodes = node.getElementsByTagName("suffixes")
        if suffixes_nodes and suffixes_nodes[0]:
            suffixes_node = suffixes_nodes[0]
            for suffix_node in suffixes_node.childNodes:
                suffixes.append(SuffixBinding.build(suffix_node))

        return WordBinding(str, parse_result, stem, suffixes)

    def to_dom(self):
        word_node = Element("word", namespaceURI=NAMESPACE)
        word_node.setAttribute("str", self.str)
        word_node.setAttribute("parse_result", self.parse_result)
        word_node.appendChild(self.stem.to_dom())

        if self.suffixes:
            suffixes_node = Element("suffixes", namespaceURI=NAMESPACE)
            for suffix in self.suffixes:
                suffixes_node.appendChild(suffix.to_dom())
            word_node.appendChild(suffixes_node)

        return word_node


class SuffixBinding (Binding):
    def __init__(self, id, name, form, application):
        self.id = id
        self.name = name
        self.form = form
        self.application = application

    @classmethod
    def build(cls, node):
        id = node.getAttribute("id")
        name = node.getAttribute("name")
        form = node.getAttribute("form")
        application = node.getAttribute("application")

        return SuffixBinding(id, name, form, application)

    def to_dom(self):
        suffix_node = Element("suffix", namespaceURI=NAMESPACE)
        suffix_node.setAttribute("id", self.id)
        suffix_node.setAttribute("name", self.name)
        suffix_node.setAttribute("form", self.form)
        suffix_node.setAttribute("application", self.application)
        return suffix_node


class InflectionalSuffixBinding(SuffixBinding):
    def __init__(self, id, name, form, application):
        super(InflectionalSuffixBinding, self).__init__(id, name, form, application)

    @classmethod
    def build(cls, suffix_binding):
        suffix_binding = super(InflectionalSuffixBinding, cls).build(suffix_binding)
        return InflectionalSuffixBinding(suffix_binding.id, suffix_binding.name, suffix_binding.form, suffix_binding.application)

    def to_dom(self):
        node = super(InflectionalSuffixBinding, self).to_dom()
        node.tagName = "inflectionalSuffix"
        return node

class DerivationalSuffixBinding(SuffixBinding):
    def __init__(self, id, name, form, application, to):
        super(DerivationalSuffixBinding, self).__init__(id, name, form, application)
        self.to = to

    @classmethod
    def build(cls, node):
        suffix_binding = super(DerivationalSuffixBinding, cls).build(node)
        to = node.getAttribute("to")
        return DerivationalSuffixBinding(suffix_binding.id, suffix_binding.name, suffix_binding.form, suffix_binding.application, to)

    def to_dom(self):
        node = super(DerivationalSuffixBinding, self).to_dom()
        node.tagName = "derivationalSuffix"
        node.setAttribute("to", self.to)
        return node


class UnparsableWordBinding (Binding):
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

class StemBinding (Binding):
    def __init__(self, root, lemma, primary_position, secondary_position=None):
        self.root = root
        self.lemma = lemma
        self.primary_position = primary_position
        self.secondary_position = secondary_position

    @classmethod
    def build(cls, node):
        root = node.getAttribute("root")
        lemma = node.getAttribute("lemma")
        primary_position = node.getAttribute("primary_position")
        secondary_position = node.getAttribute("secondary_position")

        return StemBinding(root, lemma, primary_position, secondary_position)

    def to_dom(self):
        stem_node = Element("stem", namespaceURI=NAMESPACE)
        stem_node.setAttribute("root", self.root)
        stem_node.setAttribute("lemma", self.lemma)
        stem_node.setAttribute("primary_position", self.primary_position)
        stem_node.setAttribute("secondary_position", self.secondary_position)
        return stem_node