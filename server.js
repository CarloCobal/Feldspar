const express = require('express');
const path = require('path');
const { exec } = require("child_process");
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

app.post('/search', async (req, res) => {
    const searchTerm = req.body.searchTerm || "default";
    console.log("Search endpoint hit with term:", searchTerm);

    try {
        const searchResults = await runPythonScript("modified_my_googlesearch.py", [searchTerm]);
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
        const script = exec(`python3 ${scriptPath} ${args.join(' ')}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return reject(`Error: ${error}`);
            }
            console.log('stdout:', stdout);
            console.log('stderr:', stderr);
            try {
                resolve(JSON.parse(stdout.trim()));
            } catch (parseError) {
                console.error(`Error parsing JSON: ${parseError}`);
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
