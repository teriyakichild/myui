from myui.controllers import BaseHandler


class params:
    route='/template2'
    pass

class Handler(BaseHandler):
    def get(self):
        self.render('template2.j2')
