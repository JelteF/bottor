var models = {};

models.Peer = Backbone.Model.extend({
    urlRoot: '/api/peer',
    defaults: {
        id: null,
        location: '',
        job: '',
    },
});

models.Matrix = Backbone.Model.extend({
    urlRoot: '/api/matrix',
    defaults:{
        id: null,
        filename: '',
        nRows: null,
        nCols: null,
    },
});

models.Job = Backbone.Model.extend({
    urlRoot: '/api/job',
    defaults: {
        matrixA: null,
        matrixB: null,
    }
});

/* Collections. */
var collections = {};

collections.Peers = Backbone.Collection.extend({
    model: models.Peer
});

collections.Matrices = Backbone.Collection.extend({
    model: models.Matrix
});
