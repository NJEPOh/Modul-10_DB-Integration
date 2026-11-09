class MahasiswaRepository:
    def __init__(self, database):
        self.database = database

    def tambah(self, mahasiswa):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO mahasiswa (nim, nama, email, id_prodi)
                       VALUES (%s, %s, %s, %s)""",
                    (mahasiswa.nim, mahasiswa.nama, mahasiswa.email, mahasiswa.id_prodi)
                )
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
                cur.execute("""SELECT m.id_mahasiswa, m.nim, m.nama, m.email,
                                      p.nama_prodi
                               FROM mahasiswa m
                               JOIN program_studi p ON p.id_prodi=m.id_prodi
                               ORDER BY m.id_mahasiswa""")
                return cur.fetchall()
        finally:
            conn.close()

    def ubah(self, id_mahasiswa, mahasiswa):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""UPDATE mahasiswa
                    SET nim=%s, nama=%s, email=%s, id_prodi=%s
                    WHERE id_mahasiswa=%s""",
                    (mahasiswa.nim, mahasiswa.nama, mahasiswa.email,
                     mahasiswa.id_prodi, id_mahasiswa))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def hapus(self, id_mahasiswa):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM mahasiswa WHERE id_mahasiswa=%s",
                            (id_mahasiswa,))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
