"""
Script pembantu untuk membuat database `akademik`, seluruh tabel,
dan mengisi data awal (seed data) secara otomatis melalui Python.
"""
import pymysql
from database import Database


def setup():
    db = Database()
    server_config = {
        "host": db.config["host"],
        "user": db.config["user"],
        "password": db.config["password"],
        "charset": db.config["charset"],
        "cursorclass": db.config["cursorclass"],
        "autocommit": False,
    }

    conn = pymysql.connect(**server_config)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE DATABASE IF NOT EXISTS akademik "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"
            )
            cur.execute("USE akademik")

            cur.execute("""
                CREATE TABLE IF NOT EXISTS program_studi (
                    id_prodi INT AUTO_INCREMENT PRIMARY KEY,
                    nama_prodi VARCHAR(100) NOT NULL,
                    jenjang VARCHAR(10) NOT NULL
                ) ENGINE=InnoDB
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    id_mahasiswa INT AUTO_INCREMENT PRIMARY KEY,
                    nim VARCHAR(15) NOT NULL UNIQUE,
                    nama VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE,
                    id_prodi INT NOT NULL,
                    CONSTRAINT fk_mahasiswa_prodi
                        FOREIGN KEY (id_prodi) REFERENCES program_studi(id_prodi)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                ) ENGINE=InnoDB
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS mata_kuliah (
                    id_matkul INT AUTO_INCREMENT PRIMARY KEY,
                    kode_matkul VARCHAR(15) NOT NULL UNIQUE,
                    nama_matkul VARCHAR(100) NOT NULL,
                    sks INT NOT NULL
                ) ENGINE=InnoDB
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS krs (
                    id_krs INT AUTO_INCREMENT PRIMARY KEY,
                    id_mahasiswa INT NOT NULL,
                    id_matkul INT NOT NULL,
                    semester INT NOT NULL,
                    tahun_akademik VARCHAR(9) NOT NULL,
                    CONSTRAINT fk_krs_mahasiswa
                        FOREIGN KEY (id_mahasiswa) REFERENCES mahasiswa(id_mahasiswa)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    CONSTRAINT fk_krs_matkul
                        FOREIGN KEY (id_matkul) REFERENCES mata_kuliah(id_matkul)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    CONSTRAINT uq_krs
                        UNIQUE (id_mahasiswa, id_matkul, semester, tahun_akademik)
                ) ENGINE=InnoDB
            """)

            # Cek apakah data awal sudah ada
            cur.execute("SELECT COUNT(*) AS total FROM program_studi")
            if cur.fetchone()["total"] == 0:
                cur.execute("""
                    INSERT INTO program_studi (nama_prodi, jenjang) VALUES
                    ('Pendidikan Teknik Informatika dan Komputer', 'S1'),
                    ('Pendidikan Matematika', 'S1'),
                    ('Pendidikan Teknik Bangunan', 'S1')
                """)
                cur.execute("""
                    INSERT INTO mahasiswa (nim, nama, email, id_prodi) VALUES
                    ('K3524001', 'Andi', 'andi@email.com', 1),
                    ('K3524002', 'Budi', 'budi@email.com', 1),
                    ('K3524003', 'Citra', 'citra@email.com', 2)
                """)
                cur.execute("""
                    INSERT INTO mata_kuliah (kode_matkul, nama_matkul, sks) VALUES
                    ('PTIK101', 'Pemrograman Berorientasi Objek', 3),
                    ('PTIK102', 'Basis Data', 3),
                    ('PTIK103', 'Pemrograman Web', 3)
                """)
                cur.execute("""
                    INSERT INTO krs (id_mahasiswa, id_matkul, semester, tahun_akademik) VALUES
                    (1, 1, 3, '2026/2027'),
                    (1, 2, 3, '2026/2027'),
                    (2, 1, 3, '2026/2027'),
                    (3, 2, 3, '2026/2027')
                """)
                print("Database 'akademik', tabel, dan data awal berhasil dibuat.")
            else:
                print("Database 'akademik' dan tabel sudah siap (data awal sudah ada).")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print("Gagal menyiapkan database 'akademik':", e)
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    setup()
