from revelare.cryptography import crypt
from revelare.gui.main import AppWindow, show_open_file_dialog, show_save_file_dialog


def connect_cryptography(window: AppWindow):
    window.rc4KeyLineEdit.textChanged.connect(lambda: __crypto_refresh(window))
    window.MessageField.textChanged.connect(lambda: __crypto_refresh(window))
    window.messageLoadBtn.clicked.connect(lambda: __load_file(window))
    window.resultSaveBtn.clicked.connect(lambda: __save_file(window))


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


def __load_file(window: AppWindow):
    filename = show_open_file_dialog()
    with open(filename, "r", encoding="utf-8") as file:
        isi = file.read()
        # print(isi)
        window.MessageField.setText(isi)
        file.close()


def __save_file(window: AppWindow):
    filename = show_save_file_dialog()
    with open(filename, "w", encoding="utf-8") as file:
        file.write(window.ResultField.toPlainText())
        file.close()