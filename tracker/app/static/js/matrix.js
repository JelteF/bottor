var matrixViewView;

$(function() {
    matrixViewView = new MatrixViewView({el: '#matrices tbody'});
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