var i = 1 ;

function addForm() {
  if (i <= 8) {
  var input_data = document.createElement('input');
  input_data.type = 'text';
  input_data.classList.add('form-control');
  input_data.id = 'inputform';
  input_data.name = 'destination';
  input_data.placeholder = '経由地' + i;
  var parent = document.getElementById('form_area');
  var form_group = document.createElement('div');
    form_group.classList.add('form-group', 'mb-3');
  parent.appendChild(input_data);
  i++ ;
}}
