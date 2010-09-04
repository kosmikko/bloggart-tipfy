import logging
from tipfy.ext.wtforms import Form, fields
from ..models import BlogPost
from wtforms.ext.appengine.db import ModelConverter, model_form

class SetPropertyField(fields.TextAreaField):
    """
    A field for ``db.SetProperty``. The set items are rendered in a
    textarea.
    """
    def process_data(self, value):
        if isinstance(value, set):
            value = '\n'.join(value)
        self.data = value

    def populate_obj(self, obj, name):
        if isinstance(self.data, basestring):
            value = set(self.data.strip().splitlines())
        else:
            value = set()
        setattr(obj, name, value)


class BlogModelConverter(ModelConverter):
  """
  Extends ModelConverter to support aetycoon's SetProperty
  """
  def __init__(self, converters=None):
    self.extended_converters = self.default_converters
    self.extended_converters['SetProperty'] = convert_SetProperty
    self.converters = converters or self.extended_converters

def convert_SetProperty(model, prop, kwargs):
  return SetPropertyField(**kwargs)
    
class BasePostForm(Form):
  # Add an extra, non-model related field.
  draft = fields.BooleanField('Draft?')  

PostForm = model_form(BlogPost, base_class=BasePostForm, converter=BlogModelConverter())

