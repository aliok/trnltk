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
class CorpusCreatorView(object):
    def __init__(self):
        self._context = {}

    def get_template_context(self):
        return self._context

    def set_corpus_name(self, corpus_name):
        self._context['corpus_name'] = corpus_name

    def set_corpus_name_not_unique(self):
        self.set_error("Please select a unique corpus name. Provided name already exists.")

    def set_success(self):
        self._context['error_occurred'] = False

    def set_error(self, param):
        self._context['error_occurred'] = True
        self._context['error_msg'] = param