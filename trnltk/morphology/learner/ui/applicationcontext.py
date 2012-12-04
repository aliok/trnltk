# coding=utf-8
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

        self.contextful_morphological_parser = ContextfulMorphologicalParserFactory.create(master_dictionary_path, ngram_collection_map)
        self.contextful_morphological_parser.build_indexes()

        self.dbmanager = DbManager(mongodb_connection)
        self.dbmanager.build_indexes()

        self.parse_context_creator = ParseContextCreator(self.contextful_morphological_parser._contextless_parser)

        self.sessions = {}


application_context_instance = ApplicationContext()