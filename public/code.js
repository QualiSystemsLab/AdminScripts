// build page after socket is established
socket.on('connect', () => {
  buildPage();
});

function expandFirstCard() {
  const firstCard = document.getElementById("collapse0");
  firstCard.classList.add("show");
}

// clear placeholder text for first run
function noop() { };
function clearOnce(outputText) {
  clearOnce = noop; // swap the functions
  clearOutput(outputText);
  outputText.innerHTML = '';

}

function clearOutput(outputText) {
  outputText = document.getElementById('output-text');
  outputText.innerHTML = '>';
}

function scrollConsole() {
  var console = document.getElementById("output-console");
  console.scrollTop = console.scrollHeight;
}

// on socket input, populate output console
socket.on('pyoutput', function (data) {
  console.log(data);
  outputText = document.getElementById('output-text');
  clearOnce(outputText);
  outputText.innerHTML += `> ${data} <br>`;
  scrollConsole();
})

// promise wrapper for reading parameter json
json_file_promise = fetch('script_input.json')
  .then(function (response) {
    return response.json();
  })
  .then(function (myJson) {
    return myJson;
  });

// building dynamic html in response to reading parameter json
function buildPage() {
  json_file_promise.then(function (file) {
    // console.log(file);
    var fileString = JSON.stringify(file);
    // console.log(fileString);

    var accordion = document.getElementById('accordion');
    var allText = '';
    for (var i = 0; i < file.Scripts.length; i++) {
      var parameters = '';
      for (var j = 0; j < file.Scripts[i].Input_Parameters.length; j++) {
        parameters += `
        <div class='form-group row'>
          <label for="${file.Scripts[i].Input_Parameters[j].Name}" class="col-3 col-form-label">${file.Scripts[i].Input_Parameters[j].Name}:</label>   
          <div class="col-8"> 
            <input type="text" name="${file.Scripts[i].Input_Parameters[j].Name}" class="form-control" placeholder="${file.Scripts[i].Input_Parameters[j].Value}"> 
          </div>
        </div> 
		    `
      }

      allText += `
      <div class="card">
        <div class="card-header" id="heading${i.toString()}">
          
          <h5 class="mb-0">
            <button class="btn btn-link" data-toggle="collapse" data-target="#collapse${i.toString()}" data-parent="#accordion">
              ${file.Scripts[i].Name}
            </button>
          </h5>
        </div>

        <div id="collapse${i.toString()}" class="collapse hide" aria-labelledby="heading1" data-parent="#accordion">
          <div class="card-body">
            <div class="script-desc">
              <div class='form-group row'>
                <label for="col-5" class="col-3 col-form-label">Description:</label>   
                <div class="col-8"> 
                  <textarea type=text name="Description" class="form-control" rows="4" readonly>${file.Scripts[i].Description}</textarea> 
                </div>
              </div>  
            </div>
            
            <div id="params-container${i}">
              ${parameters}
              <div class="col-12">
                <button class="btn btn-primary btn-lg submitbutton" 
                        onclick="runScript(event,'${file.Scripts[i].Name}', ${i.toString()})">
                        Run Script
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
      `
    }
    accordion.innerHTML = allText;
    expandFirstCard()

  })
}

// post request
function sendPost(inputJSON) {
  fetch('http://localhost:3000/runscript', {
    method: 'POST',
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-type': 'application/json'
    },
    body: inputJSON
  }).then(res => res.json())
    .then(data => {
      console.log(data);
      console.log('yoooo res here');
    }
    )
}

function getInputJSON(fileName, i) {
  let inputs = document.querySelectorAll(`#params-container${i} input`);
  console.log(inputs);
  let paramsObj = {
    file_name: fileName,
    socket_id: socket.id
  };
  inputs.forEach((input) => {
    paramsObj[`${input.name}`] = input.value;
  })
  return JSON.stringify(paramsObj, null, 2);
}

function runScript(event, fileName, i) {
  event.preventDefault();
  console.log(event);

  console.log('running script');
  const inputJSON = getInputJSON(fileName, i);
  console.log(inputJSON);
  sendPost(inputJSON);
}