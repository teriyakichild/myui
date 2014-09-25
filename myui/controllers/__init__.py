import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

class Application(tornado.web.Application):
    def __init__(self,handlers,settings):
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass

def run_server(handlers):
    print handlers

    tornado.options.define("port", default="3000", help="webui port")
    tornado.options.parse_command_line()

    settings = dict(
         app_title='testing',
         template_path='/templates',
         static_path='/static',
         cookie_secret='asdfasdfasdfasdfasdf',
         debug=True,
    )

    http_server = tornado.httpserver.HTTPServer(Application(handlers,settings))
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
