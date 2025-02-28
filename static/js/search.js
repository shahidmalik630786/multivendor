


document.addEventListener('DOMContentLoaded', function(){

    function searchResult(){
        debugger
        const rest_name = document.getElementById("rest_name").value.trim() || "None";
        const location = document.getElementById("location").value.trim() || "None";
        
        fetch(`/search-result/${rest_name}/${location}`)
        .then(response=>{
            if (response.status == 401){
                // window.location.href = "/accounts/login";
                console.log("*********")
            }
            return response.json();
        })
        .then(data=>{
            const ul = document.getElementById("search-result")
            ul.innerHTML="";
            data.data.forEach(item => {
                let serachHtml = `
                    <li>
                        <div class="img-holder">
                        <figure>
                            <a href="#">
                                <img src="${item.user_profile}" class="img-list wp-post-image" alt="">
                            </a>
                        </figure>
                            <span class="restaurant-status close"><em class="bookmarkRibbon"></em>Close</span>
                        </div>
                        <div class="text-holder">
                            <div class="list-rating">
                                <div class="rating-star">
                                    <span class="rating-box" style="width: 100%;"></span>
                                </div>
                                <span class="reviews">(1)</span>
                            </div>
                            <div class="post-title">
                                <h5>
                                    <a href="/marketplace/${item.restaurant_slug}">${item.restaurant_name}</a>
                                    <!-- <span class="sponsored text-color">Sponsored</span> -->
                                </h5>
                            </div>
                            <div class="delivery-potions">
                                <div class="post-time">
                                    <i class="icon-motorcycle"></i>
                                    <div class="time-tooltip">
                                        <div class="time-tooltip-holder"> <b class="tooltip-label">Delivery
                                                time</b> <b class="tooltip-info">Your order will
                                                be
                                                delivered in 10 minutes.</b> </div>
                                    </div>
                                </div>
                                <div class="post-time">
                                    <i class="icon-clock4"></i>
                                    <div class="time-tooltip">
                                        <div class="time-tooltip-holder"> <b class="tooltip-label">Pickup
                                                time</b> <b class="tooltip-info">You
                                                can pickup order in
                                                15 minutes.</b> </div>
                                    </div>
                                </div>
                                <span>${item.location}</span>
                            </div>
                        </div>
                        <div class="list-option">
                        </div>
                    </li>`

                ul.insertAdjacentHTML("beforeend", serachHtml);
            });


        })
        .catch(error=>console.error(error))
        
    }

    searchResult()

    document.getElementById("rest_name").addEventListener('keyup', searchResult);
    document.getElementById("location").addEventListener('keyup', searchResult);

})