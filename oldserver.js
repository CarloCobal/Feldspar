const express = require('express');
const path = require('path');
const fs = require('fs');
const { exec } = require("child_process");
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

app.post('/search', async (req, res) => {
    console.log("Search endpoint hit with term:", req.body.searchTerm);
    try {
        const searchTerm = req.body.searchTerm;
        const searchResults = await processSearch(searchTerm);
        res.json({ message: 'Search completed', results: searchResults.results });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'An error occurred' });
    }
});


async function processSearch(searchTerm) {
    try {
        const chatOutput = await runPythonScript("Ai/simpleChat.py", [searchTerm]);
        console.log("simpleChat.py Output:", chatOutput);

        const { firstThree, lastThree } = parseChatOutput(chatOutput);
        const searchResults = [];

        // Process first three for images
        for (const result of firstThree) {
            const imageOutput = await runPythonScript("Ai/imgGen.py", [result]);
            const imageUrl = extractImgUrl(imageOutput);

            searchResults.push({
                title: result,
                imageUrl: imageUrl,
                link: '' // Placeholder for link
            });
        }

        // Process last three for links
        for (const result of lastThree) {
            console.log("Fetching link for:", result);
            const googleSearchOutput = await runPythonScript("my_googlesearch.py", [result]);
            const googleSearchData = JSON.parse(googleSearchOutput);
            const correspondingResult = searchResults.find(r => r.title === result);
            
            if (correspondingResult) {
                correspondingResult.link = googleSearchData.top_link;
            }
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
    const lines = chatOutput.split('\n').filter(line => /^\d\./.test(line));
    const firstThree = lines.slice(0, 3);
    const lastThree = lines.slice(3, 6);
    console.log("First three for images:", firstThree);
    console.log("Last three for links:", lastThree);
    return { firstThree, lastThree };
}


function extractImgUrl(imgGenOutput) {
    try {
        const imgGenData = JSON.parse(imgGenOutput);
        return imgGenData.url;
    } catch (error) {
        console.error("Error parsing image generation output:", error);
        return null;
    }
}



app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'Feldspar.html'));
});
