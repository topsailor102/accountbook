function barchart() {
  $.ajax({
    type : 'get',
    url: 'getdataset',
    success: function (data) {

      ctx = 'dataset';

      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels, datasets: data.datasets,
        },
        options: {
            responsive: true,
            legend: {
            position: 'bottom',
          },
          title: {
            display: true, text: 'Monthly Expenses Chart'
          },
          scales: {
            xAxes: [{
                stacked: true, 
                gridLines: {
                display: false,
                }
            }],
            yAxes: [{
                stacked: true,
                ticks: {
                beginAtZero: true,
                },
                type: 'linear',
            }]
          },
        }
      });
    }
  });
}

barchart();