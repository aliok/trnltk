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
from trnltk.morphology.learner.controller.corpuscreatorcontroller import CorpusCreatorController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext
from trnltk.morphology.learner.view.corpuscreatorview import CorpusCreatorView
from trnltk.tokenizer.texttokenizer import TextTokenizer

class CorpusCreatorHandler(SessionAwareRequestHandler):
    def post(self):

        param_corpus_name = self.request.get('corpusName')
        param_corpus_desc = self.request.get('corpusDescription')
        param_corpus_content = self.request.get('corpusContent')

        assert param_corpus_name and param_corpus_desc and param_corpus_content

        corpus_creator_view = CorpusCreatorView()
        dbmanager = applicationcontext.application_context_instance.dbmanager
        tokenizer = TextTokenizer()

        self.controller = CorpusCreatorController(corpus_creator_view, dbmanager, tokenizer)

        self.controller.create_corpus(param_corpus_name, param_corpus_desc, param_corpus_content)

        view_context = corpus_creator_view.get_template_context()

        self.render_response("corpuscreatortemplate.jinja2", **view_context)