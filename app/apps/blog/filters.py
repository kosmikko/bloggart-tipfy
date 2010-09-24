from tipfy.ext.jinja2 import create_jinja2_instance

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
  return value.strftime(format)

def to_int(value):
  return int(value)

def create_environment():
  env = create_jinja2_instance()
  env.filters['datetimeformat'] = datetimeformat
  env.filters['to_int'] = to_int
  return env