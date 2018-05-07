json_file = fetch('script_input.json')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    return myJson;
  });

json_file.then(function(file) {
	console.log(file)
	var accordion = document.getElementById('accordion');
var allText = ''
for (var i=0; i<file.Scripts.length; i++){
	var parameters = ''
	for (var j=0; j<file.Scripts[i].Input_Parameters.length ;j++){
		parameters += `
        <div class='form-group row'>
            <label for="col-5" class="col-5 col-form-label">${file.Scripts[i].Input_Parameters[j].Name}:</label>   
              <div class="col-5"> 
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

   

    <div id="collapse${i.toString()}" class="collapse show" aria-labelledby="heading1" data-parent="#accordion">
      <form name="regform" action="/testing" method="POST">
      <div class="card-body">
            
        
                      <div class='form-group row'>
                <label for="col-5" class="col-5 col-form-label">Description:</label>   
              <div class="col-5"> 
              <textarea type=text name="Description" class="form-control" rows="4" readonly>${file.Scripts[i].Description}</textarea> 
                </div>
            </div>
          </div>

          	${parameters}

                      <div class='form-group row'>
                <label for="col-5" class="col-5 col-form-label">Description:</label>   
              <div class="col-5"> 
              <input type=hidden name="file_name" class="form-control" value=${file.Scripts[i].File_Name} >
                </div>
            </div>


           
    <button class="btn btn-primary btn-lg float-right" type="submit" id="submitbutton" >Run</button>
    </form>
      </div>
    </div>
  </div>
`;
}
accordion.innerHTML = allText


})


