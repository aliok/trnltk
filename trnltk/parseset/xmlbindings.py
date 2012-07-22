# ./xmlbindings.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e3d207a6b81fd6da9c2bcf9b572187e115013766
# Generated 2012-07-22 16:15:10.578863 by PyXB version 1.1.4
# Namespace http://trnltk.org/parseset

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:a593513e-d407-11e1-b24a-080027f3a520')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://trnltk.org/parseset', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.
    
    @kw default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)


# Atomic SimpleTypeDefinition
class PrimaryPositionType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PrimaryPositionType')
    _Documentation = None
PrimaryPositionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=PrimaryPositionType, enum_prefix=None)
PrimaryPositionType.Noun = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Noun', tag=u'Noun')
PrimaryPositionType.Adj = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Adj', tag=u'Adj')
PrimaryPositionType.Adv = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Adv', tag=u'Adv')
PrimaryPositionType.Conj = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Conj', tag=u'Conj')
PrimaryPositionType.Interj = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Interj', tag=u'Interj')
PrimaryPositionType.Verb = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Verb', tag=u'Verb')
PrimaryPositionType.Pron = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Pron', tag=u'Pron')
PrimaryPositionType.Num = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Num', tag=u'Num')
PrimaryPositionType.Det = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Det', tag=u'Det')
PrimaryPositionType.Part = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Part', tag=u'Part')
PrimaryPositionType.QuesPart = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'QuesPart', tag=u'QuesPart')
PrimaryPositionType.Punc = PrimaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Punc', tag=u'Punc')
PrimaryPositionType._InitializeFacetMap(PrimaryPositionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'PrimaryPositionType', PrimaryPositionType)

# Atomic SimpleTypeDefinition
class SecondaryPositionType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SecondaryPositionType')
    _Documentation = None
SecondaryPositionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=SecondaryPositionType, enum_prefix=None)
SecondaryPositionType.Dup = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Dup', tag=u'Dup')
SecondaryPositionType.Postp = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Postp', tag=u'Postp')
SecondaryPositionType.Ques = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Ques', tag=u'Ques')
SecondaryPositionType.Demons = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Demons', tag=u'Demons')
SecondaryPositionType.Reflex = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Reflex', tag=u'Reflex')
SecondaryPositionType.Pers = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Pers', tag=u'Pers')
SecondaryPositionType.Time = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Time', tag=u'Time')
SecondaryPositionType.Prop = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Prop', tag=u'Prop')
SecondaryPositionType.Abbr = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Abbr', tag=u'Abbr')
SecondaryPositionType.Card = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Card', tag=u'Card')
SecondaryPositionType.Ord = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Ord', tag=u'Ord')
SecondaryPositionType.Digits = SecondaryPositionType._CF_enumeration.addEnumeration(unicode_value=u'Digits', tag=u'Digits')
SecondaryPositionType._InitializeFacetMap(SecondaryPositionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'SecondaryPositionType', SecondaryPositionType)

# Complex type SuffixType with content type EMPTY
class SuffixType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SuffixType')
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httptrnltk_orgparseset_SuffixType_name', pyxb.binding.datatypes.string, required=True)

    name = property(__name.value, __name.set, None, None)


    # Attribute application uses Python identifier application
    __application = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'application'), 'application', '__httptrnltk_orgparseset_SuffixType_application', pyxb.binding.datatypes.string, required=True)

    application = property(__application.value, __application.set, None, None)


    # Attribute form uses Python identifier form
    __form = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'form'), 'form', '__httptrnltk_orgparseset_SuffixType_form', pyxb.binding.datatypes.string, required=True)

    form = property(__form.value, __form.set, None, None)


    _ElementMap = {

    }
    _AttributeMap = {
        __name.name() : __name,
        __application.name() : __application,
        __form.name() : __form
    }
Namespace.addCategoryObject('typeBinding', u'SuffixType', SuffixType)


# Complex type WordType with content type ELEMENT_ONLY
class WordType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'WordType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://trnltk.org/parseset}stem uses Python identifier stem
    __stem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'stem'), 'stem', '__httptrnltk_orgparseset_WordType_httptrnltk_orgparsesetstem', False)


    stem = property(__stem.value, __stem.set, None, None)


    # Element {http://trnltk.org/parseset}suffixes uses Python identifier suffixes
    __suffixes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'suffixes'), 'suffixes', '__httptrnltk_orgparseset_WordType_httptrnltk_orgparsesetsuffixes', False)


    suffixes = property(__suffixes.value, __suffixes.set, None, None)


    # Attribute str uses Python identifier str
    __str = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'str'), 'str', '__httptrnltk_orgparseset_WordType_str', pyxb.binding.datatypes.string, required=True)

    str = property(__str.value, __str.set, None, None)


    # Attribute parse_result uses Python identifier parse_result
    __parse_result = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'parse_result'), 'parse_result', '__httptrnltk_orgparseset_WordType_parse_result', pyxb.binding.datatypes.string, required=True)

    parse_result = property(__parse_result.value, __parse_result.set, None, None)


    _ElementMap = {
        __stem.name() : __stem,
        __suffixes.name() : __suffixes
    }
    _AttributeMap = {
        __str.name() : __str,
        __parse_result.name() : __parse_result
    }
Namespace.addCategoryObject('typeBinding', u'WordType', WordType)


# Complex type SentenceType with content type ELEMENT_ONLY
class SentenceType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SentenceType')
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://trnltk.org/parseset}word uses Python identifier word
    __word = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'word'), 'word', '__httptrnltk_orgparseset_SentenceType_httptrnltk_orgparsesetword', True)


    word = property(__word.value, __word.set, None, None)


    _ElementMap = {
        __word.name() : __word
    }
    _AttributeMap = {

    }
Namespace.addCategoryObject('typeBinding', u'SentenceType', SentenceType)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    # Element {http://trnltk.org/parseset}suffix uses Python identifier suffix
    __suffix = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'suffix'), 'suffix', '__httptrnltk_orgparseset_CTD_ANON_httptrnltk_orgparsesetsuffix', True)


    suffix = property(__suffix.value, __suffix.set, None, None)


    _ElementMap = {
        __suffix.name() : __suffix
    }
    _AttributeMap = {

    }



# Complex type StemType with content type EMPTY
class StemType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StemType')
    # Base type is pyxb.binding.datatypes.anyType

    # Attribute primary_position uses Python identifier primary_position
    __primary_position = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'primary_position'), 'primary_position', '__httptrnltk_orgparseset_StemType_primary_position', PrimaryPositionType, required=True)

    primary_position = property(__primary_position.value, __primary_position.set, None, None)


    # Attribute root uses Python identifier root
    __root = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'root'), 'root', '__httptrnltk_orgparseset_StemType_root', pyxb.binding.datatypes.string, required=True)

    root = property(__root.value, __root.set, None, None)


    # Attribute lemma uses Python identifier lemma
    __lemma = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lemma'), 'lemma', '__httptrnltk_orgparseset_StemType_lemma', pyxb.binding.datatypes.string, required=True)

    lemma = property(__lemma.value, __lemma.set, None, None)


    # Attribute secondary_position uses Python identifier secondary_position
    __secondary_position = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'secondary_position'), 'secondary_position', '__httptrnltk_orgparseset_StemType_secondary_position', SecondaryPositionType)

    secondary_position = property(__secondary_position.value, __secondary_position.set, None, None)


    _ElementMap = {

    }
    _AttributeMap = {
        __primary_position.name() : __primary_position,
        __root.name() : __root,
        __lemma.name() : __lemma,
        __secondary_position.name() : __secondary_position
    }
Namespace.addCategoryObject('typeBinding', u'StemType', StemType)


sentence = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'sentence'), SentenceType)
Namespace.addCategoryObject('elementBinding', sentence.name().localName(), sentence)



WordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'stem'), StemType, scope=WordType))

WordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'suffixes'), CTD_ANON, scope=WordType))
WordType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(WordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'stem')), min_occurs=1L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(WordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'suffixes')), min_occurs=1L, max_occurs=1L)
)
WordType._ContentModel = pyxb.binding.content.ParticleModel(WordType._GroupModel, min_occurs=1, max_occurs=1)



SentenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'word'), WordType, scope=SentenceType))
SentenceType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SentenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'word')), min_occurs=1L, max_occurs=None)
)
SentenceType._ContentModel = pyxb.binding.content.ParticleModel(SentenceType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'suffix'), SuffixType, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'suffix')), min_occurs=1, max_occurs=None)
)
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)
