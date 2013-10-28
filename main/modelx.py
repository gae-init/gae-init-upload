# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
import util
import flask
import hashlib


class BaseX(object):
  @classmethod
  def retrieve_one_by(cls, name, value):
    cls_db_list = cls.query(getattr(cls, name) == value).fetch(1)
    if cls_db_list:
      return cls_db_list[0]
    return None


class ConfigX(object):
  @classmethod
  def get_master_db(cls):
    return cls.get_or_insert('master')


class UserX(object):
  @property
  def avatar_url(self):
    return '//gravatar.com/avatar/%s?d=identicon&r=x' % (
        hashlib.md5((self.email or self.name).encode('utf-8')).hexdigest().lower()
      )


class ResourceX(object):
  @ndb.ComputedProperty
  def size_human(self):
    return util.size_human(self.size or 0)

  @ndb.ComputedProperty
  def download_url(self):
    if self.key:
      return '%s%s' % (
          flask.request.url_root[:-1],
          flask.url_for('resource_download', resource_id=self.key.id()),
        )
    return None

  @ndb.ComputedProperty
  def view_url(self):
    if self.key:
      return '%s%s' % (
          flask.request.url_root[:-1],
          flask.url_for('resource_view', resource_id=self.key.id()),
        )
    return None

  @ndb.ComputedProperty
  def serve_url(self):
    return '%s/serve/%s' % (
        flask.request.url_root[:-1],
        self.blob_key,
      )
