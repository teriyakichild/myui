import os, sys, inspect
import re
from importlib import import_module
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from types import ModuleType


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
    tornado.options.define("plugins", default="", help="comma-separated list of plugins that should be loaded")
    tornado.options.define("plugin_opts", default={}, help="Dictionary of plugin specific options")
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
         plugin_opts=tornado.options.options.plugin_opts
    )
    return settings


def run_server(handlers, settings):
    http_server = tornado.httpserver.HTTPServer(Application(handlers,settings))
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

def create_tables(get_settings=True):
    if get_settings:
        settings = parse_options()

    # Generating list of models
    models = {}
    cursors = {}
    for plugin in tornado.options.options.plugins.split(','):
        print 'Loading models.. ({0})'.format(plugin)
        list_of_models = generate_models(plugin)
        for model in list_of_models:
            models[model] = import_module('{0}.models.{1}'.format(plugin, model))
            try:
                cursors[model] = models[model].create_tables()
            except:
                print 'Failed to create tables for module'
            else:
                print 'Model[{0}] created'.format(model)
    return cursors

def generate_models(plugin):
    models = import_module('{0}.models'.format(plugin))
    ret = [each for each in models.__all__]
    return ret

def generate_controllers(plugin):
    controllers = import_module('{0}.controllers'.format(plugin))
    ret = [each for each in controllers.__all__]
    return ret

def main():
    settings = parse_options()

    controllers = {}
    print 'Loading controllers..'
    for plugin in tornado.options.options.plugins.split(','):
        list_of_controllers = generate_controllers(plugin)
        for controller in list_of_controllers:
            controllers[controller] = import_module('{0}.controllers.{1}'.format(plugin, controller))
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
