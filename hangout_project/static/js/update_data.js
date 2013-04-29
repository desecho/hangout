function update_data(name, value) {
    var post = {};
    post[name] = value;
    $.post('/update-data/', post,
        function(data) {}
    ).error(function() {
        $('#link_error_dialog').click();
    });
}