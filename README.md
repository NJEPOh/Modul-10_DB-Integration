# Modul 10 — Integrasi Python dan MySQL/MariaDB (OOP: Model & Repository)

Repositori ini berisi implementasi lengkap kode program Python dan rancangan database MySQL/MariaDB berdasarkan **Modul 10 Praktikum Pemrograman Dasar** (S1 Pendidikan Teknik Informatika dan Komputer — Universitas Sebelas Maret), yang mencakup:

1. **Bagian C — Praktikum: Sistem Informasi Akademik** (`praktikum_akademik/`)
2. **Bagian F — Project Latihan: Sistem Informasi Perpustakaan** (`project_perpustakaan/`)

Seluruh program menerapkan konsep **Object-Oriented Programming (OOP)** dengan pemisahan lapisan **Database**, **Model**, **Repository**, dan **Program Utama (`main.py`)**, menggunakan parameterized query (`%s`), relasi **Primary Key & Foreign Key**, transaksi database (`commit` & `rollback`), serta laporan menggunakan **SQL JOIN**.

---

## Daftar Isi

1. [Struktur Folder Proyek](#1-struktur-folder-proyek)
2. [Prasyarat Perangkat Lunak](#2-prasyarat-perangkat-lunak)
3. [Tahap 1: Menjalankan Server MySQL/MariaDB](#3-tahap-1-menjalankan-server-mysqlmariadb)
4. [Tahap 2: Instalasi Library PyMySQL](#4-tahap-2-instalasi-library-pymysql)
5. [Tahap 3: Konfigurasi Koneksi Database (`database.py`)](#5-tahap-3-konfigurasi-koneksi-database-databasepy)
6. [Tahap 4: Membuat Database dan Tabel](#6-tahap-4-membuat-database-dan-tabel)
7. [Tahap 5: Menjalankan & Menggunakan Program](#7-tahap-5-menjalankan--menggunakan-program)
   - [A. Sistem Informasi Akademik (`praktikum_akademik`)](#a-sistem-informasi-akademik-praktikum_akademik)
   - [B. Sistem Informasi Perpustakaan (`project_perpustakaan`)](#b-sistem-informasi-perpustakaan-project_perpustakaan)
8. [Penjelasan Arsitektur OOP (Database, Model, Repository)](#8-penjelasan-arsitektur-oop-database-model-repository)
9. [Troubleshooting (Solusi Kendala Koneksi)](#9-troubleshooting-solusi-kendala-koneksi)

---

## 1. Struktur Folder Proyek

```text
Modul 10/
├── README.md
├── requirements.txt
├── Modul_10.docx
│
├── praktikum_akademik/                  # Bagian C: Sistem Informasi Akademik
│   ├── database_akademik.sql            # File SQL pembuatan DB, tabel, & data awal
│   ├── setup_db.py                      # Script otomatis membuat DB & tabel via Python
│   ├── database.py                      # Class Database (konfigurasi & koneksi PyMySQL)
│   ├── main.py                          # Program utama (menu interaktif terminal)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── program_studi.py             # Class Model ProgramStudi
│   │   ├── mahasiswa.py                 # Class Model Mahasiswa
│   │   ├── mata_kuliah.py               # Class Model MataKuliah
│   │   └── krs.py                       # Class Model KRS
│   └── repositories/
│       ├── __init__.py
│       ├── program_studi_repository.py  # CRUD Program Studi
│       ├── mahasiswa_repository.py      # CRUD Mahasiswa + JOIN Prodi
│       ├── mata_kuliah_repository.py    # CRUD Mata Kuliah
│       └── krs_repository.py            # CRUD KRS + Laporan JOIN berdasarkan NIM
│
└── project_perpustakaan/                # Bagian F: Sistem Informasi Perpustakaan
    ├── database_perpustakaan.sql        # File SQL pembuatan DB, tabel, & data awal
    ├── setup_db.py                      # Script otomatis membuat DB & tabel via Python
    ├── database.py                      # Class Database (konfigurasi & koneksi PyMySQL)
    ├── main.py                          # Program utama (menu interaktif & validasi)
    ├── models/
    │   ├── __init__.py
    │   ├── anggota.py                   # Class Model Anggota
    │   ├── buku.py                      # Class Model Buku
    │   ├── petugas.py                   # Class Model Petugas
    │   ├── peminjaman.py                # Class Model Peminjaman
    │   └── detail_peminjaman.py         # Class Model DetailPeminjaman
    └── repositories/
        ├── __init__.py
        ├── anggota_repository.py        # CRUD Anggota
        ├── buku_repository.py           # CRUD Buku
        ├── petugas_repository.py        # CRUD Petugas
        └── peminjaman_repository.py     # Transaksi Multi-Buku (Commit/Rollback) & JOIN
```

---

## 2. Prasyarat Perangkat Lunak

Pastikan perangkat lunak berikut telah terpasang pada komputer Anda:
- **Python 3** (disarankan Python 3.8 ke atas)
- **XAMPP** (menyediakan **MariaDB/MySQL** dan **phpMyAdmin**) atau MySQL Server mandiri
- **Visual Studio Code** atau terminal/Command Prompt/PowerShell
- **PyMySQL** (driver koneksi Python ke MySQL/MariaDB)

---

## 3. Tahap 1: Menjalankan Server MySQL/MariaDB

1. Buka aplikasi **XAMPP Control Panel**.
2. Klik tombol **Start** pada modul **MySQL** hingga indikator berubah menjadi hijau dan menampilkan port (umumnya `3306`).
3. *(Opsional)* Jika Anda ingin membuka antarmuka web **phpMyAdmin**, klik **Start** juga pada modul **Apache**, lalu buka browser dan akses `http://localhost/phpmyadmin`.

---

## 4. Tahap 2: Instalasi Library PyMySQL

Buka terminal / PowerShell pada direktori utama `Modul 10`, kemudian jalankan perintah berikut:

```bash
# Periksa versi Python
python --version

# Instal library PyMySQL menggunakan requirements.txt
pip install -r requirements.txt
```

Atau instal secara langsung dengan:

```bash
pip install pymysql
```

Untuk memastikan PyMySQL sudah terpasang dengan benar:

```bash
pip show pymysql
```

---

## 5. Tahap 3: Konfigurasi Koneksi Database (`database.py`)

Koneksi Python ke MySQL/MariaDB dikelola oleh class `Database` yang berada pada file:
- `praktikum_akademik/database.py` (untuk database `akademik`)
- `project_perpustakaan/database.py` (untuk database `perpustakaan`)

Berikut konfigurasi bawaan di dalam `database.py` (sesuai standar XAMPP):

```python
import pymysql

class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "akademik",  # atau "perpustakaan" pada project_perpustakaan
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": False,
        }

    def connect(self):
        return pymysql.connect(**self.config)
```

> **Catatan Penyesuaian Konfigurasi:**
> - **`host`**: Gunakan `"localhost"` atau `"127.0.0.1"`.
> - **`user`**: Default XAMPP adalah `"root"`.
> - **`password`**: Default XAMPP kosong (`""`). Jika MySQL Anda menggunakan password, isi sesuai password Anda.
> - **`port`**: Jika port MySQL Anda bukan `3306` (misalnya `3307`), tambahkan key `"port": 3307` di dalam `self.config`.
> - **`cursorclass`**: Menggunakan `pymysql.cursors.DictCursor` agar hasil query `SELECT` dikembalikan sebagai dictionary (`{"nim": "K3524001", ...}`).
> - **`autocommit`**: Diatur `False` agar transaksi dikendalikan secara eksplisit menggunakan `conn.commit()` dan `conn.rollback()`.

---

## 6. Tahap 4: Membuat Database dan Tabel

Anda dapat memilih **salah satu dari 2 cara** berikut untuk membuat database (`akademik` dan `perpustakaan`) beserta tabel dan data awalnya:

### Cara 1: Otomatis Menggunakan Script Python `setup_db.py` *(Paling Cepat)*

Pastikan MySQL di XAMPP sudah menyala dan konfigurasi `user`/`password` di `database.py` sudah sesuai, lalu jalankan:

```bash
# 1. Membuat database & tabel Sistem Informasi Akademik
cd praktikum_akademik
python setup_db.py

# 2. Membuat database & tabel Sistem Informasi Perpustakaan
cd ../project_perpustakaan
python setup_db.py
```

Jika berhasil, terminal akan menampilkan pesan:
- `Database 'akademik', tabel, dan data awal berhasil dibuat.`
- `Database 'perpustakaan', tabel, dan data awal berhasil dibuat.`

---

### Cara 2: Melalui phpMyAdmin (Import File `.sql` atau Tab SQL)

1. Buka browser dan akses `http://localhost/phpmyadmin`.
2. Klik menu **Import** di bagian atas (atau buka tab **SQL**).
3. Pilih file SQL yang sudah disediakan:
   - Untuk Praktikum Akademik: pilih file `praktikum_akademik/database_akademik.sql`
   - Untuk Project Perpustakaan: pilih file `project_perpustakaan/database_perpustakaan.sql`
4. Klik tombol **Import / Go** di bagian bawah halaman.
5. Database `akademik` (4 tabel) dan `perpustakaan` (5 tabel) beserta data awalnya akan langsung terbentuk.

---

## 7. Tahap 5: Menjalankan & Menggunakan Program

### A. Sistem Informasi Akademik (`praktikum_akademik`)

#### 1. Menjalankan Program
Buka terminal dan masuk ke folder `praktikum_akademik`:

```bash
cd praktikum_akademik
python main.py
```

#### 2. Panduan Menu & Penggunaan
Saat program dijalankan, menu utama berikut akan tampil:

```text
=== SISTEM INFORMASI AKADEMIK ===
1. Program Studi
2. Mahasiswa
3. Mata Kuliah
4. KRS
5. Laporan KRS (JOIN)
0. Keluar
Pilih:
```

- **Menu `1. Program Studi`**:
  - Pilih `1` (Tambah): Masukkan nama prodi (misal `Pendidikan Teknik Mesin`) dan jenjang (`S1`).
  - Pilih `2` (Tampilkan): Menampilkan seluruh program studi beserta `id_prodi`.
  - Pilih `3` (Ubah): Masukkan `ID prodi` yang ingin diubah, lalu isi nama dan jenjang baru.
  - Pilih `4` (Hapus): Masukkan `ID prodi` yang ingin dihapus (akan ditolak oleh Foreign Key `RESTRICT` jika masih ada mahasiswa pada prodi tersebut).
- **Menu `2. Mahasiswa`**:
  - Pilih `1` (Tambah): Masukkan `NIM` (unik), `Nama`, `Email` (boleh dikosongkan dengan menekan Enter), dan `ID prodi` yang valid.
  - Pilih `2` (Tampilkan): Menampilkan daftar mahasiswa beserta `nama_prodi` hasil `JOIN`.
  - Pilih `3` (Ubah) / `4` (Hapus): Mengubah atau menghapus data mahasiswa berdasarkan `ID mahasiswa`.
- **Menu `3. Mata Kuliah`**:
  - Mengelola data mata kuliah (`Kode`, `Nama`, `SKS`) dengan aksi `1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus`.
- **Menu `4. KRS`**:
  - Pilih `1` (Tambah KRS): Masukkan `ID mahasiswa`, `ID mata kuliah`, `Semester` (angka), dan `Tahun akademik` (wajib diisi, misal `2026/2027`).
  - Pilih `2` (Tampilkan KRS): Menampilkan seluruh pengambilan KRS.
  - Pilih `3` (Hapus KRS): Menghapus baris KRS berdasarkan `ID KRS`.
- **Menu `5. Laporan KRS (JOIN)`**:
  - Masukkan NIM mahasiswa (contoh data awal: `K3524001`).
  - Program akan menampilkan informasi mahasiswa, program studi, tabel daftar mata kuliah yang diambil, serta menghitung **Total SKS** secara otomatis:

```text
=== LAPORAN KRS MAHASISWA ===
NIM              : K3524001
Nama             : Andi
Program Studi    : Pendidikan Teknik Informatika dan Komputer
---------------------------------------------------------------------------
Kode MK      Mata Kuliah                         SKS   Semester   Tahun Akademik
---------------------------------------------------------------------------
PTIK101      Pemrograman Berorientasi Objek      3     3          2026/2027
PTIK102      Basis Data                          3     3          2026/2027
---------------------------------------------------------------------------
Total SKS: 6
```

---

### B. Sistem Informasi Perpustakaan (`project_perpustakaan`)

#### 1. Menjalankan Program
Buka terminal dan masuk ke folder `project_perpustakaan`:

```bash
cd project_perpustakaan
python main.py
```

#### 2. Panduan Menu & Penggunaan
Saat program dijalankan, menu utama berikut akan tampil:

```text
=== SISTEM INFORMASI PERPUSTAKAAN ===
1. Kelola Anggota
2. Kelola Buku
3. Kelola Petugas
4. Transaksi Peminjaman & Pengembalian
5. Laporan Riwayat Peminjaman (JOIN)
0. Keluar
Pilih:
```

- **Menu `1. Kelola Anggota`**:
  - Operasi CRUD (`1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus`) untuk data anggota (`nomor_anggota` UNIQUE, `nama`, `alamat`, `nomor_telepon`).
- **Menu `2. Kelola Buku`**:
  - Operasi CRUD (`1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus`) untuk data buku (`kode_buku` UNIQUE, `judul`, `penulis`, `tahun_terbit`, `kategori`).
- **Menu `3. Kelola Petugas`**:
  - Operasi CRUD (`1 Tambah | 2 Tampilkan | 3 Ubah | 4 Hapus`) untuk data petugas (`nama_petugas`, `username` UNIQUE).
- **Menu `4. Transaksi Peminjaman & Pengembalian`**:
  - **`1 Buat Transaksi Peminjaman`**:
    - Masukkan `ID anggota`, `ID petugas`, `Tanggal pinjam (YYYY-MM-DD)`, dan `Tanggal kembali (YYYY-MM-DD)`.
    - Masukkan **jumlah jenis buku** yang ingin dipinjam dalam 1 transaksi (bisa lebih dari 1 buku).
    - Untuk setiap jenis buku, masukkan `ID buku` dan `Jumlah eksemplar`.
    - **Mekanisme Transaksi (`commit` & `rollback`)**: Header peminjaman dan seluruh detail buku disimpan dalam satu transaksi database. Apabila salah satu detail buku gagal disimpan (misalnya `ID buku` tidak terdaftar di tabel `buku` atau buku yang sama dimasukkan dua kali dalam satu transaksi), maka `conn.rollback()` otomatis membatalkan seluruh transaksi sehingga tidak ada data peminjaman yang tersimpan sebagian.
  - **`2 Tampilkan Peminjaman`**: Menampilkan daftar transaksi peminjaman.
  - **`3 Ubah Status/Kembalikan`**: Mengubah status transaksi menjadi `Dikembalikan` atau `Dipinjam` berdasarkan `ID peminjaman`.
  - **`4 Hapus`**: Menghapus transaksi peminjaman berdasarkan `ID peminjaman`.
- **Menu `5. Laporan Riwayat Peminjaman (JOIN)`**:
  - Pilih `1` untuk menampilkan seluruh riwayat peminjaman (menggabungkan 5 tabel: `peminjaman`, `anggota`, `petugas`, `detail_peminjaman`, dan `buku`), atau pilih `2` untuk memfilter laporan berdasarkan `Nomor Anggota` (contoh data awal: `ANG001`).

---

## 8. Penjelasan Arsitektur OOP (Database, Model, Repository)

| Lapisan | File / Folder | Tanggung Jawab |
| :--- | :--- | :--- |
| **Database** | `database.py` | Menyimpan konfigurasi koneksi MySQL/MariaDB dan menyediakan method `connect()`. |
| **Model** | `models/*.py` | Merepresentasikan entitas domain (atribut, constructor `__init__`, dan method `__str__`). Tidak berisi query SQL. |
| **Repository** | `repositories/*.py` | Menjalankan operasi database (`INSERT`, `SELECT`, `UPDATE`, `DELETE`, `JOIN`), mengelola transaksi (`commit()` dan `rollback()`), serta menutup koneksi pada blok `finally`. |
| **Program Utama** | `main.py` | Menangani antarmuka menu pengguna, validasi input, membentuk objek Model, dan memanggil method Repository tanpa menulis SQL secara langsung. |

---

## 9. Troubleshooting (Solusi Kendala Koneksi)

1. **`OperationalError: (2003, "Can't connect to MySQL server on 'localhost'")`**
   - **Penyebab**: Layanan MySQL/MariaDB belum berjalan atau menggunakan port berbeda.
   - **Solusi**: Buka XAMPP Control Panel dan pastikan modul **MySQL** sudah berstatus **Running** (hijau). Jika port MySQL bukan `3306`, tambahkan `"port": <nomor_port>` pada `database.py`.

2. **`OperationalError: (1045, "Access denied for user 'root'@'localhost'")`**
   - **Penyebab**: Username atau password MySQL tidak sesuai dengan konfigurasi di `database.py`.
   - **Solusi**: Periksa dan sesuaikan nilai `"user"` dan `"password"` di dalam `database.py`.

3. **`OperationalError: (1049, "Unknown database 'akademik'")` atau `'perpustakaan'`**
   - **Penyebab**: Database belum dibuat di MySQL/MariaDB.
   - **Solusi**: Jalankan `python setup_db.py` pada masing-masing folder atau import file `.sql` melalui phpMyAdmin (lihat [Tahap 4](#6-tahap-4-membuat-database-dan-tabel)).

4. **`IntegrityError: (1452, 'Cannot add or update a child row: a foreign key constraint fails')`**
   - **Penyebab**: Anda memasukkan ID relasi (seperti `id_prodi`, `id_mahasiswa`, `id_matkul`, `id_anggota`, `id_petugas`, atau `id_buku`) yang belum terdaftar di tabel induknya.
   - **Solusi**: Tampilkan terlebih dahulu daftar data master untuk melihat ID yang tersedia sebelum menambahkan data transaksi.

5. **`IntegrityError: (1062, "Duplicate entry ... for key ...")`**
   - **Penyebab**: Nilai kolom ber-constraint `UNIQUE` (seperti `nim`, `kode_matkul`, kombinasi `krs`, `nomor_anggota`, `kode_buku`, atau `username`) sudah pernah didaftarkan sebelumnya.
   - **Solusi**: Gunakan kode/nomor unik yang berbeda.
