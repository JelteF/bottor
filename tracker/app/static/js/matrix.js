var matrixViewView;

$(function() {
    matrixViewView = new MatrixViewView({el: '#matrices tbody'});

    $('#new-btn').click(function() {
        $(this).parents('.panel-body').hide();
        var matrixNewView = new MatrixNewView({el: '#new-matrix'});
        $(this).hide();
    });
});

/* Backbone stuff. */
var MatrixViewView = Backbone.View.extend({
    matrices: new collections.Matrices(),

    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/matrix/all', {}, function(data) {
            me.matrices = new collections.Matrices(data.matrices);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#matrix-view-template').html(), {
            matrices: this.matrices.models
        });
        this.$el.html(template);
    }
});

var MatrixNewView = Backbone.View.extend({
    initialize: function() {
        var me = this;
        me.render();
    },
    render: function() {
        var template = _.template($('#matrix-new-template').html(), {});
        this.$el.html(template);
        $('input#fileupload').fileupload({
            url: '/api/upload',
            dataType: 'json',
            done: function (e, data) {
                console.log(data.result.file);
                $('#filename').val(data.result.file);
            },
        }); 
    },
    events: {
        'click button#cancel-new': 'cancel',
        'click button#save-new': 'save'
    },
    cancel: function(event) {
        this.undelegateEvents();
        this.$el.removeData().unbind();

        this.$el.empty();
        $('#new-btn').parents('.panel-body').show();
        $('#new-btn').show()
    },
    save: function(event) {
        $('button#save-new').attr('disabled', true);

        var matrix = new models.Matrix();
        set_form_values(matrix, $('#new-matrix-form'));

        var view = this;
        matrix.save({}, {
            success: function() {
                clearflash();
                flash('Matrix successfully saved', 'success');
                view.cancel();
                $('#new-btn').show();
                matrixViewView.update();
            }, error: function(model, response) {
                ajax_error_handler(response);
                $('button#save-new').attr('disabled', false);
            }
        });
    }
});