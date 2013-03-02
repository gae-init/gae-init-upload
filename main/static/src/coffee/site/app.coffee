#JS enabled pages
$ ->

$ -> $('html.welcome').each ->

$ -> $('html.profile').each ->
  init_profile()

$ -> $('html.feedback').each ->
  init_loading_button()

$ -> $('html.admin-config').each ->
  init_admin_config()

$ -> $('html.resource-list').each ->
  init_resource_list()

$ -> $('html.resource-view').each ->
  init_resource_view()

$ -> $('html.resource-upload').each ->
  init_resource_upload()
