"""peer.py - Controller for Peer."""
from flask import Blueprint, jsonify, request
from app.controllers import PeerController
from app.utils import serialize_sqla

peer_api = Blueprint('peer_api', __name__, url_prefix='/api/peer')


@peer_api.route('', methods=['POST'])
def create():
    """ Create new peer """
    peer_dict = request.json

    peer = PeerController.create(peer_dict)

    return jsonify(id=peer.id)


@peer_api.route('/<int:peer_id>', methods=['DELETE'])
def delete(peer_id):
    """ Delete peer """
    peer = PeerController.get(peer_id)

    if not peer:
        return jsonify(error='Peer not found'), 500

    PeerController.delete(peer)

    return jsonify()


@peer_api.route('/<int:peer_id>', methods=['GET'])
def get(peer_id):
    """ Get peer """
    peer = PeerController.get(peer_id)

    if not peer:
        return jsonify(error='Peer not found'), 500

    return jsonify(peer=serialize_sqla(peer))


@peer_api.route('/all', methods=['GET'])
def get_all():
    """ Get all peers unfiltered """
    # At this point, the association_id should be gotten, so that not ALL
    # peers are listed, but only those related to the relevant association.
    peers = PeerController.get_all()

    if not peers:
        return jsonify(error='No peers were found'), 500

    return jsonify(peers=serialize_sqla(peers))
