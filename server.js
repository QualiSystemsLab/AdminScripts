const express = require('express');
const app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);

const bodyParser = require("body-parser");

const PythonShell = require('python-shell');


const mockObj = {
  param1: "firstParameter",
  param2: "secondParameter"
}

//// ===================== socket IO ===========================

io.on('connection', function (socket) {
  console.log(`socket id: ${socket.id} connected`);
  socket.on('disconnect', (reason) => {
    console.log(`socket id: ${socket.id} disconnected because of: ${reason}`);
  })
});

//// ===================== python shell ===========================

function runPyShell(jsonString) {
  var pyOutput = 'placeholding';
  var requestObj = JSON.parse(jsonString);
  socketId = requestObj.socket_id;
  console.log(socketId);
  var shell = new PythonShell('my_script.py', { mode: 'text' });

  shell.send(jsonString);

  shell.on('message', function (message) {
    console.log('onMessage: ', message);
    pyOutput = message;
    console.log('onmessage pyoutput:', pyOutput);
  
    io.to(socketId).emit('pyoutput', pyOutput);
  });

  // end the input stream and allow the process to exit
  shell.end(function (err, code, signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
    console.log('The exit signal was: ' + signal);
    console.log('finished');
  });
  console.log('after pyOutput:', pyOutput);
  return pyOutput;
}



//// ===================== server ===========================

// body parser for parsing the post request
// app.use(bodyParser.urlencoded({
//   extended: true
// }));
// app.use(bodyParser.json());

// serves up html
app.use(express.static(__dirname + '/public'));

var urlEncodedParser = bodyParser.urlencoded({ extended: true });

// create application/json parser
var jsonParser = bodyParser.json()

app.post("/testing", jsonParser, function (request, response) {
  request.on('end', () => {
    response.writeHead(200, { 'Content-Type': 'text/html' });
  })
  console.log(request.body); //This prints the JSON document received (if it is a JSON document)
  console.log(typeof (request.body));
  requestString = JSON.stringify(request.body, null, 2);
  console.log(requestString);
  runPyShell(requestString);
  response.send({message: 'test parameters received! response coming back down a socket soon!'});

});



app.get('/', (req, res) => res.send('Hello World!'))
http.listen(3000, () => console.log('Example app listening on port 3000!'))