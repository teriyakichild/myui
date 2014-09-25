from myui.controllers import BaseHandler


class params:
    route='/katherine/?([0-9]+)'
    pass

class Handler(BaseHandler):
    def get(self, i):
        self.write('kat is awesome: {0}'.format(str(i)))
