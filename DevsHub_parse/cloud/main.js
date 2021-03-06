
// Use Parse.Cloud.define to define as many cloud functions as you want.
// For example:
Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello world!");
});

var _ = require("underscore");
Parse.Cloud.beforeSave("Inventarios", function(request, response) {
    var prod = request.object;


    var toLowerCase = function(w) { return w.toLowerCase(); };

    var words = prod.get("Producto").split(" ");
    words = _.map(words, toLowerCase);
    prod.set("words", words);
    
    
    prod.set("Producto", prod.get("Producto").toUpperCase() );
    
    /*
    var stopWords = ["the", "in", "and"];
    words = _.filter(words, function(w) { return w.match(/^w+$/) && ! _.contains(stopWords, w); });

    var hashtags = prod.get("Producto").match(/#.+?b/g);
    hashtags = _.map(hashtags, toLowerCase);

    prod.set("words", words);
    prod.set("hashtags", hashtags);*/
    
    response.success();
});

Parse.Cloud.beforeSave("Clientes", function(request, response) {
    var client = request.object;

    var name = client.get("Name");
    
    client.set("Name", name.toUpperCase());
    client.set("words", name.toUpperCase().split(" ") );

    response.success();
});
