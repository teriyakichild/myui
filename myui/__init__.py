import os, sys, inspect
import re
from importlib import import_module
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options


class Application(tornado.web.Application):
    def __init__(self,handlers,settings):
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    pass

def parse_options():
    tornado.options.define("port", default="3000", help="webui port")
    tornado.options.define("config_file", default="/etc/myui.conf", help="webui port")
    tornado.options.parse_command_line()

    tornado.options.define("app_title", default='My-UI')
    tornado.options.define("login_url", default='/login')
    tornado.options.define("controller_dir", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'controllers'), help="controllers directory")
    tornado.options.define("model_dir", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'models'), help="models directory")

    tornado.options.define("template_path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates'), help="templates directory name")
    tornado.options.define("static_path", default=os.path.join(os.path.dirname(os.path.realpath(__file__)),'static'), help="static files dirctory name")
    tornado.options.define("cookie_secret", default='this is my secret.  you dont know it.')
    tornado.options.define("debug", default=True, help="enable tornado debug mode")

    tornado.options.parse_config_file(tornado.options.options.config_file)
    tornado.options.parse_command_line()

    settings = dict(
         login_url=tornado.options.options.login_url,
         app_title=tornado.options.options.app_title,
         template_path=tornado.options.options.template_path,
         static_path=tornado.options.options.static_path,
         cookie_secret=tornado.options.options.cookie_secret,
         debug=tornado.options.options.debug,
    )
    return settings


def run_server(handlers, settings):
    http_server = tornado.httpserver.HTTPServer(Application(handlers,settings))
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

def create_tables(get_settings=True):
    if get_settings:
        settings = parse_options()

    if tornado.options.options.model_dir not in sys.path:
        sys.path.insert(0, tornado.options.options.model_dir)

    # Generating list of models
    print 'Loading models.. ({0})'.format(tornado.options.options.model_dir)
    files = os.walk(tornado.options.options.model_dir).next()[2]
    dont_include = [ '__init__.py', '__init__.pyc' ]
    list_of_models = [ re.sub('.py$', '', x) for x in filter(lambda c: c not in dont_include and re.search('.py$',c), files) ]

    # Load models
    models = {}
    cursors = {}
    for model in list_of_models:
        models[model] = import_module(model, 'myui.models')
        try:
            cursors[model] = models[model].create_tables()
        except:
            print 'Failed to create tables for module'
        else:
            print 'Model[{0}] created'.format(model)
    return cursors

def main():
    settings = parse_options()

    # Add controller_dir to path
    if tornado.options.options.controller_dir not in sys.path:
        sys.path.insert(0, tornado.options.options.controller_dir)

    # Generating list of controllers
    print 'Loading controllers.. ({0})'.format(tornado.options.options.controller_dir)
    files = os.walk(tornado.options.options.controller_dir).next()[2]
    dont_include = [ '__init__.py', '__init__.pyc' ]
    list_of_controllers = [ re.sub('.py$', '', x) for x in filter(lambda c: c not in dont_include and re.search('.py$',c), files) ]

    # Load controllers
    controllers = {}
    for controller in list_of_controllers:
        controllers[controller] = import_module(controller, 'myui.controllers')
        print 'Controller[{0}] loaded'.format(controller)

    # Build handlers
    print 'Adding routes..'
    handlers = []
    for controller in controllers:
        c = controllers[controller]
        if isinstance(c.params.route, basestring):
            handlers.append((c.params.route, c.Handler))
        else:
            for uri_string in c.params.route:
               handlers.append((uri_string, c.Handler))


    # Start tornado server
    run_server(handlers, settings)

if __name__ == '__main__':
    main()
