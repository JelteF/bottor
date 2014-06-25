$(function() {
    $('form').on('submit', function(e) {
        e.preventDefault();
        console.log('blaaaaa');
        var a = $('input[name="A"]:checked').val();
        var b = $('input[name="B"]:checked').val();
        $('button', 'form').attr('disabled', 'true');
        JSON_post({A: a, B: b}, '/api/job/', {success: function() {
            //$('button', 'form').attr('disabled', 'false');
            redirect('/job/');

        }});
    });
});
