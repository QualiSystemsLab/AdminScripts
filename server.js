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
  console.log('a user connected');
});

//// ===================== python shell ===========================

function runPyShell(jsonString='{"param1":"yo"}') {
  var shell = new PythonShell('./ChangeBulkResources/ChangeBulkResources.py', { mode: 'text' });

  var options = {
    mode: 'text',
    args: ['my First Argument', 'My Second Argument']
  };

  // sends a message to the Python script via stdin
  // shell.send('hello');
  // shell.send(mockJSON);

  // shell.send(JSON.stringify([1, 2, 3, 4, 5]));
  mockJSON = JSON.stringify(mockObj);
  // console.log('mockJSON from Node: ', mockJSON);
  // shell.send(mockJSON);
  shell.send(jsonString);

  shell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    console.log('onMessage: ', message);
  });

  // end the input stream and allow the process to exit
  shell.end(function (err, code, signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
    console.log('The exit signal was: ' + signal);
    console.log('finished');
  });
}

// Passing arguments
// PythonShell.run('my_script.py', options, function (err, results) {
//   if (err) throw err;
//   // results is an array consisting of messages collected during execution
//   console.log('results: %j', results);
// });


//// ===================== server ===========================

// body parser for parsing the post request
// app.use(bodyParser.urlencoded({
//   extended: true
// }));
// app.use(bodyParser.json());

// serves up html
app.use(express.static(__dirname + '/public'));

app.use(bodyParser.urlencoded({ extended: true }));

app.post("/testing", function (request, response) {
  console.log(request.body); //This prints the JSON document received (if it is a JSON document)
  console.log(typeof (request.body));
  requestString = JSON.stringify(request.body);
  console.log(requestString);
  console.log(typeof(requestString));

  runPyShell(requestString);

});

app.get('/', (req, res) => res.send('Hello World!'))
http.listen(3000, () => console.log('Example app listening on port 3000!'))