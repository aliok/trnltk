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
import webapp2
from webapp2_extras import jinja2, sessions
from trnltk.morphology.learner.ui.memorysessionfactory import MemorySessionFactory

class SessionAwareRequestHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def session(self):
        # this would be different for GAE
        return self.session_store.get_session(name='session_id', factory=MemorySessionFactory)

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def dispatch(self):
        try:
            super(SessionAwareRequestHandler, self).dispatch()
        finally:
            # Save the session after each request
            self.session_store.save_sessions(self.response)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        # since the output is very small (<1MB), skip the streaming in template renderer?
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
