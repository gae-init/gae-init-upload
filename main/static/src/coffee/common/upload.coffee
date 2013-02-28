(->
  class window.FileUploader
    constructor: (@upload_handler, @selector, @drop_area) ->
      $(@selector)?.bind 'change', (e) =>
        @file_select_handler(e)

      xhr = new XMLHttpRequest()
      if xhr.upload
        $(@drop_area)?.on 'dragover', @file_drag_hover
        $(@drop_area)?.on 'dragleave', @file_drag_hover
        $(@drop_area)?.on 'drop', (e) =>
          @file_select_handler(e)
        $(@drop_area)?.show()

    file_drag_hover: (e) =>
      e.stopPropagation()
      e.preventDefault()
      if e.type is 'dragover'
        $(@drop_area).addClass('drag-hover')
      else
        $(@drop_area).removeClass('drag-hover')

    file_select_handler: (e) ->
      @file_drag_hover(e)
      files = e.originalEvent.dataTransfer?.files or e.target?.files or e.dataTransfer?.files
      if files?.length > 0
        @upload_files(files)

    upload_files: (files) ->
      @get_upload_urls files.length, (error, urls) =>
        if error
          LOG 'error getting URLs', error
          return
        @process_files(files, urls, 0)

    get_upload_urls: (n, callback) ->
      return if n <= 0
      service_call 'GET', '/_s' + window.location.pathname, {count:n}, (error, result) ->
        if error
          callback(error)
          throw error
        callback(undefined, result)

    process_files: (files, urls, i) ->
      return if i >= files.length
      @upload_file files[i], urls[i].upload_url, @upload_handler.preview(files[i]), =>
        @process_files files, urls, i + 1, @upload_handler

    upload_file: (file, url, progress, callback) ->
      xhr = new XMLHttpRequest()
      xhr.upload.addEventListener 'progress', (event) ->
          progress(parseInt(event.loaded / event.total * 99.0))
        , false

      xhr.onload = (event) ->
        response = JSON.parse(event.currentTarget.response)
        progress(100.0, response.result)
      xhr.onerror = () ->
        progress(-1)

      xhr.open('POST', url, true)
      data = new FormData()
      data.append('file', file)
      xhr.send(data)
      callback()
)()
