class BaseRenderer(object):

    def paths(self):
        raise NotImplementedError

    def render_path(self, path=None, view=None):
        raise NotImplementedError

    def generate(self):
        for path in self.paths():
            self.render_path(path)
