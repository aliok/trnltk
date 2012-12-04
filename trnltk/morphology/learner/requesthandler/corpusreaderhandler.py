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
from trnltk.morphology.learner.controller.corpusreadercontroller import CorpusReaderController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext
from trnltk.morphology.learner.view.corpusreaderview import CorpusReaderView

class CorpusReaderHandler(SessionAwareRequestHandler):
    def get(self):
        param_corpus_id = self.request.get('corpusId')

        assert param_corpus_id

        corpus_reader_view = CorpusReaderView()
        dbmanager = applicationcontext.application_context_instance.dbmanager

        self.controller = CorpusReaderController(corpus_reader_view, dbmanager)

        self.controller.read_corpus(param_corpus_id)

        view_context = corpus_reader_view.get_template_context()

        self.render_response("corpusreadertemplate.jinja2", **view_context)