(->
  class window.FileUploader
    constructor: (@options) ->
      @upload_handler = @options.upload_handler
      @selector = @options.selector
      @drop_area = @options.drop_area
      @upload_url = @options.upload_url or "/api/v1#{window.location.pathname}"
      @confirm_message = @options.confirm_message or 'Files are still being uploaded.'
      @allowed_types = @options.allowed_types
      @max_size = @options.max_size

      @active_files = 0

      @selector?.bind 'change', (e) =>
        @file_select_handler(e)

      xhr = new XMLHttpRequest()
      if @drop_area? and xhr.upload
        @drop_area.on 'dragover', @file_drag_hover
        @drop_area.on 'dragleave', @file_drag_hover
        @drop_area.on 'drop', (e) =>
          @file_select_handler(e)
        @drop_area.show()

      window.onbeforeunload = () =>
        if @confirm_message? and @active_files > 0
          return @confirm_message

    file_drag_hover: (e) =>
      if not @drop_area?
        return
      e.stopPropagation()
      e.preventDefault()
      if e.type is 'dragover'
        @drop_area.addClass('drag-hover')
      else
        @drop_area.removeClass('drag-hover')

    file_select_handler: (e) =>
      @file_drag_hover(e)
      files = e.originalEvent.dataTransfer?.files or e.target?.files or e.dataTransfer?.files
      if files?.length > 0
        @upload_files(files)

    upload_files: (files) =>
      @get_upload_urls files.length, (error, urls) =>
        if error
          console.log('Error getting URLs', error)
          return
        @process_files(files, urls, 0)

    get_upload_urls: (n, callback) =>
      return if n <= 0
      api_call 'GET', @upload_url, {count:n}, (error, result) ->
        if error
          callback(error)
          throw error
        callback(undefined, result)

    process_files: (files, urls, i) =>
      return if i >= files.length
      @upload_file files[i], urls[i].upload_url, @upload_handler?.preview(files[i]), () =>
        @process_files files, urls, i + 1, @upload_handler?

    upload_file: (file, url, progress, callback) =>
      xhr = new XMLHttpRequest()
      if @allowed_types?.length > 0
        if file.type not in @allowed_types
          progress(0, undefined, 'wrong_type')
          callback()
          return

      if @max_size?
        if file.size > @max_size
          progress(0, undefined, 'too_big')
          callback()
          return

      @active_files += 1

      xhr.upload.addEventListener 'progress', (event) ->
        progress(parseInt(event.loaded / event.total * 100.0))


      xhr.onload = (event) =>
        response = JSON.parse(event.currentTarget.response)
        progress(100.0, response.result)
        @active_files -= 1
      xhr.onerror = () =>
        progress(0, undefined, 'error')
        @active_files -= 1

      xhr.open('POST', url, true)
      data = new FormData()
      data.append('file', file)
      xhr.send(data)
      callback()
)()
