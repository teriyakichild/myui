from myui.controllers import BaseHandler
import tornado.web


class params:
    route='/example'
    pass

class Handler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render('example.html')
