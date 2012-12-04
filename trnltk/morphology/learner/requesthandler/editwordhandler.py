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
from trnltk.morphology.learner.controller.editwordcontroller import EditWordController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext
from trnltk.morphology.learner.view.editwordview import EditWordView

class EditWordHandler(SessionAwareRequestHandler):
    def get(self):
        # check word id
        param_word_id = self.request.get('wordId')
        param_next_word_id = self.request.get('nextWordId')

        assert param_word_id and param_next_word_id

        action = self.request.get('action')
        surface_first_part = self.request.get('surfaceFirstPart')
        surface_second_part = self.request.get('surfaceSecondPart')

        word_id = ObjectId(param_word_id)
        next_word_id = ObjectId(param_next_word_id)

        edit_word_view = EditWordView()
        dbmanager = applicationcontext.application_context_instance.dbmanager
        controller = EditWordController(edit_word_view, dbmanager)

        if not action:
            controller.go_to_word(word_id, next_word_id)

            view_context = edit_word_view.get_template_context()

            self.render_response("editwordtemplate.jinja2", **view_context)
        elif action == 'update':
            controller.update_word(word_id, surface_first_part, surface_second_part)
            return self.redirect("/learner?wordId={}".format(word_id))
        elif action == 'delete':
            corpus_alive = controller.delete_word(word_id)
            if not corpus_alive:
                return self.redirect("/index")
            else:
                return self.redirect("/learner?wordId={}".format(next_word_id))
        else:
            raise Exception('Invalid action!')

    def post(self):
        self.get()