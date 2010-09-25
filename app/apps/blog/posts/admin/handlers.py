"""
Admin handlers
"""

import os, logging, datetime

from google.appengine.ext import db
from google.appengine.ext import deferred

from tipfy import (RequestHandler, RequestRedirect, Response, abort,
    cached_property, redirect, url_for, render_json_response)
from tipfy.ext.auth import AppEngineAuthMixin, login_required, user_required, admin_required

from tipfy.ext.jinja2 import Jinja2Mixin, render_response, render_template
from tipfy.ext.session import AllSessionMixins, SessionMiddleware
from tipfy.ext.wtforms import Form, fields, validators

from ... import config 
from ..models import BlogPost
from utils import with_post
from forms import PostForm
from .. import markup
from .. import post_deploy

class BaseHandler(RequestHandler, AppEngineAuthMixin, Jinja2Mixin):
  def render_to_response(self, template_name, template_vals=None, theme=None):
    template = os.path.join("admin", template_name)
    context = {
    'config': config
    }
    if template_vals:
      context.update(template_vals)

    return self.render_response(template, **context)


class HomeHandler(BaseHandler):
  """A handler that outputs the result of a rendered template."""
  def get(self, **kwargs):
    return render_response('home.html', message='Hello, Jinja!')


class AdminHandler(BaseHandler):
  @admin_required
  def get(self, **kwargs):
    """
    Show a list of posts
    """
    offset = int(self.request.args.get('start', 0))
    count = int(self.request.args.get('count', 20))

    posts = BlogPost.all().order('-published').fetch(count, offset)
    template_vals = {
    'is_admin': True,
    'offset': offset,
    'count': count,
    'last_post': offset + len(posts) - 1,
    'prev_offset': max(0, offset - count),
    'next_offset': offset + count,
    'posts': posts,
    }

    return self.render_to_response('index.html', template_vals)



class PostHandler(BaseHandler):
  def render_form(self, post=None):
    self.form = self.get_form(post)
    return self.render_to_response("edit.html", {'form': self.form})

  @admin_required
  @with_post
  def get(self, post):
     return self.render_form(post)

  @admin_required
  @with_post  
  def post(self, post):
    self.form = self.get_form(post)

    newpost = False
    if not post:
      newpost = True
      post = BlogPost(title=self.form.title.data, body=self.form.body.data)

    if self.form.validate():
      self.form.populate_obj(post)
      if newpost:
        post.published = datetime.datetime.now()
      post.updated = datetime.datetime.now()
      post.publish()
      return self.render_to_response("published.html", {'post': post})

    return self.render_form()

  def get_form(self, post):
    return PostForm(self.request, obj=post)

class DeleteHandler(BaseHandler):
  @with_post
  def post(self, post):
    if post.path:# Published post
      post.remove()
    else:# Draft
      post.delete()
    return self.render_to_response("deleted.html", None)
        
class PreviewHandler(RequestHandler):
  def get(self):
    logging.info('get called')
    return Response('test')  
    
  def post(self, **kwargs):
    body = self.request.form.get('body')
    title = self.request.form.get('title')  
    body_markup = self.request.form.get('body_markup')

    try:
        post = BlogPost(title=title, body=body, body_markup=body_markup)  
        html = markup.render_body(post)
        result = {'success': 'True',
                  'content': html}
    except Exception, e:
        error = ("Unable to markup data: %s" % e)
        result = {'success': 'False',
                    'content': error}
    return render_json_response(result)     
    
class RegenerateHandler(BaseHandler):
  def post(self):
    regen = post_deploy.PostRegenerator()
    deferred.defer(regen.regenerate)
    deferred.defer(post_deploy.post_deploy, post_deploy.BLOG_VERSION)
    return self.render_to_response("regenerating.html")

