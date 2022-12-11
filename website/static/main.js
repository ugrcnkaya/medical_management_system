
//cancel an appointment
function cancelAppointment(Appointment_ID) {
  fetch("/cancel-appointment", {
    method: "POST",
    body: JSON.stringify({ Appointment_ID: Appointment_ID }),
  }).then((_res) => {
    location.reload()
  });
}

//dele schedule
function cancelSchedule(Schedule_ID) {
  fetch("/delete-schedule", {
    method: "POST",
    body: JSON.stringify({ Schedule_ID: Schedule_ID }),
  }).then((_res) => {
    location.reload()
  });
}






// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();


});

