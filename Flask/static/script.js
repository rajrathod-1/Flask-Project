$(document).ready(function() {
    $('#covid-data').DataTable();

    $('#fetch-data').on('click', function() {
        $.get('/fetch_data', function(response) {
            alert(response.message);
            loadData();
        });
    });

    function loadData() {
        $.get('/api/data', function(data) {
            var table = $('#covid-data').DataTable();
            table.clear().draw();
            $.each(data, function(index, item) {
                table.row.add([item.country, item.date, item.confirmed, item.deaths, item.recovered]).draw();
            });
        });
    }

    loadData();
});
