from .. import config
from tipfy.ext.jinja2 import render_template as jinja2_render_template


def _get_all_paths():
  import models
  keys = []
  q = models.StaticContent.all(keys_only=True).filter('indexed', True)
  cur = q.fetch(1000)
  while len(cur) == 1000:
    keys.extend(cur)
    q = models.StaticContent.all(keys_only=True)
    q.filter('indexed', True)
    q.filter('__key__ >', cur[-1])
    cur = q.fetch(1000)
  keys.extend(cur)
  return [x.name() for x in keys]
  
def _regenerate_sitemap():
  import gzip
  import models
  from StringIO import StringIO
  from ..utils import render_template
  paths = _get_all_paths()
  rendered = render_template('sitemap.xml', {'paths': paths})
  models.StaticContent.set('/sitemap.xml', rendered, 'application/xml', False)
  s = StringIO()
  gzip.GzipFile(fileobj=s,mode='wb').write(rendered)
  s.seek(0)
  renderedgz = s.read()
  models.StaticContent.set('/sitemap.xml.gz',renderedgz, 'application/x-gzip', False)
  if config.google_sitemap_ping:
      ping_googlesitemap()

def ping_googlesitemap():
  import urllib
  from google.appengine.api import urlfetch
  google_url = 'http://www.google.com/webmasters/tools/ping?sitemap=http://' + config.host + '/sitemap.xml.gz'
  response = urlfetch.fetch(google_url, '', urlfetch.GET)
  if response.status_code / 100 != 2:
    raise Warning("Google Sitemap ping failed", response.status_code, response.content)