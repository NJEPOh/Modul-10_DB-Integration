from database import Database
from models.program_studi import ProgramStudi
from models.mahasiswa import Mahasiswa
from models.mata_kuliah import MataKuliah
from models.krs import KRS
from repositories.program_studi_repository import ProgramStudiRepository
from repositories.mahasiswa_repository import MahasiswaRepository
from repositories.mata_kuliah_repository import MataKuliahRepository
from repositories.krs_repository import KRSRepository

db = Database()
prodi_repo = ProgramStudiRepository(db)
mahasiswa_repo = MahasiswaRepository(db)
matkul_repo = MataKuliahRepository(db)
krs_repo = KRSRepository(db)


def tampilkan(rows):
    if not rows:
        print("Data belum tersedia.")
        return
    for row in rows:
        print(row)


def menu():
    while True:
        print("\n=== SISTEM INFORMASI AKADEMIK ===")
        print("1. Program Studi")
        print("2. Mahasiswa")
        print("3. Mata Kuliah")
        print("4. KRS")
        print("5. Laporan KRS (JOIN)")
        print("0. Keluar")
        pilihan = input("Pilih: ").strip()

        try:
            if pilihan == "1":
                print("1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = ProgramStudi(input("Nama prodi: "), input("Jenjang: "))
                    print("ID baru:", prodi_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(prodi_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = int(input("ID prodi: "))
                    obj = ProgramStudi(input("Nama baru: "), input("Jenjang baru: "))
                    print("Berhasil." if prodi_repo.ubah(id_, obj) else "Data tidak ditemukan.")
                elif aksi == "4":
                    id_ = int(input("ID prodi: "))
                    print("Berhasil." if prodi_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "2":
                print("1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = Mahasiswa(input("NIM: "), input("Nama: "),
                                    input("Email: ") or None,
                                    int(input("ID prodi: ")))
                    print("ID baru:", mahasiswa_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(mahasiswa_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = int(input("ID mahasiswa: "))
                    obj = Mahasiswa(input("NIM baru: "), input("Nama baru: "),
                                    input("Email baru: ") or None,
                                    int(input("ID prodi baru: ")))
                    print("Berhasil." if mahasiswa_repo.ubah(id_, obj) else "Data tidak ditemukan.")
                elif aksi == "4":
                    id_ = int(input("ID mahasiswa: "))
                    print("Berhasil." if mahasiswa_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "3":
                print("1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = MataKuliah(input("Kode: "), input("Nama: "),
                                     int(input("SKS: ")))
                    print("ID baru:", matkul_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(matkul_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = int(input("ID mata kuliah: "))
                    obj = MataKuliah(input("Kode baru: "), input("Nama baru: "),
                                     int(input("SKS baru: ")))
                    print("Berhasil." if matkul_repo.ubah(id_, obj) else "Data tidak ditemukan.")
                elif aksi == "4":
                    id_ = int(input("ID mata kuliah: "))
                    print("Berhasil." if matkul_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "4":
                print("1 Tambah KRS | 2 Tampilkan KRS | 3 Hapus KRS")
                aksi = input("Pilih aksi: ").strip()
                if aksi == "1":
                    obj = KRS(int(input("ID mahasiswa: ")),
                              int(input("ID mata kuliah: ")),
                              int(input("Semester: ")),
                              input("Tahun akademik (mis. 2026/2027): "))
                    print("ID KRS baru:", krs_repo.tambah(obj))
                elif aksi == "2":
                    tampilkan(krs_repo.tampilkan_semua())
                elif aksi == "3":
                    id_ = int(input("ID KRS: "))
                    print("Berhasil." if krs_repo.hapus(id_) else "Data tidak ditemukan.")

            elif pilihan == "5":
                nim = input("Masukkan NIM mahasiswa: ").strip()
                data = krs_repo.laporan_berdasarkan_nim(nim)
                if data:
                    print("\n=== LAPORAN KRS MAHASISWA ===")
                    print("NIM              :", data[0]["nim"])
                    print("Nama             :", data[0]["nama_mahasiswa"])
                    print("Program Studi    :", data[0]["nama_prodi"])
                    print("-" * 75)
                    print(f"{'Kode MK':<12} {'Mata Kuliah':<35} {'SKS':<5} {'Semester':<10} {'Tahun Akademik'}")
                    print("-" * 75)
                    total_sks = 0
                    for row in data:
                        print(
                            f"{row['kode_matkul']:<12} "
                            f"{row['nama_matkul']:<35} "
                            f"{row['sks']:<5} "
                            f"{row['semester']:<10} "
                            f"{row['tahun_akademik']}"
                        )
                        total_sks += row["sks"]
                    print("-" * 75)
                    print("Total SKS:", total_sks)
                else:
                    print("Data KRS tidak ditemukan untuk NIM tersebut.")
            elif pilihan == "0":
                print("Program selesai.")
                break
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Input angka tidak valid.")
        except Exception as error:
            print("Operasi gagal:", error)


if __name__ == "__main__":
    menu()
