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

        context = {
            'leading_context_sentence' : u'Bilim insanları, balinadan dev ahtapota kadar',
            'target_surface' : u'birçok',
            'following_context_sentence' : u'canlının gözün sahibi olacağını öne sürdü.',

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