Turkish Natural Language Toolkit
================================

This project will try to provide a toolkit for computer linguistic work for Turkish. Here is the plan:

1. [In Progress] A context free word parser to extract roots and suffixes from the words
2. A context free word generator that can generate words from roots and suffixes by choosing the correct suffix form
3. A playground with a data set that provides
       * Concordance for words
       * Concordance for stems
       * Statistics for words, stems and suffixes
       * ...
4. A context sensitive parser that uses N-Grams for determining the correct parse result among several results
5. A context sensitive generator that uses N-Grams for determining the correct suffix form among several forms
6. A rule based and statistical lexical category determining tool for sentences


1. Context Free Parser
-------------------

A finite state machine is used for parsing the words. Nodes with different states of words and edges as suffixes.

As of June 2012, [this](https://github.com/aliok/trnltk/raw/master/suffixGraphExtended_20120628.png) graph is used to parse words.
That graph is drawn by [this script](https://github.com/aliok/trnltk/bin/suffixgraphplotter.py) with the following command

    suffixgraphplotter.py E /home/ali/Desktop/suffixGraphX.png


The format of the image is based on extension. So, for a more interactive image you can use dot:

    suffixgraphplotter.py E /home/ali/Desktop/suffixGraphX.png

### Why another parsing tool and why FSM?

I've inspected other other approaches and I saw that tracking the problems were very hard with them. For example, one approach is creating a suffix graph
by defining what suffix can come after other suffix. But with that approach it is impossible to have an overview of the graph, since there would
be thousands of nodes and edges.

Phonetic rules and implementation is copied from open-source java library [Zemberek3]{http://code.google.com/p/zemberek3/}

### How it is tested?

There are thousands of parsing unit tests. Plus, I use the treebank from METU-Sabanci, but is closed-source. Unfortunately, its license doesn't allow
anyone to publish any portion of the treebank, thus I only test the parser against it in my local environment.



