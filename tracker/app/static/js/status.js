var peerViewView;

$(function() {
    peerViewView = new PeerViewView({el: '#peers tbody'});
});

/* Backbone stuff. */
var PeerViewView = Backbone.View.extend({
    peers: new collections.Peers(),

    initialize: function() {
        this.update();
    },
    update: function() {
        var me = this;

        $.get('/api/peer/all', {}, function(data) {
            me.peers = new collections.Peers(data.peers);
            me.render();
        });
    },
    render: function() {
        var template = _.template($('#peer-view-template').html(), {
            peers: this.peers.models
        });
        this.$el.html(template);
    }
});