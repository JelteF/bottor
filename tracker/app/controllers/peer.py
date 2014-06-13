from app import db
from app.models import Peer

class PeerController:
    @staticmethod
    def create(peer_dict):
        peer = Peer.new_dict(peer_dict)

        db.session.add(peer)
        db.session.commit()

        return peer
