from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler

class ContextRootHandler(SessionAwareRequestHandler):
    def get(self):
        return self.redirect("/index")

class IndexHandler(SessionAwareRequestHandler):
    def get(self):
        self.render_response("indextemplate.html", **{})
