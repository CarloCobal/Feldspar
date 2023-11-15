const express = require('express');
const path = require('path');
const { exec } = require("child_process");
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

app.post('/search', async (req, res) => {
    console.log("Search endpoint hit with term: hello (static for testing)");
    try {
        // Using a static input for testing
        const staticTestInput = "hello";
        const searchResults = await runPythonScript("/Users/quaidbulloch/Downloads/modified_my_googlesearch.py", [staticTestInput]);
        if (searchResults) {
            const parsedResults = JSON.parse(searchResults);
            res.json({ message: 'Search completed', results: parsedResults });
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
            resolve(stdout);
        });
    });
}

// app.post('/search', async (req, res) => {
//     console.log("Search endpoint hit with term:", req.body.searchTerm);
//     try {
//         const searchTerm = req.body.searchTerm;
//         const searchResults = await runPythonScript("/Users/quaidbulloch/Downloads/modified_my_googlesearch.py", [searchTerm]);//change this to be agnostic localStorage.
//         const parsedResults = JSON.parse(searchResults);
//         res.json({ message: 'Search completed', results: parsedResults });
//     } catch (error) {
//         console.error(error);
//         res.status(500).json({ error: 'An error occurred' });
//     }
// });

// function runPythonScript(scriptPath, args) {
//     return new Promise((resolve, reject) => {
//         const script = exec(`python ${scriptPath}`, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`exec error: ${error}`);
//                 return reject(`Error: ${error}`);
//             }
//             if (stderr) {
//                 console.error(`stderr: ${stderr}`);
//                 // Only reject if stderr contains actual error messages
//                 if (isError(stderr)) {
//                     return reject(`Stderr: ${stderr}`);
//                 }
//             }
//             if (stdout) {
//                 resolve(stdout);
//             } else {
//                 reject('No output from Python script');
//             }
//         });

//         script.stdin.write(args.join(' '));
//         script.stdin.end();
//     });
// }

function isError(stderr) {
    // Implement logic to determine if stderr contains error messages
    // For example, checking for specific keywords or patterns
    return stderr.includes("Error") || stderr.includes("Traceback");
}


app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'Feldspar.html'));
});
