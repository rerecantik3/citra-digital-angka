# Citra Digital adalah Susunan Angka

Tugas: membuktikan dengan bahasa pemrograman bahwa sebuah citra digital tidak lain adalah susunan angka.

- **Bahasa**: Python 3 (NumPy, Pillow, Matplotlib)
- **Citra uji**: `gambar/pantai.jpg` (foto pantai, 1932 x 2576 piksel, RGB)
- **Skrip utama**: `src/buktikan_citra_adalah_angka.py`

## Cara menjalankan

```bash
pip install -r requirements.txt
python src/buktikan_citra_adalah_angka.py
```

Semua keluaran tersimpan di folder `hasil/` dan `data/`. Log terminal lengkap ada di `hasil/output_terminal.txt`.

## Ringkasan temuan

| Bukti | Hasil |
|---|---|
| Gambar dibaca menjadi `numpy.ndarray` | shape `(2576, 1932, 3)`, dtype `uint8` |
| Jumlah piksel | 4.976.832 |
| Jumlah angka penyusun | 14.930.496 (piksel x 3 kanal) |
| Rentang nilai | 0 sampai 255 (8 bit per kanal) |
| Satu piksel | 3 angka, contoh piksel (2000,1000) = R114 G136 B159 |
| Ukuran mentah vs file JPEG | 14,24 MB vs 464,6 KB (JPEG mengompresi angka yang sama) |
| Round-trip array -> PNG -> array | identik 100% (`np.array_equal` = True) |
| Gambar dari angka ketikan tangan | matriks 8x8 menghasilkan wajah smiley |
| Grayscale | `0.299R + 0.587G + 0.114B` cocok dengan hitungan manual (131,94 vs 131) |
| Edit angka | mengubah nilai piksel pada irisan array mengubah gambar |

## Langkah pembuktian (isi skrip)

1. **Gambar dibuka sebagai array**: `np.array(Image.open(...))` menghasilkan matriks 3 dimensi (tinggi x lebar x kanal).
2. **Satu piksel adalah tiga angka**: `arr[y, x]` mengembalikan `[R, G, B]`.
3. **Cuplikan matriks 8x8 per kanal**: angka mentah dicetak langsung ke terminal.
4. **Pembuktian terbalik**: gambar dibuat dari angka saja (matriks manual, gradasi dari rumus, noise acak). Lihat `hasil/04*.png`.
5. **Round-trip lossless**: array disimpan ke PNG, dibaca lagi, nilainya identik.
6. **Operasi matematika adalah pengolahan citra**: grayscale, negatif (`255 - x`), biner (ambang 128), crop (slicing), mirror (`[:, ::-1]`), rotasi (`np.rot90`), downsampling (`[::16, ::16]`).
7. **Statistik dan histogram**: rata-rata, simpangan baku, dan sebaran intensitas per kanal.
8. **Ekspor ke CSV**: `data/patch_gray_16x16.csv` bisa dibuka di Excel atau Notepad.
9. **Zoom bertingkat**: dari foto utuh sampai kotak 8x8 yang tiap kotaknya berisi satu angka (`hasil/09_zoom_bertingkat.png`).
10. **Pemisahan kanal**: R, G, B, grayscale, negatif, biner, mirror (`hasil/10_kanal_dan_operasi.png`).
11. **Kuantisasi**: 8, 4, 2, 1 bit per piksel, jumlah level angka menentukan detail (`hasil/11_kuantisasi.png`).
12. **Edit angka langsung**: dua pita warna dibuat hanya dengan menimpa nilai array (`hasil/12_edit_angka.png`).

## Struktur repository

```
citra-digital-angka/
├── README.md
├── requirements.txt
├── gambar/pantai.jpg
├── src/buktikan_citra_adalah_angka.py
├── data/patch_gray_16x16.csv
└── hasil/            (gambar keluaran + output_terminal.txt)
```

## Kesimpulan

Citra digital adalah array numerik. Setiap piksel menyimpan satu angka (grayscale) atau beberapa angka (RGB). Tampilan gambar muncul dari penerjemahan angka-angka itu menjadi warna oleh layar, dan setiap pengolahan citra adalah operasi matematika pada array tersebut.
