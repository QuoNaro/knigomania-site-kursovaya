function getCSRF() { 
  return $('input[name="csrfmiddlewaretoken"]').val()
}


const baseUrl = window.location.origin;




function checkCart() {
  const book_id = $('input[name="book-id"]').val();
  $.ajax({
    url: `${baseUrl}/ajax/check-cart/`,
    method: 'POST',
    data: {
      csrfmiddlewaretoken: getCSRF(),
      book_id: book_id,
    },
    success: function(response) {
      let quantity = response.quantity;
      if ($('.book-price').length > 0) {
        if (response.quantity === undefined) {
          quantity = 0;
        }
        $('.quantity').empty();
        $('.quantity').append(`${quantity}`);
        
        if ($('.open-cart').length === 0 && quantity >0) {
          $('.book-price').after(`<a href="${baseUrl}/cart" class="open-cart">В корзину!</a>`)
        }
      }
      
      


      // Проверяем, что количество больше 0
      if (quantity > 0) {
        // Создаем элемент span
        const messageSpan = $('<span>Товар в корзине!</span>');
        
        // Добавляем его после .book-price
        $('.book-preview').append(messageSpan);
        
        // Удаляем span через 2 секунды (2000 миллисекунд)
        setTimeout(function() {
          messageSpan.fadeOut(300, function() {
            $(this).remove(); // Удаляем элемент из DOM после анимации
          });
        }, 2000);
      }
    },
    error: function(xhr, status, error) {
      console.error("Ошибка при добавлении товара в корзину:", error);
      // Здесь можно обработать ошибку, если это необходимо
    }
  });
}


$(document).ready(function() {
  $(document).on('click','.book-price',function() {
    book_id = $('input[name="book-id"]').val()
      $.ajax({
          url: `${baseUrl}/ajax/add-to-cart/`, 
          method: 'POST', 
          data: { 
            csrfmiddlewaretoken : getCSRF(),
            book_id : book_id
          },
          success: function(response) { 
            checkCart();
          },
      });
  });
});


function checkRecommendations(response) {
  $('.book-recommendations').empty()
  response.data.forEach(r_book => {
    $('.book-recommendations').append(`
    <a class="recommended-book" href="${baseUrl}/book/${r_book.slug}">
      <img
        class="recommended-book-cover"
        src="${r_book.image}"
        alt="${r_book.title}"/>
      <div class="recommended-book-title">${r_book.short_title}</div>
    </a>
    

    `)
  });
  
}

$(document).ready(function() {
    checkCart();
    book_id = $('input[name="book-id"]').val()
      $.ajax({
          url: `${baseUrl}/ajax/get-recommended-books/`, 
          method: 'get', 
          data: { 
            book_id : book_id
          },
          success: function(response) {
            checkRecommendations(response);
          },
      });
});