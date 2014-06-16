var models = {};

models.Peer = Backbone.Model.extend({
    urlRoot: '/api/peer',
    defaults: {
        id: null,
        location: '',
    },
});

/* Collections. */
var collections = {};

collections.Peers = Backbone.Collection.extend({
    model: models.Peer
});
