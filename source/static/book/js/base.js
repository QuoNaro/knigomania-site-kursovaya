function getCookie() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = jQuery.trim(cookies[i]);

      if (cookie.startsWith(csrfmiddlewaretoken + "=")) {
        cookieValue = decodeURIComponent(
          cookie.substring(csrfmiddlewaretoken.length + 1)
        );
        break;
      }
    }
  }
  return cookieValue;
}

function getUserId() {
  return $('input[name="user_id"]').val();
}

function truncateString(str, maxLength = 30) {
  if (str.length > maxLength) {
    let trimmed = str.slice(0, maxLength);
    if (str[maxLength] !== " ") {
      trimmed = trimmed.slice(0, trimmed.lastIndexOf(" "));
    }
    return trimmed + "...";
  }
  return str;
}

$(document).ready(function () {
  setTimeout(function () {
    value = $("#search-input").val();
    performSearch(value);
  }, 500);


  $(".block-for-what").on("click",function () {
    $(".start-notification").removeClass("hide");
  });

  $(document).on("click", ".start-notification", function () {
    $(this).addClass("hide");
  });

  $(document).on("click", ".menu-button", function () {
    $(".menu").addClass("show");

    var substrateMenu = $(".substrate-menu");

    substrateMenu.css("display", "flex");
    setTimeout(function () {
      substrateMenu.addClass("show");
    }, 10);
  });

  $(document).on("click", ".substrate-menu", function () {
    $(".menu").removeClass("show");

    var element = $(this);
    element.removeClass("show");

    setTimeout(function () {
      element.css("display", "none");
    }, 700);
  });

  $(document).on("input", "#search-input", function () {
    var $this = $(this);

    // Clear any existing timeout to debounce input
    if ($this.data("timeout")) {
      clearTimeout($this.data("timeout"));
    }

    var query = $this.val();
    baseUrl = window.location.origin;

    // Show or hide the search box based on input
    if (query.length > 0) {
      $(".search-box").addClass("show"); // Show the search box
    } else {
      $(".search-box").removeClass("show"); // Hide the search box if input is empty
      $(".search-box").empty(); // Clear previous results
      return; // Exit if there's no query
    }

    // Set a timeout for AJAX call to avoid excessive requests
    $this.data(
      "timeout",
      setTimeout(function () {
        performSearch(query); // Call the function to perform the search
      }, 400)
    );
  });

  $(document)
    .on("focus", "#search-input", function () {
      $(".search-box").addClass("show");
    })
    .on("keydown", "#search-input", function (event) {
      if ($(this).is(":focus")) {
        let query = $(this).val();

        // Validate query for unwanted characters or terms
        if (
          /[/\\]/.test(query) ||
          query.toLowerCase() === "none" ||
          query === ".."
        ) {
          query = "";
        }

        // Handle Enter key press for search redirection
        if (event.key === "Enter" && !(query.trim() === "")) {
          event.preventDefault();
          var baseUrl = window.location.origin;
          window.location.href = `${baseUrl}/book/search/${query}`;
        }
      }
    });

  $(document).on("blur", "#search-input", function () {
    // Use a timeout to allow clicks on search results
    setTimeout(function () {
      if (!$(".search-box").is(":hover")) {
        // Check if mouse is not over .search-box
        $(".search-box").removeClass("show");
      }
    }, 200); // Adjust timeout as needed
  });

  function performSearch(query) {
    var baseUrl = window.location.origin;

    $.ajax({
      url: `${baseUrl}/ajax/search`,
      type: "GET",
      data: { query: query },
      success: function (data) {
        
        if (data.books.length === 0) {
          $(".search-box").empty();
          $(".search-box").append(`
            <img src="${location.origin}/static/book/img/kitty.svg" alt="Нет результатов поиска">
            <p class="no-results">Поиск не дал результатов</p>`

          );
          $('.search-box').css({
            'dislpay': 'flex',
            'flex-direction': 'row',
            'align-items':'center',
          })
          $('.search-box').find('img').css({
            'width': '70px',
            'height': 'auto'
          })

          $('.search-box').find('.no-results').css({
            'width': '100%',
            'display': 'flex',
            'justify-content' :'center',
            'align-items': 'center',
          })

          return;
        }
        $(".search-box").empty();
        $('.search-box').removeAttr('style');
        let delay = 0;
        data.books.forEach((book, index) => {
          setTimeout(() => {
            $(".search-box").append(`
                        <a class="search-row" href="${location.origin}/book/${book.slug}">
                          <img class="search-row-image" src="${book.image}" alt="">
                          <div class="search-row-info">
                            <p class="search-row-title">${book.short_title}</p>
                            <p class="search-row-author">${book.author_name}</p>
                          </div>
                        </a>
                        <hr>
                    `);

            // Если это последняя книга, добавляем ссылку "Показать больше результатов"
            if (index === data.books.length - 1 && data.books.length > 0) {
              setTimeout(() => {
                $(".search-box").append(`
                                <a href="${location.origin}/book/search/${query}" class="show-more-results">Показать больше результатов</a>
                            `);
              }, 100); // Небольшая дополнительная задержка для "Показать больше результатов"
            }
          }, delay);
          delay += 100; // Увеличиваем задержку для каждой следующей книги
        });
      },
    });
  }
});
