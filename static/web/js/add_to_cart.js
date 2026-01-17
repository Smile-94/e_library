document.addEventListener('DOMContentLoaded', function () {
  document.body.addEventListener('click', function (event) {
    const target = event.target.closest('.add-to-cart-btn');
    if (!target) return;

    event.preventDefault();
    const productId = target.dataset.productId;
    const csrfToken = document.getElementById('csrf-token').value;

    fetch("{% url 'order:add_to_cart' %}", {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `product_id=${productId}&quantity=1`
    })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'unauthenticated') {
        window.location.href = data.redirect_url;
        return;
      }

      // Optional: show message or update UI
      alert(data.message);

      // Update Add to Cart button UI
      if (data.status === 'success') {
        target.innerHTML = '<i class="fa fa-check"></i> Added';
        target.classList.add('disabled');
      }

      // Update header cart count dynamically
      if (data.cart_total_items !== undefined) {
        const cartCountElem = document.getElementById('header-cart-count');
        if (cartCountElem) {
          cartCountElem.textContent = data.cart_total_items;
        }
      }
    })
    .catch(() => alert('Request failed'));
  });
});