const { exec } = require("child_process");

function runPythonScript(scriptPath, input, callback) {
    exec(`/opt/homebrew/bin/python3 ${scriptPath} "${input}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
        }
        callback(stdout);
    });
}

// Example usage
runPythonScript("/Users/quaidbulloch/Documents/Code/Feldspar/my_googlesearch.py", "Your Search Query", (output) => {
    const results = JSON.parse(output);
    // Use results here
    console.log(results);  // This will be an array of the top three search results
});
