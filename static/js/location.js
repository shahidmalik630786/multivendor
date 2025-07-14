let isPopulateAddressFetching = false;

function init(activeMenu) {
    setActive(activeMenu);
    // Remove automatic location fetching from init
    // getLocation();
}
  
function setActive(activeMenu) {
    const menuElement = document.querySelector(`#${activeMenu}`);
    if (menuElement) {
      menuElement.classList.add('active');
    }
}

// Single location fetch on page load
document.addEventListener("DOMContentLoaded", function () {
    // Get current position once when page loads
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                
                const latInput = document.getElementById("id_latitude");
                const lonInput = document.getElementById("id_longitude");
                
                // Only set if fields exist and are empty/default
                if (latInput && lonInput) {
                    if (!latInput.value || latInput.value === '0.0' || latInput.value === '') {
                        latInput.value = lat;
                    }
                    if (!lonInput.value || lonInput.value === '0.0' || lonInput.value === '') {
                        lonInput.value = lon;
                    }
                }
                
                console.log("Initial Latitude:", lat);
                console.log("Initial Longitude:", lon);
            },
            function (error) {
                console.error("Error getting location:", error.message);
                // Handle different error cases
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        console.error("User denied the request for Geolocation.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        console.error("Location information is unavailable.");
                        break;
                    case error.TIMEOUT:
                        console.error("The request to get user location timed out.");
                        break;
                }
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            }
        );
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
});

// Get address button click handler
document.addEventListener("DOMContentLoaded", async function () {
    // populate the address on page loads
    await populateAddress().then(() => {
            redirectToSearch();
        });
    const getAddressBtn = document.getElementById("id_get_address");
    if (getAddressBtn) {
        getAddressBtn.addEventListener("click", function () {
            if (!isPopulateAddressFetching) {
                populateAddress();
            }
        });
    }
});

// Reverse geocoding function
function populateAddress() {
    isPopulateAddressFetching = true;

    return new Promise((resolve, reject) => {
        const iconSpan = document.getElementById("id_get_address");
        if (iconSpan) {
            iconSpan.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`;
        }

        get_current_lat_long(function(lat, lon) {
            if (!lat || !lon || isNaN(lat) || isNaN(lon) || lat === 0.0 || lon === 0.0) {
                console.error("Invalid coordinates:", lat, lon);
                isPopulateAddressFetching = false;
                if (iconSpan) iconSpan.textContent = "📍";
                return reject("Invalid coordinates");
            }

            const params = new URLSearchParams({ lat: lat.toString(), lon: lon.toString() });

            fetch("/accounts/api/get-address/?" + params.toString())
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                    return res.json();
                })
                .then(response => {
                    const addressInput = document.getElementById("id_address");
                    if (addressInput && response.address) {
                        addressInput.value = response.address;
                        // Set lat/lng as well (if needed)
                        document.getElementById("id_latitude").value = lat;
                        document.getElementById("id_longitude").value = lon;
                        resolve();
                    } else {
                        reject("No address received");
                    }
                })
                .catch(err => {
                    console.error("Error fetching address:", err);
                    reject(err);
                })
                .finally(() => {
                    isPopulateAddressFetching = false;
                    if (iconSpan) iconSpan.textContent = "📍";
                });
        });
    });
}


// Auto address suggestion
document.addEventListener("DOMContentLoaded", function () {
    const addressInput = document.getElementById("id_address");
    const addressSuggestions = document.getElementById("addressSuggestions");
    
    if (!addressInput || !addressSuggestions) {
        console.warn("Address input or suggestions container not found");
        return;
    }
    
    const suggestionsBox = document.createElement("ul");
    suggestionsBox.classList.add("list-group", "position-absolute", "w-100");
    suggestionsBox.style.zIndex = "1000";
    suggestionsBox.style.top = "100%";
    suggestionsBox.style.maxHeight = "200px";
    suggestionsBox.style.overflowY = "auto";

    // Insert suggestions box after the address input
    addressInput.parentNode.insertBefore(suggestionsBox, addressInput.nextSibling);

    let debounceTimer = null;

    addressInput.addEventListener("input", function () {
        const query = addressInput.value.trim();
        if (query.length < 2) {
            suggestionsBox.innerHTML = "";
            return;
        }

        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            fetchSuggestions(query);
        }, 300);
    });

    function fetchSuggestions(query) {
        fetch(`https://api.radar.io/v1/search/autocomplete?query=${encodeURIComponent(query)}`, {
            headers: {
                "Authorization": "prj_test_pk_870ea00220d6f8d6ca0ca4f1997d0a0220a56fd8"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            suggestionsBox.innerHTML = "";
            if (data.addresses && data.addresses.length) {
                data.addresses.forEach(addr => {
                    const li = document.createElement("li");
                    li.className = "list-group-item list-group-item-action";
                    li.style.cursor = "pointer";
                    li.textContent = addr.formattedAddress;
                    li.addEventListener("click", () => {
                        addressInput.value = addr.formattedAddress;
                        
                        // Update coordinates when address is selected
                        const latInput = document.getElementById("id_latitude");
                        const lonInput = document.getElementById("id_longitude");
                        
                        if (latInput && addr.latitude) {
                            latInput.value = addr.latitude;
                        }
                        if (lonInput && addr.longitude) {
                            lonInput.value = addr.longitude;
                        }
                        
                        suggestionsBox.innerHTML = "";
                        
                        console.log("Address selected:", addr.formattedAddress);
                        console.log("Updated coordinates:", addr.latitude, addr.longitude);
                    });
                    suggestionsBox.appendChild(li);
                });
            }
        })
        .catch(err => {
            console.error("Radar autocomplete error:", err);
            suggestionsBox.innerHTML = "";
        });
    }

    // Hide suggestions when user clicks elsewhere
    document.addEventListener("click", function (e) {
        if (!addressInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.innerHTML = "";
        }
    });
});

// Legacy functions (remove if not used elsewhere)
function getLocation() {
    // This function is now handled in DOMContentLoaded
    console.warn("getLocation() is deprecated, location is now fetched on page load");
}

function showPosition(position) {
    // This function is now handled in DOMContentLoaded
    console.warn("showPosition() is deprecated, position handling is now in DOMContentLoaded");
}


function get_current_lat_long(callback) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;

                // Optionally update the inputs if needed
                document.getElementById("id_latitude").value = lat;
                document.getElementById("id_longitude").value = lon;

                callback(lat, lon);
            },
            function (error) {
                console.error("Error getting location:", error.message);
                callback(null, null);  // Indicate failure
            }
        );
    } else {
        console.error("Geolocation is not supported by this browser.");
        callback(null, null);
    }
}