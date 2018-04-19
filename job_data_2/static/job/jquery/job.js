$(document).ready(function(){

  $(".table_selected").show()
  $(".table_not_selected").hide()

  $("#id_OT lable").html("jazz")

  $("#id_OT input").change(function() {
      $("#id_OT label").removeClass("case");

      $(this).parent().addClass("case")
  });

  $("#id_Overtime_pay input ").change(function() {
      $("#id_Overtime_pay label").removeClass("case");

      $(this).parent().addClass("case")
  });

  i = 1

  $('.increase').click(function(){
    i = i+1
    $('.repeat').append(
    "<hr>工作名稱:<br>\
    <input type='text' name='job_name"+i +"'><br>\
    工作地點::<br>\
    <input type='text' name='job_location"+i
    +"'><br>\
    平均收入:<br>\
    <input type='text' name='average"+i +"'><br>\
    最高收入:<br>\
    <input type='text' name='max_salary"+i +"'><br>\
    最低收入:<br>\
    <input type='text' name='min_salary"+i +"'>"
    )
    $('.freelance_form_number').val(i)
  })

  });
