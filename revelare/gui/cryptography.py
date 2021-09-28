from revelare.cryptography import crypt
from revelare.gui.main import AppWindow


def connect_cryptography(window: AppWindow):
    window.rc4KeyLineEdit.textChanged.connect(lambda: __crypto_refresh(window))
    window.MessageField.textChanged.connect(lambda: __crypto_refresh(window))


# ----- STATE UPDATE FUNCTIONS ----- #


def __crypto_refresh(window: AppWindow):
    newKey = window.rc4KeyLineEdit.text()
    newMessage = window.MessageField.toPlainText()
    result = crypt(newMessage, newKey)
    for i in range(256):
        window.permutationLineEdit[i].setText(str(result["perm"][i]))
        window.permutationLineEdit[i].setStyleSheet("border: 1px solid black")
    window.permutationLineEdit[result["keystream_obj"]["latest-i"]].setStyleSheet("border: 3px solid green;")
    window.permutationLineEdit[result["keystream_obj"]["latest-j"]].setStyleSheet("border: 3px solid blue;")
    window.permutationLineEdit[result["keystream_obj"]["latest-t"]].setStyleSheet("border: 3px solid red;")
    window.KeystreamField.setText(result["keystream"])
    window.ResultField.setText(result["result"])