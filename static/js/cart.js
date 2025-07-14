document.addEventListener('DOMContentLoaded', function(){

    function total_cart_count(){
        fetch('/total-cart-count/')
        .then(response => response.json())
        .then(data => {
            if (data.status == "success"){
                document.getElementById("cart_counter").textContent = data.data;
            } else {
                console.error("Error:", data.message);
            }
        })
        .catch(error => console.error("Failed to fetch cart count:", error));
    }
    total_cart_count();

    // add to cart
    function addEventListenersToCartButtons() {
        // add to cart
        document.querySelectorAll('.add_to_cart').forEach(button => {
            const id = button.getAttribute('data-id');
            const url = button.getAttribute('data-url');

            button.addEventListener('click', function(e){
                add_to_cart(e, id, url);
            });
        });

        // dec to cart
        document.querySelectorAll('.dec_to_cart').forEach(button => {
            const id = button.getAttribute('data-id');
            const url = button.getAttribute('data-url');
            button.addEventListener('click', function(e){
                dec_to_cart(e, id, url);
            });
        });
    }
    
    function add_to_cart(e, id, url) {
        e.preventDefault();
        fetch(url)
        .then(response => {
            if (response.status == 401){
                window.location.href = "/accounts/login";
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            total_cart_count();
            get_cart(); 
            get_cart_amount();
        })
        .catch(error => console.error("Error adding to cart:", error));
    }

    function dec_to_cart(e, id, url){
        e.preventDefault();
        fetch(url)
        .then(response => {
            if (response.status == 401){
                window.location.href = "/accounts/login"; 
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            Swal.fire({
                title: "Success",
                text: "Cart item deleted successfully",
                icon: "success",
                draggable: true
            });
            total_cart_count();
            get_cart(); 
            get_cart_amount();
        })
        .catch(error => console.error("Error decreasing cart item:", error));
    }

    function get_cart(){
        fetch("/get-cart/")
        .then(response => {
            if (response.status == 401){
                window.location.href = "/accounts/login"; 
            }
            return response.json();
        })
        .then(data => {
            const ul = document.getElementById('food-items');
            ul.innerHTML = "";
            const ulBill = document.getElementById('cart-bill-item');
            ulBill.innerHTML = "";
            data.data.forEach(item => {
                let cartElement = `<li>
                                        <div class="image-holder"> <a href="assets/extra-images/cover-photo12-1024x187.jpg"><img src=${item.image_url} alt="" style="height: 70px; width: 100%;" ></a></div>
                                        <div class="text-holder">
                                            <h6>${item.food_title}</h6>
                                            <span style="width: 90%;">
                                            ${item.food_description}
                                            </span>
                                        </div>
                                        <div class="price-holder" style="display: flex; justify-content: space-between;">
                                                <span class="price" style="padding: 10px;">£${item.food_price}</span>
                                                <a href="" class="dec_to_cart" data-id=${item.food_id} data-url="/dec-to-cart/${item.food_id}/">
                                                    <i class="icon-delete text-color" style="margin: 0px 0 0 4px !important;"></i>
                                                </a>
                                                <label class="cart_quantity" style="margin: 0px 0 0 4px !important;padding: 10px;">
                                                    ${item.quantity}
                                                </label>
                                                <a href="" class="add_to_cart" data-id=${item.food_id} data-url="/add-to-cart/${item.food_id}/" >
                                                    <i class="icon-plus4 text-color" style="margin: 0px 0 0 4px !important;"></i>
                                                </a>
                                        </div>
                                    </li>`;
                
                let cartBillItem = `
                <li>
                    <a href="#" class="btn-cross dev-remove-menu-item"><i class=" icon-cross3"></i></a>
                    <a id="cart-bill-item">${item.food_title}</a>
                    <span class="category-price">£${item.food_price}</span>
                </li>`


                ul.insertAdjacentHTML("beforeend", cartElement);
                ulBill.insertAdjacentHTML("beforebegin", cartBillItem)
            });
            
            // Add event listeners to newly created buttons
            addEventListenersToCartButtons();
        })
        .catch(error => console.error("Error fetching cart:", error));
    }
    get_cart();

    function get_cart_amount(){
        fetch('/get-cart-amount/')
        .then(response=> {
            if (response.status == 401){
                window.location.href = "/accounts/login";
            }
            return response.json();
        })
        .then(data => {
            grand_total=document.getElementById('total-price').textContent = data.grand_total
            sub_total=document.getElementById('sub_total').textContent = data.sub_total
            tax=document.getElementById('').textContent = data.tax
        })
        .catch(error => console.error(error));
    }
    get_cart_amount();
});