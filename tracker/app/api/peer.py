"""peer.py - Controller for Peer."""
from flask import Blueprint, jsonify, request
from app import app
from app.controllers import PeerController
from app.utils import serialize_sqla, row2dict
from app.views import login

peer_api = Blueprint('peer_api', __name__, url_prefix='/api/peer')


@peer_api.route('', methods=['POST'])
def create():
    """ Create new peer """
    if request.json['secret'] != app.config['CLIENT_HANDSHAKE']:
        return jsonify(), 401

    peer = PeerController.create(request.remote_addr)

    return jsonify(id=peer.id)


@peer_api.route('/ping/<int:peer_id>', methods=['POST'])
def ping(peer_id):
    """ Get ping from peer"""
    load = int(request.json['load'])
    if load > 0 and load <= 100 and peer_id:
        PeerController.ping(peer_id, load)
    return jsonify()


@peer_api.route('/<int:peer_id>', methods=['DELETE'])
def delete(peer_id):
    """ Delete peer """
    peer = PeerController.get(peer_id)

    if not peer:
        return jsonify(error='Peer not found'), 500

    PeerController.delete(peer)

    return jsonify()


@peer_api.route('/<int:peer_id>', methods=['GET'])
@login.login_redirect
def get(peer_id):
    """ Get peer """
    peer = PeerController.get(peer_id)

    if not peer:
        return jsonify(error='Peer not found'), 500

    return jsonify(peer=serialize_sqla(peer))


@peer_api.route('/all', methods=['GET'])
@login.login_redirect
def get_all():
    """ Get all peers unfiltered """
    peers = PeerController.get_all()

    if not peers:
        return jsonify(error='No peers were found'), 500

    ser_peers = []
    for peer in peers:
        ser_peer = row2dict(peer)
        ser_peer['job'] = None
        if(peer.task):
            ser_peer['job'] = row2dict(peer.task.job)
        ser_peers.append(ser_peer)

    return jsonify(peers=ser_peers)
