import express from 'express';
import path from 'path';
import { exec } from 'child_process';
import Pageres from 'pageres';

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
    res.sendFile(path.join(process.cwd(), 'Feldspar.html'));
});
