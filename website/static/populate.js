$(document).ready(function(){




//specification choose
    $("select#specification").change(function() {

        var selectedSpecification = $(this).find('option:selected').text();
        if (selectedSpecification != "Choose...") {
            var Specification = ($('#specification option:selected').text());
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

                   var output = "";
                   $.each(response, function(a,b){
                         output += "<option id="+b.id+">"+b.name+"</option>";
                   })
                $("#doctor").append(output);



                         console.log(response)
            }
        });


            }

    });


});