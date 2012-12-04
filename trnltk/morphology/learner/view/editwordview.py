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
class EditWordView(object):
    def __init__(self):
        self._context = {}

    def get_template_context(self):
        return self._context

    def set_current_word(self, word):
        self._context['current_word_id'] = word['_id']
        self._context['current_surface'] = word['surface']

    def set_next_word_id(self, next_word_id):
        self._context['next_word_id'] = next_word_id
