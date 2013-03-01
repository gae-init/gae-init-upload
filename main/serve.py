import webapp2
import urllib
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, blob_key):
    blob_key = str(urllib.unquote(blob_key))
    blob_info = blobstore.BlobInfo.get(blob_key)
    save_as = self.request.get('save_as', None)
    if save_as:
      save_as = urllib.quote(save_as.encode('utf-8'), safe='%!()[]=')
    self.send_blob(blob_info, save_as=save_as)


app = webapp2.WSGIApplication([
      ('/serve/([^/]+)?', ServeHandler),
    ], debug=True,
  )
