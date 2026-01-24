document.addEventListener("DOMContentLoaded", () => {
  const csrfToken = document.getElementById("csrf_token").value;

  function updateCart(itemId, quantity) {
    fetch("/cart/update/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({ item_id: itemId, quantity: quantity }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
          row.querySelector(".item-total").innerText = `৳ ${data.item_total}`;

          // Update cart summary
          document.getElementById("cart-total").innerText = data.cart_total;
          document.getElementById("cart-discount").innerText =
            data.cart_discount;
          document.getElementById("cart-net-amount").innerText =
            data.cart_net_amount;

          // ✅ Update header cart
          document.getElementById("header-cart-count").innerText =
            data.cart_count;
          document.getElementById(
            "header-cart-total"
          ).innerText = `৳ ${data.cart_total}`;
        }
      });
  }

  document.querySelectorAll(".qty-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const row = btn.closest("tr");
      const input = row.querySelector(".qty-input");
      let qty = parseInt(input.value);

      if (btn.classList.contains("plus")) qty++; // qty = qty + 2
      if (btn.classList.contains("minus") && qty > 1) qty--;

      input.value = qty;
      updateCart(row.dataset.itemId, qty);
    });
  });

  document.querySelectorAll(".qty-input").forEach((input) => {
    input.addEventListener("change", () => {
      const row = input.closest("tr");
      updateCart(row.dataset.itemId, input.value);
    });
  });

  document.querySelectorAll(".remove-item").forEach((btn) => {
    btn.addEventListener("click", () => {
      const row = btn.closest("tr");

      fetch("/cart/remove/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ item_id: row.dataset.itemId }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            row.remove();

            // Update cart summary
            document.getElementById("cart-total").innerText = data.cart_total;
            document.getElementById("cart-discount").innerText =
              data.cart_discount;
            document.getElementById("cart-net-amount").innerText =
              data.cart_net_amount;

            // ✅ Update header cart
            document.getElementById("header-cart-count").innerText =
              data.cart_count;
            document.getElementById(
              "header-cart-total"
            ).innerText = `৳ ${data.cart_total}`;
          }
        });
    });
  });
});
