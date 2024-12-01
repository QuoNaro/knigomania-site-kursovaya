

function truncateString(str, maxLength = 30) {
  if (str.length > maxLength) {
      // Обрезаем строку до последнего пробела перед maxLength
      let trimmed = str.slice(0, maxLength);
      if (str[maxLength] !== ' ') {
          trimmed = trimmed.slice(0, trimmed.lastIndexOf(' '));
      }
      return trimmed + '...'; // Добавляем многоточие
  }
  return str; // Возвращаем строку без изменений, если она короче maxLength
}



$(document).on('click', '.up-button',  function () {
  $('html, body').animate({ scrollTop: 0 }, 'fast');
})

$(document).ready(function () {
  var offset = 0;
  var limit = 30;
  var loading = false;
  var $container = $(".books");

  var load_more_url = getFilterUrl();
  
  function loadMore() {
    if (loading) return;
    loading = true;


    $.ajax({
      url: load_more_url,
      data: { 
        offset: offset,  
        limit: limit ,
        
      },
      dataType: "json",
      success: function (data) {
        if (data.items.length > 0) {
          $.each(data.items, function (index, item) {
            var short_title = truncateString(item.title);
            var bookHtml = `
                <a href="book/${item.slug}" class="book">
                    <div class="loading-placeholder"></div>
                    <div class="img"></div>
                    <div class="name">${short_title}</div>
                    <div class="author">${item.author_name}</div>
                    <div class="price">  ${item.price} руб.</div>

                </a>
            `;
            var $bookElement = $(bookHtml);
            $container.append($bookElement);
        
            // Создаем новый объект изображения для кэширования
            var img = new Image();
            
            // Устанавливаем обработчик события загрузки
            $(img).on('load', function() {
                // Устанавливаем изображение как фон для div.img
                $bookElement.find('.img').css({
                    'background-image': 'url(' + item.image + ')',
                    'background-size': 'cover', // Подгоняем изображение под размер div
                    'background-position': 'center', // Центрируем изображение
                    'display': 'flex' // Убедитесь, что div отображается
                });
                
                // Удаляем текст загрузки
                $bookElement.find('.loading-placeholder').remove();
            }).on('error', function() {
                // Обработка ошибки загрузки
                $bookElement.find('.loading-placeholder').text("Ошибка загрузки изображения");
            });
        
            // Задаем источник изображения для начала загрузки
            img.src = item.image;
        });
          offset += limit;
        }
        if (!data.has_more) {
          $(window).off("scroll", checkScroll);
        }
        loading = false;
      },
      error: function () {
        loading = false; // Устанавливаем флаг загрузки в false при ошибке
      },
    });
  }

  function checkScroll() {
    if (
      $(window).scrollTop() + $(window).height() >=
      $(document).height() - 200
    ) {
      loadMore();
    }
  }

  $(window).on("scroll", checkScroll);
  loadMore();
  
  $('.author-filter-select').select2({
    placeholder: "Авторы",
    maximumSelectionLength: 5,
    allowClear: true 
  });

  $('.genre-filter-select').select2({
    placeholder: "Жанры",
    maximumSelectionLength: 5,
    allowClear: true 
  });

  //tags select
  $('.tag-filter-select').select2({
    placeholder: "Теги",
    maximumSelectionLength: 5,
    allowClear: true, 
  });

  $(document).on('click','button[type="submit"]',function (e) {
    load_more_url = getFilterUrl();
    $('.books').empty();
    offset = 0;
    limit = 30;
    loadMore();
  });

  $(document).on('change','input[type="number"]', function () {
    value = Math.abs(parseInt($(this).val()));
    $(this).val(value);
  });

  
  $(document).on('click','button[type="reset"]', function (){
    
    $(".tag-filter-select").val(null).trigger('change')
    $(".genre-filter-select").val(null).trigger('change')
    $(".author-filter-select").val(null).trigger('change')
    $("input[type='number']").val(null)
    load_more_url = getFilterUrl();
    $('.books').empty();
    offset = 0;
    limit = 30;
    loadMore();

  })


});

function getFilters() {
  var f_author = $('.author-filter-select').val();
  var f_genre = $('.genre-filter-select').val();
  var f_tag = $('.tag-filter-select').val();
  var f_price = $('.up-to-price input[type="number"]').val();
  return [f_author,  f_genre, f_tag , f_price];
}

function getFilterUrl() {
  const filters = getFilters();

  function encodeFilter(value) {
    if (Array.isArray(value) && value.length === 0) {
      return 'None';
    }
    return value ? encodeURIComponent(value) : 'None';
  }

  return '/ajax/load-books/?' + 
    'author_id=' + encodeFilter(filters[0]) + 
    '&genre=' + encodeFilter(filters[1]) + 
    '&tag=' + encodeFilter(filters[2]) + 
    '&price=' + encodeFilter(filters[3]) + 
    '&offset=0&limit=30';
}

