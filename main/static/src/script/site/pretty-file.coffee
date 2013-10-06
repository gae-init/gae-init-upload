# http://blog.anorgan.com/2012/09/30/pretty-multi-file-upload-bootstrap-jquery-twig-silex/
if $(".pretty-file").length
  $(".pretty-file").each () ->
    pretty_file = $(this)
    file_input = pretty_file.find('input[type="file"]')
    file_input.hide()
    file_input.change () ->
      files = file_input[0].files
      info = ""
      if files.length > 1
        info = "#{files.length} files selected"
      else
        path = file_input.val().split("\\")
        info = path[path.length - 1]
      pretty_file.find(".input-group input").val(info)
    pretty_file.find(".input-group").click (e) ->
      e.preventDefault()
      file_input.click()
      $(this).blur()
