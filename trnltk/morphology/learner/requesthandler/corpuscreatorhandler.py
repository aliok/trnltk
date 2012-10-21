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

        self.render_response("corpuscreatortemplate.html", **view_context)