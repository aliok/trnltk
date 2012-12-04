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
from trnltk.morphology.learner.controller.indexcontroller import IndexController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext
from trnltk.morphology.learner.view.indexview import IndexView

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
