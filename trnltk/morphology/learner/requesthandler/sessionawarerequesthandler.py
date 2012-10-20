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
        # TODO: how about streaming in template renderer?
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)
