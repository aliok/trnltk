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
from bson.objectid import ObjectId
from trnltk.morphology.learner.controller.learnercontroller import LearnerController
from trnltk.morphology.learner.controller.sessionmanager import SessionManager
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui.applicationcontext import application_context_instance
from trnltk.morphology.learner.view.learnerview import LearnerView

class LearnerHandler(SessionAwareRequestHandler):
    def get(self):
        param_word_id = self.request.get('wordId')

        if not param_word_id:
            self.redirect('/index')

        self.go_to_word(ObjectId(param_word_id))

    def go_to_word(self, word_id):
        learnerview = LearnerView()
        dbmanager = application_context_instance.dbmanager
        sessionmanager = SessionManager(self.session)
        contextful_morphological_parser = application_context_instance.contextful_morphological_parser
        parse_context_creator = application_context_instance.parse_context_creator

        controller = LearnerController(learnerview, dbmanager, sessionmanager, contextful_morphological_parser, parse_context_creator)

        controller.go_to_word(word_id)

        view_context = learnerview.get_template_context()

        self.render_response("learnerviewtemplate.jinja2", **view_context)
