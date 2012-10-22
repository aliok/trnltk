from bson.objectid import ObjectId
from trnltk.morphology.learner.controller.parseresultcorrectmarkercontroller import ParseResultCorrectMarkerController
from trnltk.morphology.learner.controller.sessionmanager import SessionManager
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext

class ParseResultCorrectMarkerHandler(SessionAwareRequestHandler):
    def get(self):

        # check word id
        param_word_id = self.request.get('wordId')

        assert param_word_id


        # get parse result
        param_parse_result_uuid = self.request.get('parseResultUUID')
        if not param_parse_result_uuid:
            raise Exception(u"Missing parameter : parseResultUUID")

        word_id = ObjectId(param_word_id)

        # run controller, which will save the result in the db
        dbmanager = applicationcontext.application_context_instance.dbmanager
        sessionmanager = SessionManager(self.session)
        controller = ParseResultCorrectMarkerController(dbmanager, sessionmanager)
        controller.save_parse_result_for_word(word_id, param_parse_result_uuid)


        # get word index to go from request
        param_next_word_id = self.request.get('nextWordId') or param_word_id
        next_word_id = ObjectId(param_next_word_id)


        # redirect to "/nextNonParsedWord?corpusId=xx&wordIndex=yy"
        return self.redirect("/learner?wordId={}".format(next_word_id))


