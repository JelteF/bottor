from app import db
from app.models import Peer


class PeerController:
    @staticmethod
    def create(peer_dict):
        """Create peer by peer dict."""
        peer = Peer.new_dict(peer_dict)

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
    def delete(product):
        """ Delete product item """
        db.session.delete(product)
        db.session.commit()
