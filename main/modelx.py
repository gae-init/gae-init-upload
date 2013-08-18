from google.appengine.ext import ndb
import md5
import util
import flask


class BaseX(object):
  @classmethod
  def retrieve_one_by(cls, name, value):
    cls_db_list = cls.query(getattr(cls, name) == value).fetch(1)
    if cls_db_list:
      return cls_db_list[0]
    return None

  @ndb.ComputedProperty
  def created_ago(self):
    return util.format_datetime_ago(self.created) if self.created else None

  @ndb.ComputedProperty
  def modified_ago(self):
    return util.format_datetime_ago(self.modified) if self.modified else None

  @ndb.ComputedProperty
  def created_utc(self):
    return util.format_datetime_utc(self.created) if self.created else None

  @ndb.ComputedProperty
  def modified_utc(self):
    return util.format_datetime_utc(self.modified) if self.modified else None


class ConfigX(object):
  @classmethod
  def get_master_db(cls):
    return cls.get_or_insert('master')


class UserX(object):
  @ndb.ComputedProperty
  def avatar_url(self):
    return 'http://www.gravatar.com/avatar/%s?d=identicon&r=x' % (
        md5.new(self.email or self.name).hexdigest().lower()
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
