(->
  class window.FileUploader
    constructor: (options) ->
      @active_files = 0
      @options =
        confirm_message: 'Files are still being uploaded.'
        upload_url: "/_s#{window.location.pathname}"

      for option of options
        @options[option] = options[option]

      $(@options.selector)?.bind 'change', (e) =>
        @file_select_handler(e)

      xhr = new XMLHttpRequest()
      if xhr.upload
        $(@options.drop_area)?.on 'dragover', @file_drag_hover
        $(@options.drop_area)?.on 'dragleave', @file_drag_hover
        $(@options.drop_area)?.on 'drop', (e) =>
          @file_select_handler(e)
        $(@options.drop_area)?.show()

      window.onbeforeunload = () =>
        if @options?.confirm_message and @active_files > 0
          return @options.confirm_message

    file_drag_hover: (e) =>
      e.stopPropagation()
      e.preventDefault()
      if e.type is 'dragover'
        $(@options.drop_area).addClass('drag-hover')
      else
        $(@options.drop_area).removeClass('drag-hover')

    file_select_handler: (e) =>
      @file_drag_hover(e)
      files = e.originalEvent.dataTransfer?.files or e.target?.files or e.dataTransfer?.files
      if files?.length > 0
        @upload_files(files)

    upload_files: (files) =>
      @get_upload_urls files.length, (error, urls) =>
        if error
          LOG 'Error getting URLs', error
          return
        @process_files(files, urls, 0)

    get_upload_urls: (n, callback) =>
      return if n <= 0
      service_call 'GET', @options.upload_url, {count:n}, (error, result) ->
        if error
          callback(error)
          throw error
        callback(undefined, result)

    process_files: (files, urls, i) =>
      return if i >= files.length
      @upload_file files[i], urls[i].upload_url, @options.upload_handler?.preview(files[i]), =>
        @process_files files, urls, i + 1, @options.upload_handler?

    upload_file: (file, url, progress, callback) =>
      LOG 'file', file
      @active_files += 1
      xhr = new XMLHttpRequest()
      xhr.upload.addEventListener 'progress', (event) ->
          progress(parseInt(event.loaded / event.total * 99.0))
        , false

      xhr.onload = (event) =>
        response = JSON.parse(event.currentTarget.response)
        progress(100.0, response.result)
        @active_files -= 1
      xhr.onerror = () =>
        progress(-1)
        @active_files -= 1

      xhr.open('POST', url, true)
      data = new FormData()
      data.append('file', file)
      xhr.send(data)
      callback()
)()
