var links = [];
var casper = require('casper').create();
var url=casper.cli.get(0);
function getLinks() {
   
    var links = document.querySelectorAll('tr a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href')
    });
}


casper.start();

casper.open(url)
casper.then(function() {
    // aggregate results for the 'casperjs' search
    links = this.evaluate(getLinks);
	
    // now search for 'phantomjs' by filling the form again
});


casper.run(function() {
    // echo results in some pretty fashion
    this.echo(links.length + ' links found:');
    this.echo(' - ' + links.join('\n - ')).exit();
});
