// Функция для показа/скрытия пароля
function showHidePassword(target) {
  var $input = $('#password-input');
  var $img = $('#eye');
  
  if ($input.attr('type') === 'password') {
      $input.attr('type', 'text');
      $img.attr('name', 'eye-off-outline');
  } else {
      $input.attr('type', 'password');
      $img.attr('name', 'eye-outline');
  }
  return false;
}

 // Обработка нажатия клавиши Enter
 function handleKeyPress(event, nextInputId) {
  if (event.key === "Enter") {
      event.preventDefault();
      $('#' + nextInputId).focus();
  }
}


$(document).ready(function() {
  $(document).on('click' , '.password-control' , function(){
    showHidePassword()
  })

  // Обработчик клика для ссылки "Забыли пароль?"
  $('#forget-password').on('click', function(event) {
      event.preventDefault();
      $('#box').toggleClass('flip');
      $('#front').toggleClass('flip');

      if ($('#login-input').val()) {
          $('#login-forget-input').val($('#login-input').val());
      }
  });

  // Обработчик клика для ссылки "Назад"
  $('#back-link').on('click', function(event) {
      event.preventDefault();
      $('#box').removeClass('flip');
      $('#front').removeClass('flip');
  });

  // Обработка нажатий клавиш для навигации по полям ввода
  $('input').each(function(index) {
      $(this).on('keydown', function(event) {
          if (event.key === "ArrowDown" && index < $('input').length - 1) {
              event.preventDefault();
              $('input').eq(index + 1).focus();
          } else if (event.key === "ArrowUp" && index > 0) {
              event.preventDefault();
              $('input').eq(index - 1).focus();
          }
      });
  });
});


