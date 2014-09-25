from myui.controllers import BaseHandler

class params:
    route='/template'
    pass

class Handler(BaseHandler):
    def get(self):
        self.write('test')
