$(document).ready(function() {

  $("#fruta").change(function() {
      var val = $(this).val();
      $("#precio").html(options[val]);
  });

  var options = [
      "<option value='6000'>$6.000</option><option value='6500' selected>$6.500</option><option value='7000'>$7.000</option>",
      "<option value='10000'>$10.000</option><option value='11000'>$11.000</option><option value='12000' selected>$12.000</option>",
      "<option value='5000' selected>$6.000</option>"
  ];
});