'''/katherine/?([0-9]+)'''
from myui.controllers import BaseHandler

class Handler(BaseHandler):
    def get(self, i):
        self.write('kat is awesome: {0}'.format(str(i)))
