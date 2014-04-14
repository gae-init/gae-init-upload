# coding: utf-8

from google.appengine.ext import ndb

import config
import modelx
import util


class Base(ndb.Model, modelx.BaseX):
  created = ndb.DateTimeProperty(auto_now_add=True)
  modified = ndb.DateTimeProperty(auto_now=True)
  version = ndb.IntegerProperty(default=config.CURRENT_VERSION_TIMESTAMP)

  _PROPERTIES = {
      'key',
      'id',
      'version',
      'created',
      'modified',
    }


class Config(Base, modelx.ConfigX):
  analytics_id = ndb.StringProperty(default='')
  announcement_html = ndb.TextProperty(default='')
  announcement_type = ndb.StringProperty(default='info', choices=[
      'info', 'warning', 'success', 'danger',
    ])
  brand_name = ndb.StringProperty(default=config.APPLICATION_ID)
  bucket_name = ndb.StringProperty(default='')
  facebook_app_id = ndb.StringProperty(default='')
  facebook_app_secret = ndb.StringProperty(default='')
  feedback_email = ndb.StringProperty(default='')
  flask_secret_key = ndb.StringProperty(default=util.uuid())
  notify_on_new_user = ndb.BooleanProperty(default=True)
  twitter_consumer_key = ndb.StringProperty(default='')
  twitter_consumer_secret = ndb.StringProperty(default='')

  _PROPERTIES = Base._PROPERTIES.union({
      'analytics_id',
      'announcement_html',
      'announcement_type',
      'brand_name',
      'bucket_name',
      'facebook_app_id',
      'facebook_app_secret',
      'feedback_email',
      'flask_secret_key',
      'notify_on_new_user',
      'twitter_consumer_key',
      'twitter_consumer_secret',
    })


class User(Base, modelx.UserX):
  name = ndb.StringProperty(required=True)
  username = ndb.StringProperty(required=True)
  email = ndb.StringProperty(default='')
  auth_ids = ndb.StringProperty(repeated=True)
  active = ndb.BooleanProperty(default=True)
  admin = ndb.BooleanProperty(default=False)
  permissions = ndb.StringProperty(repeated=True)

  _PROPERTIES = Base._PROPERTIES.union({
      'active',
      'admin',
      'auth_ids',
      'avatar_url',
      'email',
      'name',
      'username',
      'permissions',
    })


class Resource(Base, modelx.ResourceX):
  user_key = ndb.KeyProperty(kind=User, required=True)
  blob_key = ndb.BlobKeyProperty(required=True)
  name = ndb.StringProperty(required=True)
  bucket_name = ndb.StringProperty()
  image_url = ndb.StringProperty(default='')
  content_type = ndb.StringProperty(default='')
  size = ndb.IntegerProperty(default=0)

  _PROPERTIES = Base._PROPERTIES.union({
      'bucket_name',
      'content_type',
      'download_url',
      'image_url',
      'name',
      'serve_url',
      'size',
      'size_human',
      'view_url',
    })
