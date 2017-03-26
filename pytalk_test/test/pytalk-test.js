var assert = require('chai').assert;
var request = require('request');

var base_url = "http://localhost:8080/";

describe('# Pytalk test', () => {
    describe('GET /', () => {
        it('when / requested then returns correct message', () => {
            request.get(base_url, (err, res, body) => {
                assert.equal(res.statusCode, 200);
            });
        });
    });
});