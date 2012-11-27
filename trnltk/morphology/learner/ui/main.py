# coding=utf-8
import webapp2
from trnltk.morphology.learner.requesthandler.corpuscreatorhandler import CorpusCreatorHandler
from trnltk.morphology.learner.requesthandler.editwordhandler import EditWordHandler
from trnltk.morphology.learner.requesthandler.indexhandler import IndexHandler, ContextRootHandler
from trnltk.morphology.learner.requesthandler.learnerhandler import LearnerHandler
from trnltk.morphology.learner.requesthandler.parseresultcorrectmarkerhandler import ParseResultCorrectMarkerHandler
from trnltk.morphology.learner.requesthandler.parseresultdetailhandler import ParseResultDetailHandler
from trnltk.morphology.learner.requesthandler.staticfilehandler import StaticFileHandler

config = {
    'webapp2_extras.sessions': {'secret_key': 'trnltk-learner-ui-secret-cookie-key'}
}

app = webapp2.WSGIApplication([
    ('/index', IndexHandler),
    ('/corpusCreator', CorpusCreatorHandler),
    ('/learner', LearnerHandler),
    ('/markParseResultAsCorrect', ParseResultCorrectMarkerHandler),
    ('/parseResultDetail', ParseResultDetailHandler),
    ('/editWord', EditWordHandler),
    (r'/resources/(.+)', StaticFileHandler),
    ('/', ContextRootHandler)
], debug=True, config=config)

def main():
    from paste import httpserver

    httpserver.serve(app, host='localhost', port='8080')

if __name__ == '__main__':
    main()