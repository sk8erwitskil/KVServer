from redis import Redis
from tornado import gen
from tornado.options import define, options
from tornrpc.server import TornRPCServer

define('port',
       default=8000,
       help='Http port to run on.')
define('redis',
        default='127.0.0.1:6379',
        help='The redis server')


class Handlers(object):
  def __init__(self, rhost, rport):
    self.redis = Redis(rhost, int(rport))

  def _get(self, key):
    try:
      return (self.redis.lrange(key, 0, -1), None)
    except Exception as e:
      return (None, str(e))

  def _set(self, key, val):
    try:
      self.redis.rpush(key, val)
      return ('Added "{0}" to "{1}"'.format(val, key), None)
    except Exception as e:
      return (None, str(e))

  def _lrem(self, key, val, num=0):
    try:
      self.redis.lrem(key, val, num)
      return ('Removed all occurences of "{0}" from "{1}"'.format(val, key), None)
    except Exception as e:
      return (None, str(e))

  def _del(self, key):
    try:
      self.redis.delete(key)
      return ('Deleted "{0}"'.format(key), None)
    except Exception as e:
      return (None, str(e))

  def _keys(self):
    try:
      return (self.redis.keys(), None)
    except Exception as e:
      return (None, str(e))

  @gen.coroutine
  def get(self, key):
    if not self.redis.exists(key):
      raise gen.Return('{0} does not exist'.format(key))
    ret, err = self._get(key)
    raise gen.Return(err or ret)

  @gen.coroutine
  def add(self, key, val):
    ret, err = self._set(key, val)
    raise gen.Return(err or ret)

  @gen.coroutine
  def delete(self, key):
    ret, err = self._del(key)
    raise gen.Return(err or ret)

  @gen.coroutine
  def remove_from_list(self, key, val):
    ret, err = self._lrem(key, val)
    raise gen.Return(err or ret)

  @gen.coroutine
  def keys(self):
    ret, err = self._keys()
    raise gen.Return(err or ret)

if __name__ == '__main__':
  options.parse_command_line()
  rhost, rport = options.redis.split(':')
  handlers = Handlers(rhost, rport)
  server = TornRPCServer()
  server.register_async(handlers.get)
  server.register_async(handlers.add)
  server.register_async(handlers.delete)
  server.register_async(handlers.remove_from_list)
  server.register_async(handlers.keys)
  server.start(int(options.port))
