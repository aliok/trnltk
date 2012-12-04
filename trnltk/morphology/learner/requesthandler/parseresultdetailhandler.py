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

        self.render_response("parseresultdetailtemplate.jinja2", **{'calculation_context' : calculation_context, 'parse_result_uuid' : param_parse_result_uuid})