import Pageres from 'pageres';

await new Pageres({ delay: 2 })
    .source('https://github.com/sindresorhus/pageres', ['480x320', '1024x768'], { crop: true, filename: 'A1' })
    .source('https://sindresorhus.com', ['1280x1024', '1920x1080'], { filename: 'C3' })
    .source('data:text/html,<h1>Awesome!</h1>', ['1024x768'], { filename: 'B2' }) // Example for B2
    .destination('screenshots')
    .run();

console.log('Finished generating screenshots!');
