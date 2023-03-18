var i = 1 ;
function addForm() {
  var input_data = document.createElement('input');
  input_data.type = 'text';
  input_data.class = 'destination';
  input_data.id = 'inputform';
  input_data.name = 'destination';
  input_data.placeholder = '経由地' + i;
  var parent = document.getElementById('form_area');
  parent.appendChild(input_data);
  i++ ;
}