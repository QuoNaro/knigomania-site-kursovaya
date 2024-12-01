$(document).on('click', '.up-button',  function () {
  $('html, body').animate({ scrollTop: 0 }, 'fast');
})



$(document).ready(function () {
  $('.name').each(function () {
    var str = $(this).text();
    var maxLength = 30;
    if (str.length > maxLength) {
      $(this).css({'font-size' : '1rem'});
    }
    
  })

  currentUrl = window.location.href;
  const parts = currentUrl.split('/');
  query = parts[parts.length - 2];
  const decodedString = decodeURIComponent(query);
  
  $('input#search-input').val(decodedString);
  
  $('p.second').append(`«${decodedString}»`)
  

});





