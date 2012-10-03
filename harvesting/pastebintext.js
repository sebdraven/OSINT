
var casper = require('casper').create();


var url=casper.cli.get(0);
var ua =casper.cli.get(1)

casper.start().then(function() {
    this.userAgent(ua);
    this.open(url, {
        method: 'get',
        headers: {
            'Accept': 'application/text'
        }
    });
});

casper.run(function() {
    this.echo(this.debugPage());
    this.exit();
});

