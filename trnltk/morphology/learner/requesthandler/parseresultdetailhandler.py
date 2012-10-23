from trnltk.morphology.learner.controller.parseresultdetailcontroller import ParseResultDetailController
from trnltk.morphology.learner.controller.sessionmanager import SessionManager
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler

class ParseResultDetailHandler(SessionAwareRequestHandler):
    def get(self):

        param_parse_result_uuid = self.request.get('parseResultUUID')
        if not param_parse_result_uuid:
            raise Exception(u"Missing parameter : parseResultUUID")

        sessionmanager = SessionManager(self.session)
        controller = ParseResultDetailController(sessionmanager)
        calculation_context = controller.get_calculation_context(param_parse_result_uuid)

        self.render_response("parseresultdetailtemplate.html", **{'calculation_context' : calculation_context, 'parse_result_uuid' : param_parse_result_uuid})