from trnltk.morphology.learner.controller.indexcontroller import IndexController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext
from trnltk.morphology.learner.view.Indexview import IndexView

class ContextRootHandler(SessionAwareRequestHandler):
    def get(self):
        return self.redirect("/index")

class IndexHandler(SessionAwareRequestHandler):
    def get(self):
        index_view = IndexView()
        dbmanager = applicationcontext.application_context_instance.dbmanager

        index_controller = IndexController(index_view, dbmanager)

        index_controller.go_home()

        view_context = index_view.get_template_context()

        self.render_response("indextemplate.jinja2", **view_context)
