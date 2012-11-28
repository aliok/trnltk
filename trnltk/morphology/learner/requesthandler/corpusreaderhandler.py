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