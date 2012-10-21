from bson.objectid import ObjectId
from trnltk.morphology.learner.controller.parseresultcorrectmarkercontroller import ParseResultCorrectMarkerController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext

class ParseResultCorrectMarkerHandler(SessionAwareRequestHandler):
    def get(self):

        # check word id
        param_word_id = self.request.get('wordId')

        assert param_word_id


        # get parse result
        parseResultUUID = self.request.get('parseResultUUID')
        if not parseResultUUID:
            raise Exception(u"No parseResultUUID found for {}".format(parseResultUUID))

        parse_result = self.session[parseResultUUID]

        word_id = ObjectId(param_word_id)

        # run controller, which will save the result in the db
        dbmanager = applicationcontext.application_context_instance.dbmanager
        controller = ParseResultCorrectMarkerController(dbmanager)
        controller.save_parse_result_for_word(word_id, parse_result)


        # get word index to go from request
        param_next_word_id = self.request.get('nextWordId') or param_word_id
        next_word_id = ObjectId(param_next_word_id)


        # redirect to "/nextNonParsedWord?corpusId=xx&wordIndex=yy"
        return self.redirect("/learner?wordId={}".format(next_word_id))


