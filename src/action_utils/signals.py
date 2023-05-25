
class Signal:
    def __init__(self, message, sender, receiver):
        self.message = message
        self.sender = sender
        self.receiver = receiver

    def send(self, broadcast=False):
        if self.receiver:
            print(f"Signal sent {self}{' as broadcast' if broadcast else ''}")
            self.receiver.read_signal(self, broadcast)

    def __str__(self):
        return f"Signal({self.__dict__})"


def send_signal(message, sender, receiver, broadcast=False):
    signal = Signal(message, sender, receiver)
    signal.send(broadcast)
    return signal
