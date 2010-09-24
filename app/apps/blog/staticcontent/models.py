import datetime
import hashlib

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.ext import deferred
from google.appengine.datastore import entity_pb
from google.appengine.api.labs import taskqueue

import aetycoon

import utils

class StaticContent(db.Model):
  """
  Container for statically served content.

  The serving path for content is provided in the key name.
  """
  body = db.BlobProperty()
  content_type = db.StringProperty()
  status = db.IntegerProperty(required=True, default=200)
  last_modified = db.DateTimeProperty(required=True)
  etag = aetycoon.DerivedProperty(lambda x: hashlib.sha1(x.body).hexdigest())
  indexed = db.BooleanProperty(required=True, default=True)
  headers = db.StringListProperty()

  @classmethod
  def get(cls, path):
    """Returns the StaticContent object for the provided path.

    Args:
      path: The path to retrieve StaticContent for.
    Returns:
      A StaticContent object, or None if no content exists for this path.
    """
    entity = memcache.get(path)
    if entity:
      entity = db.model_from_protobuf(entity_pb.EntityProto(entity))
    else:
      entity = StaticContent.get_by_key_name(path)
      if entity:
        memcache.set(path, db.model_to_protobuf(entity).Encode())
    return entity

  @classmethod
  def set(cls, path, body, content_type, indexed=True, **kwargs):
    """Sets the StaticContent for the provided path.

    Args:
      path: The path to store the content against.
      body: The data to serve for that path.
      content_type: The MIME type to serve the content as.
      indexed: Index this page in the sitemap?
      **kwargs: Additional arguments to be passed to the StaticContent constructor
    Returns:
      A StaticContent object.
    """
    now = datetime.datetime.now().replace(second=0, microsecond=0)
    defaults = {
      "last_modified": now,
    }
    defaults.update(kwargs)
    content = StaticContent(
        key_name=path,
        body=body,
        content_type=content_type,
        indexed=indexed,
        **defaults)
    content.put()
    memcache.replace(path, db.model_to_protobuf(content).Encode())
    try:
      eta = now.replace(second=0, microsecond=0) + datetime.timedelta(seconds=65)
      if indexed:
        deferred.defer(
            utils._regenerate_sitemap,
            _name='sitemap-%s' % (now.strftime('%Y%m%d%H%M'),),
            _eta=eta)
        #utils._regenerate_sitemap()

    except (taskqueue.TaskAlreadyExistsError, taskqueue.TombstonedTaskError), e:
      pass
    return content

  @classmethod
  def add(cls, path, body, content_type, indexed=True, **kwargs):
    """Adds a new StaticContent and returns it.

    Args:
      As per set().
    Returns:
      A StaticContent object, or None if one already exists at the given path.
    """
    def _tx():
      if StaticContent.get_by_key_name(path):
        return None
      return cls.set(path, body, content_type, indexed, **kwargs)
    return db.run_in_transaction(_tx)

  @classmethod
  def remove(cls, path):
    """Deletes a StaticContent.

    Args:
      path: Path of the static content to be removed.
    """
    memcache.delete(path)
    def _tx():
      content = StaticContent.get_by_key_name(path)
      if not content:
        return
      content.delete()
    return db.run_in_transaction(_tx)
