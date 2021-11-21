'''from django.template import Library, TemplateSyntaxError, Node, TemplateDoesNotExist
from django.template.loader import get_template
from django.template.response import SimpleTemplateResponse as sr

class IncludeNode(Node):
    def __init__(self, template_name):
        self.template_name = template_name

        def render(self, context):
            try:
               template_name = sr.resolve_template(self.template_name, context)
               included_template = get_template(template_name).render(context)
            except TemplateDoesNotExist:
                included_template = ''
            return included_template


register = Library()

@register.tag
def try_to_include(parser, token):
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError('{0} tag requires a single argument'.format(token.contents.split()[0]))
    return IncludeNode(template_name)'''