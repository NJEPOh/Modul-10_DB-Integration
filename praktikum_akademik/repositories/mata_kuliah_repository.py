class MataKuliahRepository:
    def __init__(self, database):
        self.database = database

    def tambah(self, matkul):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO mata_kuliah
                    (kode_matkul, nama_matkul, sks) VALUES (%s, %s, %s)""",
                    (matkul.kode_matkul, matkul.nama_matkul, matkul.sks))
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
                cur.execute("SELECT * FROM mata_kuliah ORDER BY id_matkul")
                return cur.fetchall()
        finally:
            conn.close()

    def ubah(self, id_matkul, matkul):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("""UPDATE mata_kuliah
                    SET kode_matkul=%s, nama_matkul=%s, sks=%s
                    WHERE id_matkul=%s""",
                    (matkul.kode_matkul, matkul.nama_matkul, matkul.sks, id_matkul))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def hapus(self, id_matkul):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM mata_kuliah WHERE id_matkul=%s", (id_matkul,))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
