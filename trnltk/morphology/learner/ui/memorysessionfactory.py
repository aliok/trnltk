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