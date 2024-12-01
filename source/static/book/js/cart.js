// Получение суммы денег выбранных элементов
function getMoneySumOfSelected() {
  return $('.cart-item.selected').toArray().reduce((total, item) => {
      const price = parseInt($(item).find('input[name="book-price"]').val()) || 0;
      return total + price;
  }, 0);
}

// Получение количества выбранных элементов
function getCountSumOfSelected() {
  return $('.cart-item.selected').toArray().reduce((total, item) => {
      const count = parseInt($(item).find('.cart-item-quantity').text()) || 0;
      return total + count;
  }, 0);
}

// Обновление общей цены и количества внизу страницы
function recountTotalPrice() {
  const $footer = $('.footer');

  if ($('.selected').length === 0) {
      $footer.removeClass('show');
      return
  }

  $footer.addClass('show');

  if ($footer.is(':empty')) {
      $footer.append(`
          <div class="selected-counter">Выбрано: <div id="animated-text1">000000</div></div>
          <hr>
          <div class="selected-sum">Cумма:<div id="animated-text2">000000</div></div>

      `);
  }

  const count = $('.selected').length.toString();
  var money = getMoneySumOfSelected().toString();
  if (count === "0") {money = "0";}
  $('input[name="summary_money"]').val(money);
  
  
  // calculating
  wallet = parseInt($('.cash').text())
  var result = (wallet - parseInt(money)).toString();
  $('input[name="remainder"]').val(result);

  result = `${result} руб.`; 
  money = `${money} руб.`

  shuffleLetters(document.getElementById('animated-text1'), { text: count, iterations: 15, fps: 60 });
  shuffleLetters(document.getElementById('animated-text2'), { text: money, iterations: 15, fps: 60 });  
  shuffleLetters(document.getElementById('summary_price'), { text: money, iterations: 14, fps: 60 });
  shuffleLetters(document.getElementById('result'), { text: result, iterations: 19, fps: 60 });



}

// Получение CSRF токена
function getCSRF() {
  return $('input[name="csrfmiddlewaretoken"]').val();
}

// Активация кнопки "Оформить заказ"
function activeSubmit() {
  
  const isActive = $('.selected').length > 0 
    && $('.address').hasClass('lock') 
    && parseInt($('input[name="remainder"]').val()) >= 0; // Проверяем, что remainder не отрицательный

  // Если значение remainder отрицательное, кнопка всегда inactive
  if (parseInt($('input[name="remainder"]').val()) < 0) {
    $('#place-order').addClass('inactive');
  } else {
    // Убираем класс inactive только если все условия выполнены
    $('#place-order').toggleClass('inactive', !isActive);
  }
}

// Инициализация событий при загрузке документа
$(document).ready(function() {
  inactiveButton();

  $(document).on('click', '.cart-item', function() {
      $(this).toggleClass('selected');
      $(this).closest('.item').find('.cart-item-buttons').toggleClass('selected2');

      
      recountTotalPrice();
      activeSubmit();
  });
});

// Поиск адреса через API
$(document).on('input', '#search-address', function() {
  const apiKey = 'a59ad7523f081b1101a2ed4e384c368ccd2afab3';
  const query = $(this).val();
  
  clearTimeout($.data(this, 'timer'));
  
  const timer = setTimeout(() => {
      $.ajax({
          url: 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/fias',
          type: 'POST',
          contentType: 'application/json',
          headers: { 'Authorization': `Token ${apiKey}` },
          data: JSON.stringify({ query }),
          success: function(data) {
              const suggestions = data.suggestions;
              $('.search-address-box').empty().toggleClass('show', suggestions.length > 0);

              suggestions.forEach(suggestion => {
                  const cls = checkDom(suggestion.value) ? 'suggestion' : 'suggestion inactive';
                  $('.search-address-box').append(`<div class="${cls}" value="${suggestion.value}">${suggestion.value}</div>`);
              });
          },
      });
  }, 600);

  $(this).data('timer', timer);
});

// Показать адреса при фокусе
$(document).on('focus', '#search-address', function() {
  if (!$('.search-address-box').is(':empty')) {
      $('.search-address-box').addClass('show');
  }
});

// Скрыть адреса при потере фокуса
$(document).on("blur", "#search-address", function() {
  setTimeout(() => {
      if (!$(".search-box").is(":hover")) {
          $('.search-address-box').removeClass('show');
      }
  }, 200);
});

// Обработка выбора адреса
$(document).on("click", ".suggestion", function() {
  const selectedValue = $(this).attr('value').trim();
  $('.address').text(selectedValue).css({ 'text-transform': 'none' });
  $('#search-address').val(selectedValue);
  makeAddress();
});

// Функции для формирования и разбора адреса
function unmakeAddress() {
  const $address = $('.address');
  
  if ($address.text() && $address.hasClass('lock')) {
      const parts = $address.text().split(',');
      const flat = parseInt(parts.pop());
      
      $('.flat').val(flat);
      $('#search-address').val(parts.join(','));
  }
}

function makeAddress() {
  const $address = $('.address');
  
  $address.empty();
  
  const dom = $('#search-address').val();
  const kvartira = $('.flat').val();
  
  $address.text(`${dom}, кв. ${kvartira}`).trigger('input');
}

// Проверка домового адреса
function checkDom(string) {
  return /,д|,зд/.test(string.replace(/ /g, ''));
}

function getAddress() {
  const address = $('.address').text();  
  return address;
}


// Обновление адреса на сервере
$(document).on('click', '.locker', function () {

  console.log(getAddress())
  $.ajax({
      url: `${window.location.origin}/ajax/update-address/`,
      type: 'POST',
      data: { csrfmiddlewaretoken: getCSRF(), address: getAddress() },
      success: function(data) {
          $('.address').addClass('lock')
      }
  });
});

// Проверка состояния кнопки "Заблокировать"
function inactiveButton() {
  const $address = $('#search-address').val();
  const $flat = $('.flat').val();
  
  $('.locker').toggleClass('inactive', !$address || !$flat);
}

// Обработка ввода квартиры
$(document).on('input', '.flat', function () {
 if ($('.address').text()) makeAddress();
 inactiveButton();
});

function getSelectedItems(){
  const items = [];
  $('.selected').each(function() {
    const book_id = parseInt($(this).find('input[name="book_id"]').val());
    const book_quantity = parseInt($(this).find('.cart-item-quantity').text());
    const book_price = parseInt($(this).find('.cart-item-price').text());
    
    items.push({'book_id':book_id,'quantity': book_quantity,'price':book_price})
    
    
    


    afterResult = $('#result').text()
    shuffleLetters(document.getElementById('cash'), { text: afterResult, iterations: 10, fps: 60 });
    shuffleLetters(document.getElementById('summary_price'), { text: '0 руб.', iterations: 12, fps: 60 });
    shuffleLetters(document.getElementById('result'), { text: afterResult, iterations: 14, fps: 60 });

    $(this).closest('.item').remove(); // Удаляем родительский элемент .item
    $('#place-order').addClass('inactive')
    $('.footer').removeClass('show')

  });
  return items

}

$(document).on('click', '#place-order', function () {
  
  $.ajax({
    url: `${window.location.origin}/ajax/place-order/`,
    type: 'POST',
    data: { 
          csrfmiddlewaretoken: getCSRF(), 
          items: JSON.stringify(getSelectedItems()) ,
          address: getAddress()},
    success: function(data) {
      loadOrdersList()
    }
  })





})


$(document).ready(function() {
  loadOrdersList()
})

function loadOrdersList() {
  $.ajax({
    url: `${window.location.origin}/ajax/get-orders/`,  // Используйте имя URL, которое вы указали в urls.py
    type: "GET",
    dataType: "json",
    success: function(response) {
      var orders = response.orders;
      $('.orders-list').empty(); // Очистка контейнера заказов
      $.each(orders, function(index, order) {
        console.log(order)
          
          var orderHtml = '<div class="order">';
          orderHtml += '<h3>Заказ #' + order.order_id + '</h3>';
          
          
          orderHtml += '<ul>';
          $.each(order.items, function(i, item) {
              orderHtml += '<li>' + item.title + '<span>'+ item.quantity + 'шт.</span></li>';
          });
          orderHtml += '</ul>';
          orderHtml += '<div class="itogo" >';

          orderHtml += '<p>' + order.total_price + ' руб.</p>';
          orderHtml += '<span>' + formatDate(order.arrival_date) + '</span>';

          
          orderHtml += '</div>';


          orderHtml += '</div>';

          

          $('.orders-list').append(orderHtml); // Предполагается, что у вас есть контейнер с id="orders-container"
      });
        
    },
  });

}

function quantityMinus(cart_item_id) {
  
  $.ajax({
    url: `${window.location.origin}/ajax/quantity-minus/`,  // Используйте имя URL, которое вы указали в urls.py
    type: "POST",
    data: {
      csrfmiddlewaretoken : getCSRF(),

      cart_item_id : cart_item_id
    },
  }
)}

function quantityPlus(cart_item_id) {
  $.ajax({
    url: `${window.location.origin}/ajax/quantity-plus/`,  // Используйте имя URL, которое вы указали в urls.py
    type: "POST",
    data: {
      csrfmiddlewaretoken : getCSRF(),
      cart_item_id : cart_item_id
    },
  }
)}





$(document).ready(function() {
  $('.left-arrow').on('click', function() {
      // Находим родительский элемент .item
      var itemContainer = $(this).closest('.item');
      
      // Находим элемент с количеством
      var quantityElement = itemContainer.find('.cart-item-quantity');
      
      // Получаем текущее количество
      var currentQuantity = parseInt(quantityElement.text());
      cart_item_id = itemContainer.find('input[name="cart_item_id"]').val()
      // Уменьшаем количество, если оно больше 1
      if (currentQuantity > 1) {
          currentQuantity--;
          quantityMinus(cart_item_id);

          var pricePerUnit = parseInt(itemContainer.find('input[name="std-book-price"]').val()); // Получаем цену за единицу
          var newPrice = currentQuantity * pricePerUnit;
          itemContainer.find('.cart-item-price').text(newPrice + ' руб.');
          itemContainer.find('input[name="book-price"]').val(newPrice); // Обновляем цену



          quantityElement.text(currentQuantity); // Обновляем отображение количества
          recountTotalPrice();

      }
  });

  $('.right-arrow').on('click', function() {
      // Находим родительский элемент .item
      var itemContainer = $(this).closest('.item');
      
      // Находим элемент с количеством
      var quantityElement = itemContainer.find('.cart-item-quantity');
      
      // Получаем текущее количество
      var currentQuantity = parseInt(quantityElement.text());
      cart_item_id = itemContainer.find('input[name="cart_item_id"]').val()
      // Увеличиваем количество
      currentQuantity++;
      quantityPlus(cart_item_id);

      var pricePerUnit = parseInt(itemContainer.find('input[name="std-book-price"]').val()); // Получаем цену за единицу
      var newPrice = currentQuantity * pricePerUnit;
      itemContainer.find('.cart-item-price').text(newPrice + ' руб.'); // Обновляем цену
      itemContainer.find('input[name="book-price"]').val(newPrice);
      quantityElement.text(currentQuantity); // Обновляем отображение количества

      recountTotalPrice();
  });
});


function removeCartItem(cart_item_id) {
  
  $.ajax({
    url: `${window.location.origin}/ajax/remove-cart-item/`,  // Используйте имя URL, которое вы указали в urls.py
    type: "POST",
    data: {
      csrfmiddlewaretoken : getCSRF(),
      cart_item_id : cart_item_id
    },
  }
)}


$(document).on('click','.trash', function() {
  var itemContainer = $(this).closest('.item');
  
  cart_item_id = itemContainer.find('input[name="cart_item_id"]').val()
  itemContainer.remove();
  removeCartItem(cart_item_id);
  recountTotalPrice();
});


function formatDate(dateString) {
  // Преобразование строки в объект Date
  var dateObject = new Date(dateString);
  
  // Форматирование даты в нужный вид
  var options = { year: 'numeric', month: 'long', day: 'numeric' };
  var formattedDate = dateObject.toLocaleString('ru-RU', options);
  
  return formattedDate;
}