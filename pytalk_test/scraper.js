function scraper_module() {
    const pytalk = require('pytalk');
    let worker = pytalk.worker('test-scraper.py');

    let subito = worker.method('subito');

    var done = false;

    this.run = function(callback) {
        subito((err, res) => {
            if (!done) {
                callback(res);
                done = true;
            }
        });
    };


}

module.exports = scraper_module;