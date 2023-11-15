const express = require('express');
const fs = require('fs');
const path = require('path');
const { exec } = require("child_process");
const app = express();
const port = 3000;
app.use(express.static('public')); // 'public' is the folder where your images and other static files are.

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'Feldspar.html'));
});

app.post('/search', async (req, res) => {
    const searchTerm = req.body.searchTerm;

    try {
        const content = await updateContent(searchTerm);
        res.json(content); // Send back the generated content as JSON
    } catch (error) {
        console.error(error);
        res.status(500).send('An error occurred');
    }
});    

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});


function runPythonScript(scriptPath, args) {
    const formattedArgs = args.map(arg => `"${arg}"`).join(' ');
    return new Promise((resolve, reject) => {
        exec(`/opt/homebrew/bin/python3 ${scriptPath} ${formattedArgs}`, (error, stdout, stderr) => {
            if (error) {
                reject(`exec error: ${error}`);
                return;
            }
            if (stderr) {
                reject(`stderr: ${stderr}`);
                return;
            }
            resolve(stdout);
        });
    });
}

function extractImgUrl(imgGenOutput) {
    try {
        const imgGenData = JSON.parse(imgGenOutput);
        return imgGenData.url;
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return null;
    }
}

async function updateContent(searchTerm) {
    try {
        // Run simpleChat.py with searchTerm
        const chatOutput = await runPythonScript("Ai/simpleChat.py", [searchTerm]);
        console.log("simpleChat.py Output:", chatOutput);

        const movieTitles = chatOutput.split('\n')
                              .filter(line => /^\d/.test(line))
                              .map(line => {
                                  const match = line.match(/^\d+\.\s*(.+)/);
                                  return match ? match[1] : '';
                              });

        let htmlContent = fs.readFileSync("Feldspar.html", "utf-8");
        for (let i = 0; i < movieTitles.length; i++) {
            const title = movieTitles[i];

            const imgGenOutput = await runPythonScript("Ai/imgGen.py", [title]);
            const imgUrl = extractImgUrl(imgGenOutput);
            console.log(`Image URL for ${title}: ${imgUrl}`); // Debugging

            const searchOutput = await runPythonScript("my_googlesearch.py", [title]);
            const searchLink = JSON.parse(searchOutput).top_link;
            console.log(`Google Link for ${title}: ${searchLink}`); // Debugging

            htmlContent = htmlContent.replace(`PLACEHOLDER_IMAGE_${i+1}`, imgUrl);
            htmlContent = htmlContent.replace(`PLACEHOLDER_LINK_${i+1}`, searchLink);
        }

        console.log(htmlContent); // Debugging: Check the final HTML content

        fs.writeFileSync("Feldspar.html", htmlContent);
    } catch (error) {
        console.error(error);
        throw error; // Rethrow the error to be caught in /search endpoint
    }
    
}
