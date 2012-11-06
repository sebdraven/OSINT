var casper = require('casper').create({

})
, terms = casper.cli.get(0),url=casper.cli.get(1),emplacement=casper.cli.get(2),i=0
casper.start(url, function() {
    this.capture(emplacement+'/'+terms+'.png', {
        top: 10,
        left: 10,
        width: 1024,
        height: 768
    },12000);
});

casper.run()
