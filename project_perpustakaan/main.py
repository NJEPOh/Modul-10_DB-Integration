from datetime import datetime
from database import Database
from models.anggota import Anggota
from models.buku import Buku
from models.petugas import Petugas
from models.peminjaman import Peminjaman
from models.detail_peminjaman import DetailPeminjaman
from repositories.anggota_repository import AnggotaRepository
from repositories.buku_repository import BukuRepository
from repositories.petugas_repository import PetugasRepository
from repositories.peminjaman_repository import PeminjamanRepository

db = Database()
anggota_repo = AnggotaRepository(db)
buku_repo = BukuRepository(db)
petugas_repo = PetugasRepository(db)
peminjaman_repo = PeminjamanRepository(db)


def input_wajib(prompt):
    nilai = input(prompt).strip()
    if not nilai:
        raise ValueError("Input tidak boleh kosong.")
    return nilai


def input_int_positif(prompt):
    nilai = int(input(prompt).strip())
    if nilai <= 0:
        raise ValueError("Nilai angka harus lebih besar dari 0.")
    return nilai


def input_tanggal(prompt):
    teks = input_wajib(prompt)
    try:
        datetime.strptime(teks, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Format tanggal tidak valid. Gunakan format YYYY-MM-DD (mis. 2026-11-09).")
    return teks


def tampilkan(rows):
    if not rows:
        print("Data belum tersedia.")
        return
    for row in rows:
        print(row)


def cetak_laporan_peminjaman(data):
    if not data:
        print("Data riwayat peminjaman tidak ditemukan.")
        return

    print("\n=== LAPORAN RIWAYAT PEMINJAMAN PERPUSTAKAAN ===")
    print("-" * 105)
    print(
        f"{'ID':<4} {'No Anggota':<11} {'Nama Anggota':<18} "
        f"{'Petugas':<15} {'Tgl Pinjam':<12} {'Tgl Kembali':<12} "
        f"{'Status':<13} {'Buku (Jml)'}"
    )
    print("-" * 105)
    total_buku = 0
    for row in data:
        info_buku = f"[{row['kode_buku']}] {row['judul_buku']} ({row['jumlah']})"
        print(
            f"{row['id_peminjaman']:<4} "
            f"{row['nomor_anggota']:<11} "
            f"{row['nama_anggota']:<18} "
            f"{row['nama_petugas']:<15} "
            f"{str(row['tanggal_pinjam']):<12} "
            f"{str(row['tanggal_kembali']):<12} "
            f"{row['status']:<13} "
            f"{info_buku}"
        )
        total_buku += row["jumlah"]
    print("-" * 105)
    print("Total Eksemplar Buku pada Laporan:", total_buku)


def menu():
    while True:
        print("\n=== SISTEM INFORMASI PERPUSTAKAAN ===")
        print("1. Kelola Anggota")
        print("2. Kelola Buku")
        print("3. Kelola Petugas")
        print("4. Transaksi Peminjaman & Pengembalian")
        print("5. Laporan Riwayat Peminjaman (JOIN)")
        print("0. Keluar")
        pilihan = input("Pilih: ").strip()

        try:
            if pilihan == "1":
                print("1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = Anggota(
                        input_wajib("Nomor anggota: "),
                        input_wajib("Nama anggota: "),
                        input_wajib("Alamat: "),
                        input_wajib("Nomor telepon: "),
                    )
                    print("ID anggota baru:", anggota_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(anggota_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = input_int_positif("ID anggota: ")
                    obj = Anggota(
                        input_wajib("Nomor anggota baru: "),
                        input_wajib("Nama anggota baru: "),
                        input_wajib("Alamat baru: "),
                        input_wajib("Nomor telepon baru: "),
                    )
                    print("Berhasil." if anggota_repo.ubah(id_, obj) else "Data tidak ditemukan.")
                elif aksi == "4":
                    id_ = input_int_positif("ID anggota: ")
                    print("Berhasil." if anggota_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "2":
                print("1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = Buku(
                        input_wajib("Kode buku: "),
                        input_wajib("Judul buku: "),
                        input_wajib("Penulis: "),
                        input_int_positif("Tahun terbit: "),
                        input_wajib("Kategori: "),
                    )
                    print("ID buku baru:", buku_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(buku_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = input_int_positif("ID buku: ")
                    obj = Buku(
                        input_wajib("Kode buku baru: "),
                        input_wajib("Judul buku baru: "),
                        input_wajib("Penulis baru: "),
                        input_int_positif("Tahun terbit baru: "),
                        input_wajib("Kategori baru: "),
                    )
                    print("Berhasil." if buku_repo.ubah(id_, obj) else "Data tidak ditemukan.")
                elif aksi == "4":
                    id_ = input_int_positif("ID buku: ")
                    print("Berhasil." if buku_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "3":
                print("1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = Petugas(
                        input_wajib("Nama petugas: "),
                        input_wajib("Username: "),
                    )
                    print("ID petugas baru:", petugas_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(petugas_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = input_int_positif("ID petugas: ")
                    obj = Petugas(
                        input_wajib("Nama petugas baru: "),
                        input_wajib("Username baru: "),
                    )
                    print("Berhasil." if petugas_repo.ubah(id_, obj) else "Data tidak ditemukan.")
                elif aksi == "4":
                    id_ = input_int_positif("ID petugas: ")
                    print("Berhasil." if petugas_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "4":
                print("1 Buat Transaksi Peminjaman | 2 Tampilkan Peminjaman | 3 Ubah Status/Kembalikan | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    id_anggota = input_int_positif("ID anggota: ")
                    id_petugas = input_int_positif("ID petugas: ")
                    tgl_pinjam = input_tanggal("Tanggal pinjam (YYYY-MM-DD): ")
                    tgl_kembali = input_tanggal("Tanggal kembali (YYYY-MM-DD): ")
                    if tgl_kembali < tgl_pinjam:
                        raise ValueError("Tanggal kembali tidak boleh lebih awal dari tanggal pinjam.")

                    peminjaman_obj = Peminjaman(
                        id_anggota=id_anggota,
                        id_petugas=id_petugas,
                        tanggal_pinjam=tgl_pinjam,
                        tanggal_kembali=tgl_kembali,
                        status="Dipinjam",
                    )

                    banyak_item = input_int_positif("Jumlah jenis buku yang dipinjam: ")
                    daftar_detail = []
                    for i in range(banyak_item):
                        print(f"-- Detail Buku ke-{i + 1} --")
                        id_buku = input_int_positif("ID buku: ")
                        jumlah = input_int_positif("Jumlah eksemplar: ")
                        daftar_detail.append(DetailPeminjaman(id_buku=id_buku, jumlah=jumlah))

                    id_baru = peminjaman_repo.tambah_transaksi(peminjaman_obj, daftar_detail)
                    print("Transaksi peminjaman berhasil disimpan. ID peminjaman:", id_baru)

                elif aksi == "2":
                    tampilkan(peminjaman_repo.tampilkan_semua())

                elif aksi == "3":
                    id_peminjaman = input_int_positif("ID peminjaman: ")
                    status_baru = input_wajib("Status baru (Dipinjam / Dikembalikan): ")
                    if status_baru not in ("Dipinjam", "Dikembalikan"):
                        raise ValueError("Status hanya boleh 'Dipinjam' atau 'Dikembalikan'.")
                    print(
                        "Berhasil."
                        if peminjaman_repo.ubah_status(id_peminjaman, status_baru)
                        else "Data tidak ditemukan."
                    )

                elif aksi == "4":
                    id_peminjaman = input_int_positif("ID peminjaman: ")
                    print("Berhasil." if peminjaman_repo.hapus(id_peminjaman) else "Data tidak ditemukan.")

            elif pilihan == "5":
                print("1 Semua Riwayat Peminjaman | 2 Cari Berdasarkan Nomor Anggota")
                sub = input("Pilih laporan: ").strip()
                if sub == "1":
                    data = peminjaman_repo.laporan_riwayat_peminjaman()
                    cetak_laporan_peminjaman(data)
                elif sub == "2":
                    nomor = input_wajib("Masukkan Nomor Anggota (mis. ANG001): ")
                    data = peminjaman_repo.laporan_riwayat_peminjaman(nomor)
                    cetak_laporan_peminjaman(data)

            elif pilihan == "0":
                print("Program selesai.")
                break
            else:
                print("Pilihan tidak valid.")
        except ValueError as ve:
            print("Validasi gagal:", ve)
        except Exception as error:
            print("Operasi gagal:", error)


if __name__ == "__main__":
    menu()
