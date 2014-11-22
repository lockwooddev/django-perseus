from django.template import Context, Template


class TestStaticTag:

    def setup(self):
        self.ctx = Context({})

    def test_static_tag_startswith(self, settings):
        settings.RENDER_STATIC = True
        template = Template("{% load django_perseus_tags %}{% static 'css/styles.css' %}")
        assert template.render(self.ctx) == 'css/styles.css'

    def test_static_tag_setting_disabled(self, settings):
        settings.RENDER_STATIC = False
        template = Template("{% load django_perseus_tags %}{% static 'css/styles.css' %}")
        assert template.render(self.ctx) == '/css/styles.css'

    def test_static_tag_relative_url(self, settings):
        settings.RENDER_STATIC = True
        settings.STATIC_URL = ''
        template = Template("{% load django_perseus_tags %}{% static 'css/styles.css' %}")
        assert template.render(self.ctx) == 'css/styles.css'


class TestUrlTag:

    def setup(self):
        self.ctx = Context({})

    def test_url_tag_index(self, settings):
        settings.RENDER_STATIC = True
        template = Template("{% load django_perseus_tags %}{% url 'index' %}")
        assert template.render(self.ctx) == 'index.html'

    def test_url_tag_subpage_index(self, settings):
        settings.RENDER_STATIC = True
        template = Template("{% load django_perseus_tags %}{% url 'testapp2:index' %}")
        assert template.render(self.ctx) == 'testapp2.html'

    def test_url_tag_subpage_sub(self, settings):
        settings.RENDER_STATIC = True
        template = Template("{% load django_perseus_tags %}{% url 'testapp2:sub1' %}")
        assert template.render(self.ctx) == 'testapp2/test.html'

    def test_url_tag_subpage_sub_arg_1(self, settings):
        settings.RENDER_STATIC = True
        template = Template("{% load django_perseus_tags %}{% url 'testapp2:sub2' 1 %}")
        assert template.render(self.ctx) == 'testapp2/test/1.html'

    def test_url_tag_subpage_sub_arg_2(self, settings):
        settings.RENDER_STATIC = True
        template = Template("{% load django_perseus_tags %}{% url 'testapp2:sub5' 1 1 %}")
        assert template.render(self.ctx) == 'testapp2/test/1/test/1.html'

    def test_url_tag_renderer_disabled(self, settings):
        settings.RENDER_STATIC = False
        template = Template("{% load django_perseus_tags %}{% url 'index' %}")
        assert template.render(self.ctx) == '/'
