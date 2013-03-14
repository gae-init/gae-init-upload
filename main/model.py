from google.appengine.ext import ndb
import modelx
from uuid import uuid4


class Base(ndb.Model, modelx.BaseX):
  created = ndb.DateTimeProperty(auto_now_add=True)
  modified = ndb.DateTimeProperty(auto_now=True)
  _PROPERTIES = set([
      'key', 'id', 'created', 'modified', 'created_ago', 'modified_ago',
    ])


class Config(Base, modelx.ConfigX):
  analytics_id = ndb.StringProperty(default='')
  brand_name = ndb.StringProperty(default='gae-init-upload')
  bucket_name = ndb.StringProperty(default='')
  facebook_app_id = ndb.StringProperty(default='')
  facebook_app_secret = ndb.StringProperty(default='')
  feedback_email = ndb.StringProperty(default='')
  flask_secret_key = ndb.StringProperty(default=str(uuid4()).replace('-', ''))
  twitter_consumer_key = ndb.StringProperty(default='')
  twitter_consumer_secret = ndb.StringProperty(default='')
  _PROPERTIES = Base._PROPERTIES.union(set([
      'analytics_id',
      'brand_name',
      'bucket_name',
      'facebook_app_id',
      'facebook_app_secret',
      'feedback_email',
      'flask_secret_key',
      'twitter_consumer_key',
      'twitter_consumer_secret',
    ]))


class User(Base, modelx.UserX):
  name = ndb.StringProperty(indexed=True, required=True)
  username = ndb.StringProperty(indexed=True, required=True)
  email = ndb.StringProperty(default='')

  active = ndb.BooleanProperty(default=True)
  admin = ndb.BooleanProperty(default=False)

  federated_id = ndb.StringProperty(default='')
  facebook_id = ndb.StringProperty(default='')
  twitter_id = ndb.StringProperty(default='')

  _PROPERTIES = Base._PROPERTIES.union(set([
      'name', 'username', 'avatar_url',
    ]))


class Resource(Base, modelx.ResourceX):
  user_key = ndb.KeyProperty(kind=User, required=True)
  blob_key = ndb.BlobKeyProperty(required=True)
  name = ndb.StringProperty(required=True)
  bucket_name = ndb.StringProperty()
  image_url = ndb.StringProperty(default='')
  content_type = ndb.StringProperty(default='')
  size = ndb.IntegerProperty(default=0)

  _PROPERTIES = Base._PROPERTIES.union(set([
      'name',
      'bucket_name',
      'image_url',
      'content_type',
      'size',
      'size_human',
      'download_url',
      'view_url',
      'serve_url',
    ]))
