document.addEventListener('DOMContentLoaded', function() {
    const addressInput = document.getElementById('id_address');
    if (!addressInput) {
        console.error('Address input element not found');
        return;
    }

    addressInput.addEventListener("input", function() {
        let address = this.value.trim();
        let suggestionsList = document.getElementById("suggestions");

        if (!address) {
            suggestionsList.innerHTML = ""; // Clear suggestions if input is empty
            return;
        }

        fetch(`https://maps.gomaps.pro/maps/api/place/autocomplete/json?input=${encodeURIComponent(address)}&key=AlzaSy4QJVPKSckZ8mUNL4HA1ciPuEeDS8qrvMx`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            // Clear old suggestions
            suggestionsList.innerHTML = "";

            // Check if predictions exist
            if (data.predictions && data.predictions.length > 0) {
                data.predictions.forEach((place) => {
                    let listItem = document.createElement("li");
                    listItem.textContent = place.description;
                    listItem.style.cursor = "pointer";
                    listItem.onclick = function() {
                        addressInput.value = place.description;
                        suggestionsList.innerHTML = ""; // Clear suggestions after selection
                        console.log(place.terms)
                    };
                    suggestionsList.appendChild(listItem);
                });
            } else {
                suggestionsList.innerHTML = "<li>No suggestions found</li>";
            }
        })
        .catch(error => console.error("Error:", error));
    });
});