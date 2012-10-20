from trnltk.morphology.learner.requesthandler.sessionawarerequesthandler import SessionAwareRequestHandler

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

        print self.session[parseResultUUID]

        # run controller, which will save the result in the db
        # check if the parse result belongs to the word in given index!

        # get word index to go from request
        param_next_word_index = self.request.get('nextWordIndex') or 0

        # redirect to "/nextNonParsedWord?corpusId=xx&wordIndex=yy"
        return self.redirect("/learner?corpusId={}&wordIndex={}".format(param_corpus_id, param_next_word_index))


