class PetugasRepository:
    def __init__(self, database):
        self.database = database

    def tambah(self, petugas):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO petugas (nama_petugas, username)
                       VALUES (%s, %s)""",
                    (petugas.nama_petugas, petugas.username),
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
                cur.execute("SELECT * FROM petugas ORDER BY id_petugas")
                return cur.fetchall()
        finally:
            conn.close()

    def ubah(self, id_petugas, petugas):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE petugas
                       SET nama_petugas=%s, username=%s
                       WHERE id_petugas=%s""",
                    (petugas.nama_petugas, petugas.username, id_petugas),
                )
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def hapus(self, id_petugas):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM petugas WHERE id_petugas=%s", (id_petugas,)
                )
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
