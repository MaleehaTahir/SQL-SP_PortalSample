$(document).ready(function () {

    var table = $('#report_table').DataTable();

    var yadcfOptions = [
        {
            column_number: 4,
            filter_match_mode: 'exact',
            filter_type: "multi_select",
            select_type: 'select2',
            data: ['ab', 'cd']
        }, {
            column_number: 5,
            filter_match_mode: 'exact',
            filter_type: "multi_select",
            select_type: 'select2'
        }
    ];

    yadcf.init(table, yadcfOptions);

    $('#s2id_autogen31').change(function() {
        console.log('selection changed');
        var dependentColumnIdx = 4;

        // Remove the existing select
        $('#filter_' + dependentColumnIdx).closest('td').children().remove();

        // Get the filtered data for the column and create a select list
        var dataSource = table
            .column(dependentColumnIdx, { filter : 'applied'} )
            .data();
        createFilterOptions(dataSource, dependentColumnIdx);
    });

    MutationObserver = window.MutationObserver || window.WebKitMutationObserver;

    var observer = new MutationObserver(function(mutations, observer) {
        // fired when a mutation occurs
        // Index of this column in yadcfOptions
        var colIdx = 0;
        var filterData = [];
        table
            .column(yadcfOptions[colIdx].column_number, { filter : 'applied'} )
            .data().sort()
            .unique()
            .each(function (value) {
                filterData.push(value);
            });
        console.log(filterData);
        yadcfOptions[colIdx].data = filterData;
        yadcf.init(table, yadcfOptions);
    });

    // define what element should be observed by the observer
    // and what types of mutations trigger the callback
    observer.observe($('#yadcf-filter-wrapper--report_table-5 .select2-choices')[0], {
        childList: true,
        subtree: true
    });
});