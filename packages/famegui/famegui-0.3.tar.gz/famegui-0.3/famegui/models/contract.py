
class Contract:
    """ Represents a contract between two agents """

    def __init__(self, sender_id, receiver_id, product_name):
        if sender_id == receiver_id:
            raise ValueError("sender and receiver can't have the same id {}".format(sender_id))
        self._sender_id = sender_id
        self._receiver_id = receiver_id
        self.product_name = product_name

    @property
    def sender_id(self):
        return self._sender_id

    @property
    def sender_id_str(self):
        return "#{}".format(self._sender_id)

    @property
    def receiver_id(self):
        return self._receiver_id

    @property
    def receiver_id_str(self):
        return "#{}".format(self._receiver_id)
