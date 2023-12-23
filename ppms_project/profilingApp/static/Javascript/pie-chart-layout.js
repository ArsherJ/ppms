// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Pie Chart Example
var data_count = JSON.parse('{{ count_data|escapejs }}')
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: ["Validated", "Unvalidated", "Parent", "Preschooler"],
    datasets: [{
      data: data_count,
      backgroundColor: ['#dc3545', '#ffc107', '#28a745'],
    }],
  },
});
