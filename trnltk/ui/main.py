# coding=utf-8
import webapp2
from webapp2_extras import jinja2
from trnltk.ui.staticfilehandler import StaticFileHandler

class Main(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


    def get(self):

        parse_result_container_1 = {
            'likelihood_percentage_color' : u'info',
            'likelihood_percentage' : u'78',
            'likelihood_value_color' : u'success',
            'likelihood_value' : 0.501211,
            'formatted_parse_result' : u'masa+Noun+A3sg+Pnon+Dat'
        }

        parse_result_container_2 = {
            'likelihood_percentage_color' : u'warning',
            'likelihood_percentage' : u'22',
            'likelihood_value_color' : u'warning',
            'likelihood_value' : 0.140011,
            'formatted_parse_result' : u'masay+Noun+A3sg+Pnon+Dat'
        }

        parse_result_containers = [parse_result_container_1, parse_result_container_2]


        leading_context_word_1 = {'id':'1', 'surface' : u'Bilim', 'parsed':False}
        leading_context_word_2 = {'id':'2', 'surface' : u'insanları', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        leading_context_word_3 = {'id':'3', 'surface' : u',', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        leading_context_word_4 = {'id':'4', 'surface' : u'balinadan', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        leading_context_word_5 = {'id':'5', 'surface' : u'dev', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        leading_context_word_6 = {'id':'6', 'surface' : u'ahtapota', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        leading_context_word_7 = {'id':'7', 'surface' : u'kadar', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}


        leading_context_words = [leading_context_word_1, leading_context_word_2, leading_context_word_3, leading_context_word_4,
                                 leading_context_word_5, leading_context_word_6, leading_context_word_7]

        following_context_word_1 = {'id':'1', 'surface' : u'canlının', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        following_context_word_2 = {'id':'2', 'surface' : u'gözün', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        following_context_word_3 = {'id':'3', 'surface' : u'sahibi', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        following_context_word_4 = {'id':'4', 'surface' : u'olacağını', 'parsed':False}
        following_context_word_5 = {'id':'5', 'surface' : u'öne', 'parsed':True, 'parse_result' : 'X+Y+Z+Abc'}
        following_context_word_6 = {'id':'6', 'surface' : u'sürdü', 'parsed':False}
        following_context_word_7 = {'id':'7', 'surface' : u'.', 'parse_result' : 'X+Y+Z+Abc'}

        following_context_words = [following_context_word_1, following_context_word_2, following_context_word_3, following_context_word_4,
                                   following_context_word_5, following_context_word_6, following_context_word_7]

        previous_sentence = {'id' : '123123111', 'str' : u'Komisyon, Facebook ve Flickr sayfalarında, yapılan analizler hakkında bilgi paylaştı.'}
        next_sentence = {'id' : '123123111', 'str' : u'İlk günden akıllara gelen en büyük aday kılıçbalığıydı.'}

        context = {
            'leading_context_words' : leading_context_words,
            'following_context_words' : following_context_words,
            'target_surface' : u'birçok',
            'previous_sentence' : previous_sentence,
            'next_sentence' : next_sentence,

            'index' : 3,
            'count_not_parsed' : 100,
            'style_class_previous_button' : u'disabled',

            'parse_result_containers': parse_result_containers
        }

        self.render_response('main_template.html', **context)

app = webapp2.WSGIApplication([
    ('/', Main),
    (r'/resources/(.+)', StaticFileHandler)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='localhost', port='8080')

if __name__ == '__main__':
    main()