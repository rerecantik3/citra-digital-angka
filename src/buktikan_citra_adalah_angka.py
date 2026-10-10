"""
Pembuktian: citra digital = susunan angka (array/matriks).
Bahasa: Python (Pillow hanya untuk membaca/menyimpan file; analisis memakai NumPy).

Jalankan dari root repository:
    python src/buktikan_citra_adalah_angka.py
"""
import os
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PATH = "gambar/pantai.jpg"
OUT = "hasil"
os.makedirs(OUT, exist_ok=True)
os.makedirs("data", exist_ok=True)
np.set_printoptions(linewidth=140)


def judul(t):
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


# ---------------------------------------------------------------- 1
judul("1. Membuka file: dari file ke ARRAY ANGKA")
img = Image.open(PATH)
arr = np.array(img)  # titik kunci: gambar menjadi ndarray
print("Tipe objek      :", type(arr))
print("Bentuk (shape)  :", arr.shape, "-> (tinggi, lebar, kanal)")
print("Tipe data       :", arr.dtype, "-> bilangan bulat tak bertanda 8-bit")
print("Jumlah dimensi  :", arr.ndim)
H, W, C = arr.shape
print(f"Jumlah piksel   : {H} x {W} = {H*W:,}")
print(f"Jumlah angka    : {H} x {W} x {C} = {arr.size:,}")
print("Nilai minimum   :", arr.min(), "| maksimum:", arr.max())
print(f"Ukuran di memori: {arr.nbytes/1024/1024:.2f} MB (mentah, tanpa kompresi)")
print(f"Ukuran file JPEG: {os.path.getsize(PATH)/1024:.1f} KB (terkompresi)")

# ---------------------------------------------------------------- 2
judul("2. Satu piksel = 3 angka (R, G, B)")
for (y, x) in [(0, 0), (H // 2, W // 2), (H - 1, W - 1), (2000, 1000)]:
    r, g, b = arr[y, x]
    print(f"Piksel (baris={y:4d}, kolom={x:4d}) -> R={r:3d} G={g:3d} B={b:3d}")

# ---------------------------------------------------------------- 3
judul("3. Cuplikan matriks 8x8 per kanal (pojok kiri atas = baris 1900, kolom 600)")
y0, x0 = 1900, 600
patch = arr[y0:y0 + 8, x0:x0 + 8, :]
for i, nama in enumerate(["R (Merah)", "G (Hijau)", "B (Biru)"]):
    print(f"\nKanal {nama}:")
    print(patch[:, :, i])

# ---------------------------------------------------------------- 4
judul("4. Pembuktian terbalik: bangun gambar dari angka murni")
tangan = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 255, 255, 0, 0, 255, 255, 0],
                   [0, 255, 255, 0, 0, 255, 255, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 255, 0, 0, 0, 0, 255, 0],
                   [0, 0, 255, 0, 0, 255, 0, 0],
                   [0, 0, 0, 255, 255, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]], dtype=np.uint8)
print("Matriks yang diketik manual:\n", tangan)
Image.fromarray(tangan, mode="L").resize((256, 256), Image.NEAREST).save(f"{OUT}/04a_gambar_dari_angka.png")
grad = np.tile(np.linspace(0, 255, 256), (64, 1)).astype(np.uint8)
Image.fromarray(grad, mode="L").save(f"{OUT}/04b_gradasi_rumus.png")
rng = np.random.default_rng(42)
Image.fromarray(rng.integers(0, 256, (128, 128, 3), dtype=np.uint8)).resize((384, 384), Image.NEAREST).save(f"{OUT}/04c_noise_acak.png")
print("Tersimpan: 04a (smiley dari matriks), 04b (gradasi dari rumus), 04c (noise angka acak)")

# ---------------------------------------------------------------- 5
judul("5. Round-trip: array -> file PNG -> array (lossless, angka harus identik)")
Image.fromarray(arr).save(f"{OUT}/05_roundtrip.png")
arr2 = np.array(Image.open(f"{OUT}/05_roundtrip.png"))
print("Array identik 100%? ->", np.array_equal(arr, arr2))

# ---------------------------------------------------------------- 6
judul("6. Operasi matematika pada angka = pengolahan citra")
gray = (0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]).astype(np.uint8)
p = arr[1900, 600]
print("Grayscale = 0.299R + 0.587G + 0.114B -> shape", gray.shape)
print(f"Piksel (1900,600): RGB {p} -> gray {gray[1900, 600]} | hitung manual: "
      f"{0.299*int(p[0]) + 0.587*int(p[1]) + 0.114*int(p[2]):.2f}")
negatif = 255 - arr
biner = ((gray > 128) * 255).astype(np.uint8)
crop = arr[1500:2200, 0:900]
flip_h = arr[:, ::-1]
kecil = arr[::16, ::16]
print("Negatif  : 255 - nilai")
print("Biner    : 255 jika gray > 128, selain itu 0")
print("Crop     : arr[1500:2200, 0:900] ->", crop.shape)
print("Mirror   : arr[:, ::-1] (membalik urutan kolom)")
print("Downsample 1/16 : arr[::16, ::16] ->", kecil.shape)

# ---------------------------------------------------------------- 7
judul("7. Statistik (citra = kumpulan angka yang bisa dihitung)")
for i, n in enumerate("RGB"):
    k = arr[..., i]
    print(f"Kanal {n}: mean={k.mean():6.2f}  std={k.std():6.2f}  min={k.min():3d}  max={k.max():3d}")
print(f"Gray    : mean={gray.mean():6.2f}  std={gray.std():6.2f}")

# ---------------------------------------------------------------- 8
judul("8. Ekspor angka ke CSV / NPY (bisa dibuka di Excel/Notepad)")
np.savetxt("data/patch_gray_16x16.csv", gray[1900:1916, 600:616], fmt="%d", delimiter=",")
np.save("data/citra_penuh.npy", arr)
print("data/patch_gray_16x16.csv  (16x16 angka gray)")
print(f"data/citra_penuh.npy       (seluruh array, {os.path.getsize('data/citra_penuh.npy')/1e6:.1f} MB)")

# ---------------------------------------------------------------- 9
judul("9. Zoom bertingkat: dari gambar sampai angka")
fig, ax = plt.subplots(1, 4, figsize=(20, 5.5))
ax[0].imshow(arr); ax[0].set_title(f"Citra utuh {W}x{H}")
ax[0].add_patch(plt.Rectangle((560, 1860), 140, 140, fill=False, ec="red", lw=3))
ax[1].imshow(arr[1860:2000, 560:700]); ax[1].set_title("Zoom 140x140 piksel")
ax[1].add_patch(plt.Rectangle((40, 40), 16, 16, fill=False, ec="red", lw=2))
z2 = gray[1900:1916, 600:616]
ax[2].imshow(z2, cmap="gray", interpolation="nearest"); ax[2].set_title("Zoom 16x16 piksel (gray)")
z3 = z2[:8, :8]
ax[3].imshow(z3, cmap="gray", interpolation="nearest", vmin=0, vmax=255)
for (i, j), v in np.ndenumerate(z3):
    ax[3].text(j, i, int(v), ha="center", va="center", fontsize=11,
               color="white" if v < 128 else "black")
ax[3].set_title("Zoom 8x8: tiap kotak = 1 angka")
for a in ax:
    a.set_xticks([]); a.set_yticks([])
plt.tight_layout(); plt.savefig(f"{OUT}/09_zoom_bertingkat.png", dpi=110); plt.close()
print("Tersimpan: hasil/09_zoom_bertingkat.png")

# ---------------------------------------------------------------- 10
judul("10. Visualisasi kanal, operasi, dan histogram")
fig, ax = plt.subplots(2, 4, figsize=(20, 11))
ax = ax.ravel()
items = [("Asli", arr, None), ("Kanal R", arr[..., 0], "Reds"), ("Kanal G", arr[..., 1], "Greens"),
         ("Kanal B", arr[..., 2], "Blues"), ("Grayscale", gray, "gray"), ("Negatif", negatif, None),
         ("Biner (>128)", biner, "gray"), ("Mirror horizontal", flip_h, None)]
for a, (t, d, cm) in zip(ax, items):
    a.imshow(d, cmap=cm); a.set_title(t); a.axis("off")
plt.tight_layout(); plt.savefig(f"{OUT}/10_kanal_dan_operasi.png", dpi=60); plt.close()

fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
for i, c in enumerate("rgb"):
    ax[0].hist(arr[..., i].ravel(), bins=256, range=(0, 255), color=c, alpha=.5, label=c.upper())
ax[0].set_title("Histogram RGB"); ax[0].set_xlabel("Nilai intensitas (0-255)"); ax[0].set_ylabel("Jumlah piksel"); ax[0].legend()
ax[1].hist(gray.ravel(), bins=256, range=(0, 255), color="gray")
ax[1].set_title("Histogram Grayscale"); ax[1].set_xlabel("Nilai intensitas (0-255)")
plt.tight_layout(); plt.savefig(f"{OUT}/10b_histogram.png", dpi=100); plt.close()
print("Tersimpan: 10_kanal_dan_operasi.png, 10b_histogram.png")

# ---------------------------------------------------------------- 11
judul("11. Kuantisasi: mengurangi jumlah level angka")
fig, ax = plt.subplots(1, 4, figsize=(20, 5.5))
for a, bits in zip(ax, [8, 4, 2, 1]):
    lv = 2 ** bits
    step = 256 // lv
    q = (gray // step) * step
    a.imshow(q, cmap="gray", vmin=0, vmax=255); a.set_title(f"{bits}-bit = {lv} level"); a.axis("off")
    print(f"{bits}-bit -> {lv:3d} level keabuan, nilai unik nyata: {len(np.unique(q))}")
plt.tight_layout(); plt.savefig(f"{OUT}/11_kuantisasi.png", dpi=60); plt.close()

# ---------------------------------------------------------------- 12
judul("12. Bukti akhir: ubah ANGKA tertentu, gambar ikut berubah")
edit = arr.copy()
edit[1700:1760, 200:1700] = [255, 0, 0]
edit[1780:1840, 200:1700] = [0, 0, 0]
Image.fromarray(edit).save(f"{OUT}/12_edit_angka.png")
print("Baris 1700-1760 -> [255,0,0] (merah), baris 1780-1840 -> [0,0,0] (hitam)")

print("\nKESIMPULAN: citra digital = array numerik N-dimensi; "
      "semua operasi citra = operasi matematika pada array.")
