import ctypes, os
from PIL import Image

# Загрузка DLL
base_path = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(base_path, "qrpng.dll")
qr = ctypes.CDLL(dll_path)

qr.generate_qr_mono_bitmap.argtypes = [
    ctypes.POINTER(ctypes.c_ubyte),  # data
    ctypes.c_int,                    # length
    ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)),  # out_bitmap
    ctypes.POINTER(ctypes.c_int),                 # width_out
]
qr.generate_qr_mono_bitmap.restype = ctypes.c_int

qr.free_qr_bitmap.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
qr.free_qr_bitmap.restype = None

def generate_qr(data: bytes, scale: int = 1) -> Image.Image:
    buf_ptr = ctypes.POINTER(ctypes.c_ubyte)()
    width = ctypes.c_int()

    data_arr = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)

    res = qr.generate_qr_mono_bitmap(
        data_arr,
        len(data),
        ctypes.byref(buf_ptr),
        ctypes.byref(width),
    )

    if res != 0:
        raise RuntimeError(f"QR generation failed: code {res}")

    try:
        size = width.value
        flat_data = ctypes.string_at(buf_ptr, size * size)

        # Создаём изображение: mode '1' = 1 бит на пиксель (черно-белое)
        # img = Image.frombytes('1', (size, size), flat_data)
        gray_data = bytes(255 - b * 255 for b in flat_data)
        img = Image.frombytes('L', (size, size), gray_data)
        img = img.resize((size * scale, size * scale), resample=Image.NEAREST)

        if scale > 1:
            img = img.resize((size * scale, size * scale), resample=Image.NEAREST)

        return img
    finally:
        qr.free_qr_bitmap(buf_ptr)

if __name__ == '__main__':
    img = generate_qr("Привет, мир!".encode('utf-8'), scale=4)
    img.show()