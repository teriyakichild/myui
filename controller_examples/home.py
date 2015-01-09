from myui import BaseHandler
import tornado.web


class params:
    route='/'
    pass

class Handler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.write('home')
