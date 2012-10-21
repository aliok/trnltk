from bson.objectid import ObjectId
from trnltk.morphology.learner.controller.parseresultcorrectmarkercontroller import ParseResultCorrectMarkerController
from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler
from trnltk.morphology.learner.ui import applicationcontext

class ParseResultCorrectMarkerHandler(SessionAwareRequestHandler):
    def get(self):

        # check corpus and word index
        param_corpus_id = self.request.get('corpusId')
        param_word_index = self.request.get('wordIndex')

        assert param_corpus_id and param_word_index is not None


        # get parse result
        parseResultUUID = self.request.get('parseResultUUID')
        if not parseResultUUID:
            raise Exception(u"No parseResultUUID found for {}".format(parseResultUUID))

        parse_result = self.session[parseResultUUID]

        corpus_id = ObjectId(param_corpus_id)
        word_index = int(param_word_index)

        # run controller, which will save the result in the db
        dbmanager = applicationcontext.application_context_instance.dbmanager
        controller = ParseResultCorrectMarkerController(dbmanager)
        controller.save_parse_result_for_word(corpus_id, word_index, parse_result)


        # get word index to go from request
        param_next_word_index = self.request.get('nextWordIndex') or 0


        # redirect to "/nextNonParsedWord?corpusId=xx&wordIndex=yy"
        return self.redirect("/learner?corpusId={}&wordIndex={}".format(param_corpus_id, param_next_word_index))


