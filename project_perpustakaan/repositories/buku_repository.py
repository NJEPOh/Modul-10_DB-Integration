class BukuRepository:
    def __init__(self, database):
        self.database = database

    def tambah(self, buku):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO buku
                       (kode_buku, judul, penulis, tahun_terbit, kategori)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        buku.kode_buku,
                        buku.judul,
                        buku.penulis,
                        buku.tahun_terbit,
                        buku.kategori,
                    ),
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
                cur.execute("SELECT * FROM buku ORDER BY id_buku")
                return cur.fetchall()
        finally:
            conn.close()

    def ubah(self, id_buku, buku):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE buku
                       SET kode_buku=%s, judul=%s, penulis=%s, tahun_terbit=%s, kategori=%s
                       WHERE id_buku=%s""",
                    (
                        buku.kode_buku,
                        buku.judul,
                        buku.penulis,
                        buku.tahun_terbit,
                        buku.kategori,
                        id_buku,
                    ),
                )
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def hapus(self, id_buku):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM buku WHERE id_buku=%s", (id_buku,))
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
