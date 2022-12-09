$(document).ready(function(){




//specification choose
    $("select#specification").change(function() {
        var selectedSpecification = $(this).find('option:selected').text();
        if (selectedSpecification != "Choose...") {
            //var Specification = ($('#specification option:selected').text());
            var select = document.getElementById('specification');
            var value = select.options[select.selectedIndex].value;
             $.ajax({
            type: 'GET',
            url: "/list_appointments?Specification_ID="+value,
            //data: { Specification: Specification },
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                 $("#doctor").empty();

                   var output = "<option selected value=\"0\">Choose...</option>";
                   $.each(response, function(a,b){
                         output += "<option value="+b.id+">"+b.name+"</option>";
                   })
                $("#doctor").append(output);
            }
        });


        }

    });


    //doctor choose
    $("select#doctor").change(function() {
        var doctor = $(this).find('option:selected').text();


        if (doctor != "Choose...") {
            var select_doctor = document.getElementById('doctor');
            var doctor_id = select_doctor.options[select_doctor.selectedIndex].value;
                $.ajax({
            type: 'GET',
            url: "/list_appointments?Doctor_ID="+doctor_id,
            contentType: 'application/json',
            dataType: 'json',
            success: function(response) {
                    $("#date").empty();

                   var output = "<option selected value=\"0\">Choose...</option>";
                   $.each(response, function(a,b){
                        output += "<option value="+b.id+">"+b.date+"</option>";
                   })
                $("#date").append(output);
            }
            });



        }


    });


    //date choose


    //ready

});