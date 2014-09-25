'''/template2'''
from myui.controllers import BaseHandler

class Handler(BaseHandler):
    def get(self):
        self.write('test')
