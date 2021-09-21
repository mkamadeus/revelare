from stegano.utils import bmp_to_bytes, bytes_to_bmp
from stegano.steganography import extract_message, inject_message
from icecream import ic

b = bmp_to_bytes("./mocks/bmp/snail.bmp")
img = inject_message(b, "asdas", random=True)
msg = extract_message(img, random=True)
ic(msg)
bytes_to_bmp(img, "lol.bmp")
