const express = require('express');
const path = require('path');
const fs = require('fs');
const { exec } = require("child_process");
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

app.post('/search', async (req, res) => {
    const searchTerm = req.body.searchTerm;
    console.log("Received search term:", searchTerm);

    try {
        const results = await processSearch(searchTerm);
        res.json({ message: 'Search completed', results: results });
      } catch (error) {
        console.error("Error in /search route:", error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

async function processSearch(searchTerm) {
    try {
        const chatOutput = await runPythonScript("Ai/simpleChat.py", [searchTerm]);
        console.log("simpleChat.py Output:", chatOutput);

        // Declare the searchResults array to store the results
        const searchResults = [];

        const parsedResults = parseChatOutput(chatOutput);

        for (const result of parsedResults) {
            const googleSearchOutput = await runPythonScript("./my_googlesearch.py", [result]);
            console.log(`Top search result for "${result}":`, googleSearchOutput);
            // Call imgGen.py for each title

            const imageOutput = await runPythonScript("Ai/imgGen.py", [result]);
            const imageUrl = extractImgUrl(imageOutput);

            // console.log(`Image URL for "${result}":`, imageOutput);

            searchResults.push({
                title: result,
                link: googleSearchOutput.top_link,
                imageUrl: imageUrl // Use the extracted image URL
            });
        }

        return { message: 'Search processed', results: searchResults };
    } catch (error) {
        console.error("Error in processSearch:", error);
        throw error;
    }
}


function runPythonScript(scriptPath, args) {
    return new Promise((resolve, reject) => {
        const script = exec(`python ${scriptPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return reject(error);
            }
            if (stderr) {
                console.error(`stderr: ${stderr}`);
                return reject(stderr);
            }
            resolve(stdout);
        });

        // Write the arguments as input to the script
        script.stdin.write(args.join(' '));
        script.stdin.end();
    });
}


function parseChatOutput(chatOutput) {
    const results = [];
    const searchTerms = chatOutput.split('\n').filter(line => /^\d\./.test(line));

    for (const term of searchTerms) {
        const match = term.match(/^\d\.\s*(.+)/);
        if (match && match[1]) {
            results.push(match[1].trim());
        }
    }

    return results;
}


function extractImgUrl(imgGenOutput) {
    try {
        // Assuming imgGen.py outputs JSON with a structure like { "url": "http://image.url" }
        const imgGenData = JSON.parse(imgGenOutput);
        return imgGenData.url; // Extract the URL
    } catch (error) {
        console.error("Error parsing image generation output:", error);
        return null; // Return null or a default image URL if parsing fails
    }
}

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'Feldspar.html'));
});
