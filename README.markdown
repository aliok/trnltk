PROJECT MOVED
=============
This project is first ported to [Java](https://github.com/aliok/trnltk-java)
and then merged into Zemberek project ( [code](https://code.google.com/p/zemberek3/), [Turkish Wikipedia Article](http://tr.wikipedia.org/wiki/Zemberek_(yaz%C4%B1l%C4%B1m) ).
Zemberek is an NLP project which has been used in the industry for several years. It is used in products such as OpenOffice.

Current codebase for TRNLTK is kept, for people who wants to work on/with a Python Turkish morphologic parser.

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

Turkish Natural Language Toolkit
================================

This project will try to provide a toolkit for computer linguistic work for Turkish.

Some terms used in documentation and code
-----------------------------------------

**surface**: Full word including the root and suffixes

**root** : The root of a word. Root atomic part.

**derivation** : Deriving a new wo

**inflection** : Conjugating a word with a person agreement / possession / tense etc.

**suffix form** : Form of a suffix. For example, suffix 'Progressive' has 2 suffix forms; '-iyor' and '-makta'

**stem** : Root + derivations. Doesn't include the inflections

**syntactic category** : Verb, Noun, Adjective etc.

**inflectional suffix** : A suffix that doesn't change stem nor the syntactic category of a surface

**derivational suffix** : A suffix that changes the stem and might change the syntactic category of a surface

**morpheme** : Elements of a surface; stem and suffixes

**lemma** : The root text that can be found in a dictionary

**lexeme** : Lemma + Syntactic category of the lemma

**morphology** : How a surface is constructed and how can it be extracted to morphemes

**morphotactics** : Rules when can a suffix can be applied. For example "Progressive suffix can only be applied to a Verb, and it can't be applied to a surface which has Progressive suffix already"

**ortographics** : Rules of phonetics. For example the rules for voicing (kitap+a --> kitaba), devoicing (kitap+cı --> kitapçı), vowel drop (omuz+u --> omzu), etc.

### for "yüzücülere":
surface : yüzücülere

root : yüz

stem : yüzücü

syntactic category of root : Verb

syntactic category of surface : Noun

suffixes and suffix forms:
 * derivational suffix 'Agentive' with form '-cü'
 * inflectional suffix '3rd person plural agreement' with form '-ler'
 * inflectional suffix 'Dativ' with form '-e'

morphemes:
 * root 'yüz'
 * derivational suffix 'Agentive' with form '-cü'
 * inflectional suffix '3rd person plural agreement' with form '-ler'
 * inflectional suffix 'Dativ' with form '-e'

lemma : yüz

lexeme : yüz + Verb

### for 'kitaba':

surface : kitaba

root : kitab

stem : kitab (or kitap, doesn't matter)

syntactic category of root : Noun

syntactic category of surface : Noun

suffixes and suffix forms:
 * inflectional suffix 'Dativ' with form '-a'

morphemes:
 * root 'kitab'
 * inflectional suffix 'Dativ' with form '-a'

lemma : kitap

lexeme : kitap + Noun


Plan
-----------------------

1. [In Progress] A contextless morphological parser to extract roots and suffixes out of surfaces
2. A contextless morphological generator that can generate surfaces from roots and suffixes by choosing the correct suffix form
3. A playground with a data set that provides
       * Concordance for surfaces
       * Concordance for roots
       * Concordance for lexemes
       * Concordance for transition words
       * Statistics for words, roots and suffixes
       * ...
4. A context dependent morphological parser that uses N-Grams for determining the correct parse result among several results
5. A context dependent morphological generator that uses N-Grams for determining the correct suffix form among several forms
6. A rule based and statistical lexical category determining tool for sentences


1. Contextless Morphological Parser
------------------------------------

A finite state machine is used for parsing surfaces. Nodes with different states of words and edges as suffixes.

As of October 2012, [this](https://github.com/aliok/trnltk/raw/master/suffixGraphExtended_20121010.png) graph is used to parse surfaces.
That graph is drawn by [this script](https://github.com/aliok/trnltk/bin/suffixgraphplotter.py) with the following command

    suffixgraphplotter.py E /home/ali/Desktop/suffixGraphX.png


The format of the image is based on extension. So, for a more interactive image you can use dot:

    suffixgraphplotter.py E /home/ali/Desktop/suffixGraphX.png

### Why another parsing tool and why FSM?

I've inspected other other approaches and I saw that tracking the problems were very hard with them. For example, one approach is creating a suffix graph
by defining what suffix can come after other suffix. But with that approach it is impossible to have an overview of the graph, since there would
be thousands of nodes and edges.

Phonetic rules and implementation is copied from open-source java library [Zemberek3](http://code.google.com/p/zemberek3/)

### How it is tested?

There are thousands of parsing unit tests. Plus, I use the treebank from METU-Sabanci, but is closed-source. Unfortunately, its license doesn't allow
anyone to publish any portion of the treebank, thus I only test the parser against it in my local environment.



