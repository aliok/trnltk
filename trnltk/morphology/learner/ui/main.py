# coding=utf-8
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
from trnltk.morphology.learner.requesthandler.corpuscreatorhandler import CorpusCreatorHandler
from trnltk.morphology.learner.requesthandler.corpusreaderhandler import CorpusReaderHandler
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
    ('/corpusReader', CorpusReaderHandler),
    (r'/resources/(.+)', StaticFileHandler),
    ('/', ContextRootHandler)
], debug=True, config=config)

def main():
    from paste import httpserver

    httpserver.serve(app, host='localhost', port='8080')

if __name__ == '__main__':
    main()