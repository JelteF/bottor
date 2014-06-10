var models = {};

models.Piece = Backbone.Model.extend({
    urlRoot: '/api/piece',
    defaults: {
        id: null,
        name: '',
        description: '',
        location: '',
        piece_serie_id: null,
    },
});

models.PieceSerie = Backbone.Model.extend({
    urlRoot: '/api/piece_serie',
    defaults: {
        id: null,
        name: '',
    },
});

/* Collections. */
var collections = {};

collections.Pieces = Backbone.Collection.extend({
    model: models.Piece
});

collections.PieceSeries = Backbone.Collection.extend({
    model: models.PieceSerie
});