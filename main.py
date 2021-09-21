from stegano.utils import bmp_to_bytes, bytes_to_bmp
from stegano.steganography import extract_message, inject_message

b = bmp_to_bytes("./mocks/bmp/snail.bmp")
img = inject_message(b, "asdas")
extract_message(img)
bytes_to_bmp(img, "lol.bmp")
