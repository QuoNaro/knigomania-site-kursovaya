function goBack() {
  window.history.back();
}

$(document).on('click','.backdoor-button', function() {
  goBack();
});