from app import db
from app.models import Peer
from datetime import datetime


class PeerController:
    @staticmethod
    def create(peer):
        """Create peer by peer dict."""
        if type(peer) is dict:
            peer = Peer.new_dict(peer)
        else:
            peer = Peer(peer)

        db.session.add(peer)
        db.session.commit()

        return peer

    @staticmethod
    def get(peer_id):
        """Get peer by id."""
        return Peer.query.get(peer_id)

    @staticmethod
    def get_all():
        """Get all peers."""
        return Peer.query.all()

    @staticmethod
    def delete(peer):
        """ Delete peer item """
        db.session.delete(peer)
        db.session.commit()

    @staticmethod
    def ping(peer_id, CPU):
        peer = PeerController.get(peer_id)
        peer.active = True
        peer.last_active = datetime.now()

        peer.CPU = CPU
        db.session.add(peer)
        db.session.commit()
