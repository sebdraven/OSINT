var links = [];
var casper = require('casper').create();
var padding=casper.cli.get(0)
var criteria=casper.cli.get(1)
function getLinks() {
   
    var links = document.querySelectorAll('h3 a');
    return Array.prototype.map.call(links, function(e) {
        return e.getAttribute('href')
    });
}


casper.start();

casper.open('http://fr.yahoo.com/search='+criteria+'&rd=r1&fr=yfp-t-731&fr2=sb-top&xargs=0&pstart=1&b='+padding)
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
