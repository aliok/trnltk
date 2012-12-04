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
from webapp2_extras import sessions
from webapp2_extras.sessions import CustomBackendSessionFactory
from trnltk.morphology.learner.ui.applicationcontext import application_context_instance

class MemorySessionFactory(CustomBackendSessionFactory):

    def _get_by_sid(self, sid):
        if self._is_valid_sid(sid):
            data = application_context_instance.sessions.get(sid)
            if data is not None:
                self.sid = sid
                return sessions.SessionDict(self, data=data)

        self.sid = self._get_new_sid()
        return sessions.SessionDict(self, new=True)

    def save_session(self, response):
        if self.session is None or not self.session.modified:
            return

        application_context_instance.sessions[self.sid] = dict(self.session)
        self.session_store.save_secure_cookie(
            response, self.name, {'_sid': self.sid}, **self.session_args)