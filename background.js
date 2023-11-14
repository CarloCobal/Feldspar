function handleKeyPress(event) {
    if (event.key === "Enter") {
        performSearch();
    }
}

function performSearch() {
    const searchTerm = document.getElementById('searchBar').value;
    
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchTerm: searchTerm }),
    })
    .then(response => response.json())
    .then(data => {
        updatePageWithSearchResults(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    return false; // Prevent default form submission behavior
}

function updatePageWithSearchResults(data) {
    // Here, you will update your webpage based on the search results
    // For example, if you're displaying the results in a div with id 'results'
    // document.getElementById('results').innerHTML = ...;
}
