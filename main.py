from revelare.gui.main import AppWindow
from revelare.gui.steganography import StegoAppState, connect_app_to_state
from revelare.gui.cryptography import CryptoAppState, connect_cryptography


from PyQt5.QtWidgets import QApplication


class RevelareApplication(AppWindow):
    crypto_state = CryptoAppState()
    stego_state = StegoAppState()

    def __init__(self) -> None:
        super().__init__()
        self.connect_buttons()

    def connect_buttons(self):
        connect_app_to_state(self, self.stego_state)
        connect_cryptography(self, self.crypto_state)


def window():
    import sys

    app = QApplication(sys.argv)
    win = RevelareApplication()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()
