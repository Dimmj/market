const toggleBtn = document.querySelector('.header__toggle');
const menu = document.querySelector('.header__right');

toggleBtn.addEventListener('click', () => {
  menu.classList.toggle('header__right--open');
});








// Находим все карточки товаров на странице
const productCards = document.querySelectorAll('.product-card');

// Добавляем обработчики событий на кнопки "В корзину" и "+" и "-"
productCards.forEach((productCard) => {
  const addToCartBtn = productCard.querySelector('.add-to-cart-btn');
  const minusBtn = productCard.querySelector('.minus-btn');
  const plusBtn = productCard.querySelector('.plus-btn');
  const quantityInput = productCard.querySelector('input[type="text"]');

  // Обработчик события для кнопки "В корзину"
  addToCartBtn.addEventListener('click', () => {
    const productName = productCard.querySelector('.product-name').textContent;
    const productPrice = parseFloat(productCard.querySelector('.product-price').textContent.replace('$', ''));
    const productQuantity = parseInt(quantityInput.value);

    // Отправляем информацию о товаре в корзину (в данном случае выводим информацию в консоль)
    console.log(`Товар "${productName}" добавлен в корзину. Количество: ${productQuantity}. Цена: ${productPrice * productQuantity}$.`);
  });

  // Обработчик события для кнопки "-"
  minusBtn.addEventListener('click', () => {
    let quantity = parseInt(quantityInput.value);
    if (quantity > 1) {
      quantity--;
      quantityInput.value = quantity;
    }
  });

  // Обработчик события для кнопки "+"
  plusBtn.addEventListener('click', () => {
    let quantity = parseInt(quantityInput.value);
    quantity++;
    quantityInput.value = quantity;
  });
});

