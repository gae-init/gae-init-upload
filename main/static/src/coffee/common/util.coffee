window.LOG = () ->
  console?.log?(arguments...)


window.init_loading_button = () ->
  $('body').on 'click', '.btn-loading', ->
    $(this).button('loading')


window.size_human = (nbytes) ->
  for suffix in ['B', 'KB', 'MB', 'GB', 'TB']
    if nbytes < 1000
      if suffix == 'B'
        return "#{nbytes} #{suffix}"
      return "#{parseInt(nbytes * 10) / 10} #{suffix}"
    nbytes /= 1024.0
