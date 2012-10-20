from bson.objectid import ObjectId
from trnltk.morphology.learner.controller.learnercontroller import LearnerController
from trnltk.morphology.learner.controller.sessionmanager import SessionManager
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui.applicationcontext import application_context_instance
from trnltk.morphology.learner.ui.learnerview import LearnerView

class LearnerHandler(SessionAwareRequestHandler):
    def get(self):
        param_corpus_id = self.request.get('corpusId')
        param_word_index = self.request.get('wordIndex')

        if not param_corpus_id:
            self.redirect('/index')

        param_word_index = int(param_word_index) if param_word_index else 0

        self.go_to_word(param_corpus_id, param_word_index)

    def go_to_word(self, str_corpus_id, current_word_index):
        learnerview = LearnerView()
        dbmanager = application_context_instance.dbmanager
        sessionmanager = SessionManager(self.session)
        contextless_morphological_parser = application_context_instance.contextless_morphological_parser
        likelihood_calculator = application_context_instance.likelihood_calculator
        parse_context_creator = application_context_instance.parse_context_creator

        controller = LearnerController(learnerview, dbmanager, sessionmanager, contextless_morphological_parser, likelihood_calculator, parse_context_creator)

        corpus_id = ObjectId(str_corpus_id)

        controller.go_to_word(corpus_id, current_word_index)

        view_context = learnerview.get_template_context()

        print view_context

        self.render_response("learnerviewtemplate.html", **view_context)
