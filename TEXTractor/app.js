const http = require('http');
var fs = require('fs')

const hostname = '172.26.66.41';
const port = 8004;

fs.readFile('./index.html', function(err, html){
    if (err){
        throw err;
    }
  http.createServer(function(req, res) {
  res.writeHeader(200, {'Content-Type': 'text/html'});
  res.write(html);
  res.end();
}).listen(port, hostname);

});

