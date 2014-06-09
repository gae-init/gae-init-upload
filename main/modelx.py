# coding: utf-8

from google.appengine.ext import ndb
import util
import flask
import hashlib


class Config(object):
  @classmethod
  def get_master_db(cls):
    return cls.get_or_insert('master')

  @property
  def has_facebook(self):
    return bool(self.facebook_app_id and self.facebook_app_secret)

  @property
  def has_twitter(self):
    return bool(self.twitter_consumer_key and self.twitter_consumer_secret)


class User(object):
  def has_permission(self, perm):
    return self.admin or perm in self.permissions

  def avatar_url_size(self, size=None):
    return '//gravatar.com/avatar/%(hash)s?d=identicon&r=x%(size)s' % {
        'hash': hashlib.md5(self.email or self.username).hexdigest(),
        'size': '&s=%d' % size if size > 0 else '',
      }
  avatar_url = property(avatar_url_size)


class ResourceX(object):
  @ndb.ComputedProperty
  def size_human(self):
    return util.size_human(self.size or 0)

  @property
  def download_url(self):
    if self.key:
      return '%s%s' % (
          flask.request.url_root[:-1],
          flask.url_for('resource_download', resource_id=self.key.id()),
        )
    return None

  @property
  def view_url(self):
    if self.key:
      return '%s%s' % (
          flask.request.url_root[:-1],
          flask.url_for('resource_view', resource_id=self.key.id()),
        )
    return None

  @property
  def serve_url(self):
    return '%s/serve/%s' % (
        flask.request.url_root[:-1],
        self.blob_key,
      )
