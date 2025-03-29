// Get DOM elements
const recommendationForm = document.getElementById('recommendation-form');
const popup = document.getElementById('recommendation-popup');

// Handle form submission
recommendationForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const name = document.getElementById('name').value;
    const position = document.getElementById('position').value;
    const message = document.getElementById('message').value;

    // Create new recommendation card
    const newRecommendation = document.createElement('div');
    newRecommendation.className = 'recommendation-card';
    newRecommendation.innerHTML = `
        <img src="https://via.placeholder.com/100" alt="${name}">
        <div class="recommendation-content">
            <h3>${name}</h3>
            <p>${position}</p>
            <p>"${message}"</p>
        </div>
    `;

    // Add confirmation dialog
    if (confirm('Are you sure you want to submit this recommendation?')) {
        // Add new recommendation to the container
        const recommendationsContainer = document.querySelector('.recommendations-container');
        recommendationsContainer.appendChild(newRecommendation);

        // Reset form
        recommendationForm.reset();

        // Show popup
        showPopup(true);

        // Scroll to the new recommendation
        newRecommendation.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
});

// Show popup function
function showPopup(bool) {
    var popup = document.getElementById('popup');
    if (bool) {
        popup.style.visibility = 'visible';
        popup.style.opacity = '1';
        popup.style.transform = 'translate(-50%, -50%) scale(1)';
    } else {
        popup.style.visibility = 'hidden';
        popup.style.opacity = '0';
        popup.style.transform = 'translate(-50%, -50%) scale(0.8)';
    }
}

// Close popup when clicking outside
document.addEventListener('click', function(e) {
    if (e.target === popup) {
        closePopup();
    }
});

function addRecommendation() {
    // Get the message of the new recommendation
    let recommendation = document.getElementById("new_recommendation");
    
    // If the user has left a recommendation, display a pop-up
    if (recommendation.value != null && recommendation.value.trim() != "") {
        console.log("New recommendation added");
        
        // Create a new 'recommendation' element and set it's value to the user's message
        var element = document.createElement("div");
        element.setAttribute("class", "recommendation");
        element.innerHTML = `<span>&#8220;</span>${recommendation.value}<span>&#8221;</span>`;
        
        // Add this element to the end of the list of recommendations
        let allRecommendations = document.getElementById("all_recommendations");
        if (!allRecommendations) {
            // If the container doesn't exist, create it
            allRecommendations = document.createElement("div");
            allRecommendations.id = "all_recommendations";
            allRecommendations.className = "all_recommendations";
            document.querySelector(".recommendations-container").appendChild(allRecommendations);
        }
        allRecommendations.appendChild(element);

        // Reset the value of the textarea
        recommendation.value = "";
        
        // Show popup
        showPopup(true);
    }
}
  