# coding=utf-8
import os
import pymongo
from trnltk.morphology.contextful.parser.contexfulmorphologicalparser import ContextfulMorphologicalParserFactory
from trnltk.morphology.learner.controller.learnercontroller import ParseContextCreator
from trnltk.morphology.learner.dbmanager.dbmanager import DbManager

class ApplicationContext(object):
    # some parameters
    PARSESET_INDEX = "999"      # this is the id of the knowledge ngrams collections
    DB_HOST = '127.0.0.1'

    def __init__(self):
        master_dictionary_path = os.path.join(os.path.dirname(__file__), '../../../resources/master_dictionary.txt')

        mongodb_connection = pymongo.Connection(host=ApplicationContext.DB_HOST)
        ngram_collection_map = {
            1: mongodb_connection['trnltk']['wordUnigrams{}'.format(ApplicationContext.PARSESET_INDEX)],
            2: mongodb_connection['trnltk']['wordBigrams{}'.format(ApplicationContext.PARSESET_INDEX)],
            3: mongodb_connection['trnltk']['wordTrigrams{}'.format(ApplicationContext.PARSESET_INDEX)]
        }

        self.contextful_parser = ContextfulMorphologicalParserFactory.create(master_dictionary_path, ngram_collection_map)

        self.dbmanager = DbManager(mongodb_connection)
        self.dbmanager.build_indexes()

        self.parse_context_creator = ParseContextCreator(self.contextful_parser._contextless_parser)

        self.sessions = {}


application_context_instance = ApplicationContext()