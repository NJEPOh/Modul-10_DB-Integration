-- ============================================================
-- SQL Script: Database Sistem Informasi Perpustakaan (Modul 10)
-- DBMS: MySQL / MariaDB
-- ============================================================

CREATE DATABASE IF NOT EXISTS perpustakaan
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE perpustakaan;

-- 1. Tabel anggota
CREATE TABLE IF NOT EXISTS anggota (
    id_anggota INT AUTO_INCREMENT PRIMARY KEY,
    nomor_anggota VARCHAR(20) NOT NULL UNIQUE,
    nama VARCHAR(100) NOT NULL,
    alamat VARCHAR(255) NOT NULL,
    nomor_telepon VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

-- 2. Tabel buku
CREATE TABLE IF NOT EXISTS buku (
    id_buku INT AUTO_INCREMENT PRIMARY KEY,
    kode_buku VARCHAR(20) NOT NULL UNIQUE,
    judul VARCHAR(150) NOT NULL,
    penulis VARCHAR(100) NOT NULL,
    tahun_terbit INT NOT NULL,
    kategori VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- 3. Tabel petugas
CREATE TABLE IF NOT EXISTS petugas (
    id_petugas INT AUTO_INCREMENT PRIMARY KEY,
    nama_petugas VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 4. Tabel peminjaman
CREATE TABLE IF NOT EXISTS peminjaman (
    id_peminjaman INT AUTO_INCREMENT PRIMARY KEY,
    id_anggota INT NOT NULL,
    id_petugas INT NOT NULL,
    tanggal_pinjam DATE NOT NULL,
    tanggal_kembali DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Dipinjam',
    CONSTRAINT fk_peminjaman_anggota
        FOREIGN KEY (id_anggota) REFERENCES anggota(id_anggota)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_peminjaman_petugas
        FOREIGN KEY (id_petugas) REFERENCES petugas(id_petugas)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 5. Tabel detail_peminjaman
CREATE TABLE IF NOT EXISTS detail_peminjaman (
    id_detail INT AUTO_INCREMENT PRIMARY KEY,
    id_peminjaman INT NOT NULL,
    id_buku INT NOT NULL,
    jumlah INT NOT NULL,
    CONSTRAINT fk_detail_peminjaman
        FOREIGN KEY (id_peminjaman) REFERENCES peminjaman(id_peminjaman)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_detail_buku
        FOREIGN KEY (id_buku) REFERENCES buku(id_buku)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT uq_peminjaman_buku
        UNIQUE (id_peminjaman, id_buku)
) ENGINE=InnoDB;

-- ============================================================
-- Data Awal (Seed Data)
-- ============================================================

INSERT INTO anggota (nomor_anggota, nama, alamat, nomor_telepon) VALUES
('ANG001', 'Andi Pratama', 'Jl. Ir. Sutami No. 36A, Surakarta', '081234567801'),
('ANG002', 'Budi Santoso', 'Jl. Slamet Riyadi No. 120, Surakarta', '081234567802'),
('ANG003', 'Citra Lestari', 'Jl. Ahmad Yani No. 200, Kartasura', '081234567803');

INSERT INTO buku (kode_buku, judul, penulis, tahun_terbit, kategori) VALUES
('BK001', 'Pemrograman Python Dasar', 'Abdul Kadir', 2023, 'Pemrograman'),
('BK002', 'Sistem Basis Data Relasional', 'Fathansyah', 2022, 'Basis Data'),
('BK003', 'Rekayasa Perangkat Lunak Terstruktur', 'Rosa A.S.', 2024, 'Rekayasa Perangkat Lunak');

INSERT INTO petugas (nama_petugas, username) VALUES
('Dewi Kusuma', 'dewi_admin'),
('Rizky Saputra', 'rizky_staff');

INSERT INTO peminjaman (id_anggota, id_petugas, tanggal_pinjam, tanggal_kembali, status) VALUES
(1, 1, '2026-11-01', '2026-11-08', 'Dipinjam'),
(2, 2, '2026-10-20', '2026-10-27', 'Dikembalikan');

INSERT INTO detail_peminjaman (id_peminjaman, id_buku, jumlah) VALUES
(1, 1, 1),
(1, 2, 1),
(2, 3, 2);
