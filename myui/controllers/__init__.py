import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

class Application(tornado.web.Application):
    def __init__(self,handlers,settings):
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass

def run_server(handlers):
    tornado.options.define("port", default="3000", help="webui port")
    tornado.options.parse_command_line()

    tornado.options.define("app_title", default='My-UI')
    tornado.options.define("template_path", default='templates', help="templates directory name")
    tornado.options.define("static_path", default='static', help="static files dirctory name")
    tornado.options.define("cookie_secret", default='this is my secret.  you dont know it.')
    tornado.options.define("debug", default=True, help="enable tornado debug mode")

    tornado.options.parse_config_file('/etc/myui.conf')
    tornado.options.parse_command_line()

    settings = dict(
         app_title=tornado.options.options.app_title,
         template_path=tornado.options.options.template_path,
         static_path=tornado.options.options.static_path,
         cookie_secret=tornado.options.options.cookie_secret,
         debug=tornado.options.options.debug,
    )

    http_server = tornado.httpserver.HTTPServer(Application(handlers,settings))
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()
