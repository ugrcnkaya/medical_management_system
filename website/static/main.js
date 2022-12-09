
//cancel an appointment
function cancelAppointment(Appointment_ID) {
  fetch("/cancel-appointment", {
    method: "POST",
    body: JSON.stringify({ Appointment_ID: Appointment_ID }),
  }).then((_res) => {
    window.location.href = "/appointments";
  });
}





// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});