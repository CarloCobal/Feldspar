const express = require('express');
const path = require('path'); // Ensure this line is present
const { exec } = require("child_process");
const app = express();
const port = 3000;

// ... rest of your server.js code

app.use(express.json());
app.use(express.static('public'));

app.post('/search', async (req, res) => {
    const searchMethod = req.body.searchMethod || "A1"; // Default to A1 if not specified
    const searchTerm = req.body.searchTerm || "default";

    console.log("Search endpoint hit with method:", searchMethod, "and term:", searchTerm);

    try {
        const searchResults = await runPythonScript("Ai/toplink.py", [searchMethod, searchTerm]);
        console.log(searchResults); // Log to verify the structure
        if (searchResults) {
            res.json({ message: 'Search completed', results: searchResults });
        } else {
            throw new Error("No output from Python script");
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: error.message });
    }
});

function runPythonScript(scriptPath, args) {
    return new Promise((resolve, reject) => {
        // Join the arguments with spaces and wrap them in quotes
        const formattedArgs = args.map(arg => `"${arg}"`).join(' ');
        const script = exec(`python3 ${scriptPath} ${formattedArgs}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return reject(`Error: ${error}`);
            }
            console.log('stdout:', stdout);
            console.log('stderr:', stderr);

            try {
                // Attempt to parse stdout as JSON
                const parsedOutput = JSON.parse(stdout.trim());
                resolve(parsedOutput);
            } catch (parseError) {
                console.error(`Error parsing JSON: ${parseError}`);
                console.error(`Problematic output: ${stdout}`);
                reject(`Error parsing JSON: ${parseError}`);
            }
        });
    });
}

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'Feldspar.html'));
});
