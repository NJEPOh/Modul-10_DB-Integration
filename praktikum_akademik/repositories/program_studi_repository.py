class ProgramStudiRepository:
    def __init__(self, database):
        self.database = database

    def tambah(self, prodi):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO program_studi (nama_prodi, jenjang) VALUES (%s, %s)",
                    (prodi.nama_prodi, prodi.jenjang)
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
                cur.execute("SELECT * FROM program_studi ORDER BY id_prodi")
                return cur.fetchall()
        finally:
            conn.close()

    def ubah(self, id_prodi, prodi):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE program_studi SET nama_prodi=%s, jenjang=%s WHERE id_prodi=%s",
                    (prodi.nama_prodi, prodi.jenjang, id_prodi)
                )
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def hapus(self, id_prodi):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM program_studi WHERE id_prodi=%s", (id_prodi,))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
