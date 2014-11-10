from django.conf import settings
from django import template
from django.template.defaulttags import url as django_url_tag
from django.template.defaulttags import URLNode
from django.templatetags.static import do_static, StaticNode


register = template.Library()


def render_static():
    return getattr(settings, 'RENDER_STATIC', False)


class StaticUrlNode(StaticNode):

    def render(self, context):
        url = super(StaticUrlNode, self).render(context)
        if not render_static():
            return url

        if url.startswith('/'):
            return url[1:]

        return url


@register.tag
def static(parser, token, node_cls=StaticUrlNode):
    node_instance = do_static(parser, token)

    return node_cls(
        varname=node_instance.varname,
        path=node_instance.path
    )


class RenderUrlNode(URLNode):

    path = '{0}.html'

    def render(self, context):
        url = super(RenderUrlNode, self).render(context)
        if not render_static():
            return url

        if url == '/':
            return self.path.format('index')

        if url.startswith('/'):
            url = url[1:]

        if url.endswith('/'):
            return self.path.format(url[:-1])
        else:
            return self.path.format(url)


@register.tag
def url(parser, token, node_cls=RenderUrlNode):
    node_instance = django_url_tag(parser, token)

    return node_cls(
        view_name=node_instance.view_name,
        args=node_instance.args,
        kwargs=node_instance.kwargs,
        asvar=node_instance.asvar
    )
