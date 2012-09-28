
var casper = require('casper').create();


var url=casper.cli.get(0)

casper.start(url,function(){

    // aggregate results for the 'casperjs' search
	this.echo(this.getTitle());
    this.echo(this.fetchText('li'));
	
    // now search for 'phantomjs' by filling the form again
});

casper.run();

