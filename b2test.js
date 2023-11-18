// Assuming you've already defined 'runPythonScript' and 'captureScreenshot' functions

app.post('/b2search', async (req, res) => {
    const searchTerm = req.body.searchTerm || "default";

    try {
        // Call B2loop.py with the searchTerm
        const b2Result = await runPythonScript("Ai/B2loop.py", [searchTerm]);

        if (b2Result && b2Result.result) {
            // Use the result from B2loop.py as the query for toplink.py
            const searchResults = await runPythonScript("Ai/toplink.py", ["B2", b2Result.result]);

            if (searchResults && searchResults.url) {
                // If toplink.py returns a URL, capture a screenshot
                const screenshotPath = await captureScreenshot(searchResults.url, 'B2');
                res.json({
                    message: 'B2 Search completed',
                    screenshotPath: screenshotPath,
                    url: searchResults.url
                });
            } else {
                res.json({ error: "Toplink script did not return a valid URL" });
            }
        } else {
            res.json({ error: "B2 script did not return a valid result" });
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: error.message });
    }
});

// Testing the B2 search functionality
runPythonScript('Ai/B2loop.py', ['sample search term'])
    .then(result => console.log('Result:', result))
    .catch(error => console.error('Error:', error));
