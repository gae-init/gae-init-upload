$(() => {
  initCommon();

  $('html.auth').each(() => {
    initAuth();
  });

  $('html.user-list').each(() => {
    initUserList();
  });

  $('html.user-merge').each(() => {
    initUserMerge();
  });

  $('html.resource-list').each(() => {
  initResourceList()
  });

  $('html.resource-view').each(() => {
    initResourceView()
    });

  $('html.resource-upload').each(() => {
    initResourceUpload()
    });

});
