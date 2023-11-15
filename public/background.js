document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('searchBar');
    if (searchBar) {
        searchBar.addEventListener('keypress', handleKeyPress);
    }
});

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
        console.log('Server response:', data.message); // Log the server's response
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    return false;
}

function updatePageWithSearchResults(data) {
    for (let i = 0; i < data.results.length; i++) {
        const result = data.results[i];

        const imageDiv = document.getElementById(`rect${i + 1}`);
        const linkElement = document.getElementById(`link${i + 1}`);

        if (imageDiv && result.imageUrl) {
            imageDiv.style.backgroundImage = `url('${result.imageUrl}')`;
        }

        if (linkElement && result.link) {
            linkElement.href = result.link;
        }
    }
}


