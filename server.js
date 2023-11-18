import express from 'express';
import path from 'path';
import { exec } from 'child_process';
import Pageres from 'pageres';
import fs from 'fs/promises'; // Use ES6 import for fs as well

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

async function captureScreenshot(url, searchMethod) {
    const filename = `${searchMethod}.png`; // Filename will be either A1.png or C3.png
    
    await new Pageres({ delay: 2 })
        .source(url, ['1280x1024'], { crop: true, filename: searchMethod }) // Set filename based on searchMethod
        .destination('public') // Saving in the 'public' directory
        .run();

    return `/${filename}`; // Return the path relative to the public directory
}

app.post('/search', async (req, res) => {
    const searchMethod = req.body.searchMethod || "A1"; // Example: "A1" or "C3"
    const searchTerm = req.body.searchTerm || "default";

    try {
        const searchResults = await runPythonScript("Ai/toplink.py", [searchMethod, searchTerm]);
        if (searchResults && searchResults.url) {
            const screenshotPath = await captureScreenshot(searchResults.url, searchMethod);
            res.json({
                message: 'Search completed',
                screenshotPath: screenshotPath,
                url: searchResults.url
            });
        } else {
            throw new Error("No valid URL from Python script");
        }
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: error.message });
    }
});

function runPythonScript(scriptPath, args) {
    return new Promise((resolve, reject) => {
        const formattedArgs = args.map(arg => `"${arg}"`).join(' ');
        const script = exec(`python3 ${scriptPath} ${formattedArgs}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return reject(`Error: ${error}`);
            }

            try {
                const parsedOutput = JSON.parse(stdout.trim());
                resolve(parsedOutput);
            } catch (parseError) {
                console.error(`Error parsing JSON: ${parseError}`);
                reject(`Error parsing JSON: ${parseError}`);
            }
        });
    });
}

function runPythonScriptB2(scriptPath, searchTerm) {
    return new Promise((resolve, reject) => {
        const script = exec(`python3 ${scriptPath} "${searchTerm}"`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return reject(`Error: ${error}`);
            }

            try {
                const parsedOutput = JSON.parse(stdout.trim());
                resolve(parsedOutput);
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
    res.sendFile(path.join(process.cwd(), 'Feldspar.html'));
});

app.post('/saveSearchHistory', async (req, res) => {
    const term = req.body.searchTerm; // Assuming you send one term at a time
    try {
        await writeSearchHistoryToFile([term]); // Pass an array with the single term
        res.json({ message: 'Search history updated successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: error.message });
    }
});

async function writeSearchHistoryToFile(history) {
    const filePath = 'UserDat/searchHistory.txt'; // Specify the path to your .txt file
    for (const term of history) {
        await fs.appendFile(filePath, term + '\n');
    // const fileContent = history.join('\n'); // Join array elements with a newline character
    // await fs.writeFile(filePath, fileContent);
}
}

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


// Helper function to check if a string is a valid URL
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}
