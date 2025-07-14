document.addEventListener('DOMContentLoaded', function(){

    function total_cart_count(){
        fetch('/total-cart-count/')
        .then(response=>response.json())
        .then(data=>{
            if (data.status == "success"){
                console.log(data.data)
                document.getElementById("cart_counter").textContent = data.data;

            }else{
                console.error("Error:", data.message);
            }
        })
        .catch(error => console.error());
    }
    total_cart_count()

    // add to cart
    document.querySelectorAll('.add_to_cart').forEach(button => {
        const id = button.getAttribute('data-id')
        const url = button.getAttribute('data-url')
        console.log(id, url)

        button.addEventListener('click', function(e){
            add_to_cart(e, id, url)
        });
    });
    
    function add_to_cart(e, id, url) {
        e.preventDefault();
        fetch(url)
        .then(response => {
            if (response.status == 401){
                window.location.href = "/accounts/login"
            }
            return response.json()
        })
        .then(data => {
            console.log(data)
            
            total_cart_count()
        })
        .catch(error => console.error());
    }

    // dec to cart
    document.querySelectorAll('.dec_to_cart').forEach(button =>{
        const id = button.getAttribute('data-id')
        const url = button.getAttribute('data-url')
        button.addEventListener('click', function(e){
            dec_to_cart(e, id, url)
        });
    });

    function dec_to_cart(e, id, url){
        e.preventDefault();
            fetch(url)
            .then(response=>{
                if (response.status == 401){
                    window.location.href = "accounts/logout"
                }
                return response.json()
            })
            .then(data =>{
                console.log(data)
                Swal.fire({
                    title: "success",
                    text: "Cart item deleted successfully",
                    icon: "success",
                    draggable: true
                  });
                total_cart_count()
            })
            .catch(error => console.error());
    }
});  

 