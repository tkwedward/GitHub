function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('a.order').click(function(e){
  e.preventDefault();
  var target = $(this);
  var previous_action = $(this).data('action')
  var previous_text = $(this).text()
  $.post(ajax_order,
          {
          action: previous_action,

          id: $(this).data('id'),
          position: $('#id_keyword').val(),
          industry: $('#id_industry').val(),
          location: $('#id_location').val(),
          salary: $('#id_salary').val()
        },
        function(data){
          // console.log(data);
          $('#id_keyword').val(previous_action)
          target.text(previous_text=='up'?'down':'up')
          target.data('action',previous_action=='+'?'-':'+');
          $('.list_table').html(data['template'])

        })//function(data)
      }//get
)//click
