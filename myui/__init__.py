import os, sys, inspect
import re
from importlib import import_module
from myui.controllers import run_server

def main():
    controller_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'controllers')
    if controller_dir not in sys.path:
        sys.path.insert(0, controller_dir)

    print 'Loading controllers.. ({0})'.format(controller_dir)
    files = os.walk(controller_dir).next()[2]
    dont_include = [ '__init__.py', '__init__.pyc' ]
    list_of_controllers = [ re.sub('.py$', '', x) for x in filter(lambda c: c not in dont_include and re.search('.py$',c), files) ]

    print list_of_controllers
    controllers = {}
    for controller in list_of_controllers:
        controllers[controller] = import_module(controller, 'myui.controllers')
        print 'Controller[{0}] loaded'.format(controller)

    handlers = []
    for controller in controllers:
        c = controllers[controller]
        uri_string = c.__doc__
        handlers.append((uri_string, c.Handler))

    run_server(handlers)

if __name__ == '__main__':
    main()
