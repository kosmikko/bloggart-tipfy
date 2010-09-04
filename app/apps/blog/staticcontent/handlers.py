"""
Admin handlers
"""

import os, logging, datetime

from tipfy import (RequestHandler, RequestRedirect, Response, NotFound)
from tipfy.ext.jinja2 import Jinja2Mixin, render_response, render_template
from werkzeug import Headers
from models import StaticContent
from .. import config

HTTP_DATE_FMT = "%a, %d %b %Y %H:%M:%S GMT"

class BaseHandler(RequestHandler, Jinja2Mixin):
  def render_to_response(self, template_name, template_vals=None, theme=None):
    context = {
    }

    context.update(template_vals)

    return self.render_response(template_name, **context)

class StaticContentHandler(BaseHandler):

  def output_content(self, content, serve=True):
    """Output the content in the datastore as a HTTP Response"""
    headers = Headers()
    if content.content_type:
      headers['Content-Type'] = content.content_type
    last_modified = content.last_modified.strftime(HTTP_DATE_FMT)
    headers.add('Last-Modified', last_modified)
    headers.add('ETag', '"%s"' % (content.etag,))
    for header in content.headers:
      key, value = header.split(':', 1)
      headers[key] = value.strip()
    if serve:
      response = Response(content.body, content_type=content.content_type,
                          headers=headers, status=content.status)
    else:
      response = Response(status=304)
    return response

  def get(self, path=''):
    content = StaticContent.get("/%s" % path.lower())
    logging.info(path)
    logging.info(content)
    if not content:
      if path == '':
        return self.render_to_response("themes/%s/listing.html" % config.theme,
                                       {'config': config, 'no_post': True,})
      else:
        raise NotFound

    serve = True
    # check modifications and etag
    if 'If-Modified-Since' in self.request.headers:
      last_seen = datetime.datetime.strptime(
          self.request.headers['If-Modified-Since'], HTTP_DATE_FMT)
      if last_seen >= content.last_modified.replace(microsecond=0):
        serve = False
    if 'If-None-Match' in self.request.headers:
      etags = [x.strip('" ')
               for x in self.request.headers['If-None-Match'].split(',')]
      if content.etag in etags:
        serve = False
    response = self.output_content(content, serve)
    return response