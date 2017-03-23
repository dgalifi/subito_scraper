'use strict';

const Hapi = require('hapi');
const pytalk = require('pytalk');
const server = new Hapi.Server();

server.connection({ port: 3000, host: 'localhost' });

let worker = pytalk.worker('test-scraper.py');

// routes
server.route({
    method: 'GET',
    path: '/',
    handler: function(request, reply) {
        reply('Hello, world!');
    }
});

var testFunc = function(callback) {
    console.log('Doing something');
    setTimeout(function() {
        console.log("...");

        var ret = 'done';
        var err = '';

        callback(err, ret);

    }, 3000);
}


server.route({
    method: 'GET',
    path: '/search',
    handler: function(request, reply) {

        var done = false;
        let scraper = worker.method('subito');

        var res = scraper((err, ret) => {
            if (!done) {
                reply(ret);
                done = true;
            }
        });


    }
});

// Start server
server.start((err) => {

    if (err) {
        throw err;
    }
    console.log(`Server running at: ${server.info.uri}`);
});
