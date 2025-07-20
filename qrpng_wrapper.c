#include <stdlib.h>
#include <string.h>
#include <qrencode.h>

__declspec(dllexport)
int generate_qr_mono_bitmap(const unsigned char* data, int length,
                            unsigned char** out_bitmap, int* width_out) {
    if (!data || length <= 0 || !out_bitmap || !width_out)
        return -1;

    QRcode* qr = QRcode_encodeData(length, data, 0, QR_ECLEVEL_L);
    if (!qr) return -2;

    int width = qr->width;
    int size = width * width;

    unsigned char* bitmap = (unsigned char*)malloc(size);
    if (!bitmap) {
        QRcode_free(qr);
        return -3;
    }

    // Копируем и нормализуем (0 или 1)
    for (int i = 0; i < size; i++) {
        bitmap[i] = (qr->data[i] & 1);
    }

    *out_bitmap = bitmap;
    *width_out = width;

    QRcode_free(qr);
    return 0;
}

__declspec(dllexport)
void free_qr_bitmap(unsigned char* ptr) {
    if (ptr) free(ptr);
}
