# coding: utf-8

import urllib

from flask.ext import wtf
from google.appengine.api import images
from google.appengine.ext import blobstore
import flask
import werkzeug

import auth
import config
import model
import util

from main import app


################################################################################
# Upload
################################################################################
@app.route('/_s/resource/upload/', endpoint='resource_upload_service', methods=['GET', 'POST'])
@app.route('/resource/upload/', endpoint='resource_upload', methods=['GET', 'POST'])
@auth.login_required
def resource_upload():
  if flask.request.method == 'GET':
    gs_bucket_name = config.CONFIG_DB.bucket_name or None
    count = util.param('count', int) or 1

    if flask.request.path.startswith('/_s/'):
      urls = []
      for _ in range(count):
        urls.append({'upload_url': blobstore.create_upload_url(
            flask.request.path,
            gs_bucket_name=gs_bucket_name,
          )})
      return flask.jsonify({
          'status': 'success',
          'count': count,
          'result': urls,
        })

    return flask.render_template(
        'resource/resource_upload.html',
        title='Resource Upload',
        html_class='resource-upload',
        get_upload_url=flask.url_for('resource_upload_service'),
        has_json=True,
        upload_url=blobstore.create_upload_url(
            flask.request.path,
            gs_bucket_name=gs_bucket_name,
          ),
      )

  # POST stuff
  resource_db = resource_db_from_upload()

  if flask.request.path.startswith('/_s/'):
    if resource_db:
      return util.jsonify_model_db(resource_db)
    else:
      flask.abort(500)

  if resource_db:
    return flask.redirect(flask.url_for('welcome'))
  else:
    flask.flash('Something went wrong with the uploading.. please try again!', category='danger')
    return flask.redirect(flask.url_for('resource_upload'))


################################################################################
# List
################################################################################
@app.route('/_s/resource/', endpoint='resource_list_service')
@app.route('/resource/', endpoint='resource_list')
@auth.login_required
def resource_list():
  resource_dbs, next_cursor = auth.current_user_db().get_resource_dbs()

  if flask.request.path.startswith('/_s/'):
    return util.jsonify_model_dbs(resource_dbs, next_cursor)

  return flask.render_template(
      'resource/resource_list.html',
      html_class='resource-list',
      title='Resource List',
      resource_dbs=resource_dbs,
      next_url=util.generate_next_url(next_cursor),
      has_json=True,
    )


################################################################################
# View
################################################################################
@app.route('/_s/resource/<int:resource_id>/view/', endpoint='resource_view_service')
@app.route('/resource/<int:resource_id>/view/', endpoint='resource_view')
@auth.login_required
def resource_view(resource_id):
  resource_db = model.Resource.get_by_id(resource_id)

  if not resource_db or resource_db.user_key != auth.current_user_key():
    return flask.abort(404)

  if flask.request.path.startswith('/_s/'):
    return util.jsonify_model_db(resource_db)

  return flask.render_template(
      'resource/resource_view.html',
      html_class='resource-view',
      title='%s' % (resource_db.name),
      resource_db=resource_db,
      has_json=True,
    )


################################################################################
# Update
################################################################################
class ResourceUpdateForm(wtf.Form):
  name = wtf.TextField('Name', [wtf.validators.required()])


@app.route('/_s/resource/<int:resource_id>/update/', methods=['GET', 'POST'], endpoint='resource_update_service')
@app.route('/resource/<int:resource_id>/update/', methods=['GET', 'POST'], endpoint='resource_update')
@auth.login_required
def resource_update(resource_id):
  resource_db = model.Resource.get_by_id(resource_id)

  if not resource_db or resource_db.user_key != auth.current_user_key():
    return flask.abort(404)

  form = ResourceUpdateForm()

  if form.validate_on_submit():
    resource_db.name = form.name.data
    resource_db.put()
    return flask.redirect(flask.url_for(
        'resource_view', resource_id=resource_db.key.id(),
      ))
  if not form.errors:
    form.name.data = resource_db.name

  if flask.request.path.startswith('/_s/'):
    if form.errors:
      return flask.abort(400)
    return util.jsonify_model_db(resource_db)

  return flask.render_template(
      'resource/resource_update.html',
      html_class='resource-update',
      title='%s' % (resource_db.name),
      resource_db=resource_db,
      form=form,
      has_json=True,
    )


################################################################################
# Delete
################################################################################
@app.route('/_s/resource/<int:resource_id>/delete/', methods=['POST'])
@auth.login_required
def resource_delete(resource_id):
  resource_db = model.Resource.get_by_id(resource_id)

  if not resource_db or resource_db.user_key != auth.current_user_key():
    return flask.abort(404)

  blobstore.BlobInfo.get(resource_db.blob_key).delete()
  resource_db.key.delete()

  return util.jsonify_model_db(resource_db)


################################################################################
# Download
################################################################################
@app.route('/resource/<int:resource_id>/download/')
@auth.login_required
def resource_download(resource_id):
  resource_db = model.Resource.get_by_id(resource_id)
  name = urllib.quote(resource_db.name.encode('utf-8'))
  url = '/serve/%s?save_as=%s' % (resource_db.blob_key, name)
  return flask.redirect(url)


################################################################################
# Helpers
################################################################################
def resource_db_from_upload():
  try:
    uploaded_file = flask.request.files['file']
  except:
    return None
  headers = uploaded_file.headers['Content-Type']
  blob_info_key = werkzeug.parse_options_header(headers)[1]['blob-key']
  blob_info = blobstore.BlobInfo.get(blob_info_key)

  image_url = None
  if blob_info.content_type.startswith('image'):
    try:
      image_url = images.get_serving_url(blob_info.key())
    except:
      pass

  resource_db = model.Resource(
      user_key=auth.current_user_key(),
      blob_key=blob_info.key(),
      name=blob_info.filename,
      content_type=blob_info.content_type,
      size=blob_info.size,
      image_url=image_url,
      bucket_name=config.CONFIG_DB.bucket_name or None,
    )
  resource_db.put()
  return resource_db
