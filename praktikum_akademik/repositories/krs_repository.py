class KRSRepository:
    def __init__(self, database):
        self.database = database

    def tambah(self, krs):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO krs
                    (id_mahasiswa, id_matkul, semester, tahun_akademik)
                    VALUES (%s, %s, %s, %s)""",
                    (krs.id_mahasiswa, krs.id_matkul, krs.semester,
                     krs.tahun_akademik))
                id_baru = cur.lastrowid
            conn.commit()
            return id_baru
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def tampilkan_semua(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""SELECT k.id_krs, m.nim, m.nama,
                    mk.kode_matkul, mk.nama_matkul, mk.sks,
                    k.semester, k.tahun_akademik
                    FROM krs k
                    JOIN mahasiswa m ON m.id_mahasiswa=k.id_mahasiswa
                    JOIN mata_kuliah mk ON mk.id_matkul=k.id_matkul
                    ORDER BY k.tahun_akademik, k.semester, m.nim""")
                return cur.fetchall()
        finally:
            conn.close()

    def hapus(self, id_krs):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM krs WHERE id_krs=%s", (id_krs,))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def laporan_berdasarkan_nim(self, nim):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        m.nim,
                        m.nama AS nama_mahasiswa,
                        p.nama_prodi,
                        mk.kode_matkul,
                        mk.nama_matkul,
                        mk.sks,
                        k.semester,
                        k.tahun_akademik
                    FROM krs k
                    JOIN mahasiswa m
                        ON m.id_mahasiswa = k.id_mahasiswa
                    JOIN program_studi p
                        ON p.id_prodi = m.id_prodi
                    JOIN mata_kuliah mk
                        ON mk.id_matkul = k.id_matkul
                    WHERE m.nim = %s
                    ORDER BY k.tahun_akademik, k.semester, mk.kode_matkul
                """, (nim,))
                return cur.fetchall()
        finally:
            conn.close()
