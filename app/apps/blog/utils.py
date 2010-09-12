import config
from tipfy.ext.jinja2 import render_template as jinja2_render_template

def render_template(template_name, template_vals={}):
    """
    render_to_string returns a unicode string, the rendered template needs to
    be a string to be stored in BlobProperty
    """
    template_vals['config'] = config
    template = "themes/%s/%s" % (config.theme, template_name)
    return str(jinja2_render_template(template, **template_vals))