$(document).ready(function () {

    var table = $('#report_table').DataTable();

    yadcf.init(table, [{
        column_number: 4,
        filter_type: "multi_select",
        select_type: 'select2'
    }]);

    var createFilterOptions = function(dataSource, colIdx) {
        // Create the select list and search operation
        var select = $('<select multiple id="filter_' + colIdx + '" />')
            .appendTo(
                table.column(colIdx).footer()
            )
            .on('change', function () {
                console.log($(this).val());
                var searchText = '';
                var searchValues = $(this).val();
                if (searchValues.length > 0) {
                    searchText = "^" + searchValues.join("|") + "$";
                }
                console.log(searchText);
                table
                    .column(colIdx)
                    .search(searchText, true, false)
                    .draw();
            });

        dataSource
            .sort()
            .unique()
            .each(function (value) {
                select.append($('<option value="' + value + '">' + value + '</option>'));
            });

        //select.multiselect();
        //select.select2();
    };

    table.columns().flatten().each(function (colIdx) {
        // Get the search data for the column and create a select list
        var dataSource = table
            .column(colIdx)
            .cache('search');
        createFilterOptions(dataSource, colIdx);
    });

    $('#filter_5').change(function() {
        var dependentColumnIdx = 4;

        // Remove the existing select
        $('#filter_' + dependentColumnIdx).closest('td').children().remove();

        // Get the filtered data for the column and create a select list
        var dataSource = table
            .column(dependentColumnIdx, { filter : 'applied'} )
            .data();
        createFilterOptions(dataSource, dependentColumnIdx);
    })
});