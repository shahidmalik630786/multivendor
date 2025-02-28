serachHtml = `
 <li>
                                        <div class="img-holder">
                                            <figure>
                                                <a href="#">
                                                    {% if vendor.user_profile.profile_picture %}
                                                    <img src="{{vendor.user_profile.profile_picture.url}}" class="img-list wp-post-image" alt="">
                                                    {% else %}
                                                    <img class="thumbnail" src="{% static 'assets/images/default-food.png' %}" alt="profile photo">
                                                    {% endif %}
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
                                                    <a href="{% url 'marketplace:vendor-detail' vendor.restaurant_slug %}">{{ vendor.restaurant_name }}</a>
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
                                                <span>{{ vendor.user_profile.address }}</span>
                                            </div>
                                        </div>
                                        <div class="list-option">
                                            <a href="javascript:void(0);" class="shortlist-btn" data-toggle="modal" data-target="#sign-in"><i class="icon-heart4"></i> </a>
                                            <a href="{% url 'marketplace:vendor-detail' vendor.restaurant_slug %}" class="viewmenu-btn text-color">View Menu</a>
                                        </div>
                                    </li>`


document.addEventListener('DOMContentLoaded', function(){

    

    function searchResult(){
        const rest_name =document.getElementById("rest_name").value
        const location = document.getElementById("location").value
        
        fetch("/search-result/${rest_name}/${location}")
        .then(response=>response.json)
        .then(data=>{
            console.log(data)
        })
        .catch(error=>console.error(error))
        
    }

    searchResult()

})