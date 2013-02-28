window.init_resource_list = () ->
  init_delete_resource_button()

window.init_resource_view = () ->
  init_delete_resource_button()


window.init_resource_upload = () ->
  if window.File and window.FileList and window.FileReader
    file_uploader = new FileUploader(upload_handler, $('.file'), $('.drop-area'))


upload_handler =
  preview: (file) ->
    $resource = $ """
        <li class="span3">
          <div class="thumbnail">
            <div class="preview"></div>
            <h5>#{file.name}</h5>
            <div class="progress">
              <div class="bar" style="width: 0%;"></div>
            </div>
          </div>
        </li>
      """
    $preview = $('.preview', $resource)

    if file.type.indexOf("image") is 0
      reader = new FileReader()
      reader.onload = (e) =>
        $preview.css('background-image', "url(#{e.target.result})")
      reader.readAsDataURL(file)
    else
      $preview.text(file.type or 'application/octet-stream')

    $('.resource-uploads').prepend($resource)

    (progress, resource) =>
      if progress >=0
        $('.bar', $resource).css
          width: "#{progress}%"
        $('.bar', $resource).text("#{progress}% of #{size_human(file.size)}")
        if resource
          $('.bar', $resource).addClass('bar-success')
          $('.bar', $resource).text("Success #{size_human(file.size)}")
      else
        $('.bar', $resource).css('width', '100%')
        $('.bar', $resource).addClass('bar-danger')
        $('.bar', $resource).text('Failed')


window.init_delete_resource_button = () ->
  $('body').on 'click', '.btn-delete', (e) ->
    e.preventDefault()
    if confirm('Press OK to delete the resource')
      $(this).attr('disabled', 'disabled')
      service_call 'POST', $(this).data('service-url'), (err, result) =>
        if err
          $(this).removeAttr('disabled')
          LOG 'Something went terribly wrong during delete!', err
          return
        target = $(this).data('target')
        redirect_url = $(this).data('redirect-url')
        if target
          $("#{target}").remove()
        if redirect_url
          window.location.href = redirect_url
