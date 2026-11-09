class PeminjamanRepository:
    def __init__(self, database):
        self.database = database

    def tambah_transaksi(self, peminjaman, daftar_detail):
        """
        Menyimpan header peminjaman beserta seluruh detail buku dalam
        satu transaksi. Jika salah satu detail gagal disimpan (misal ID buku
        tidak valid atau duplikat), seluruh transaksi di-rollback.
        """
        if not daftar_detail:
            raise ValueError("Transaksi peminjaman wajib memiliki minimal 1 detail buku.")

        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO peminjaman
                       (id_anggota, id_petugas, tanggal_pinjam, tanggal_kembali, status)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (
                        peminjaman.id_anggota,
                        peminjaman.id_petugas,
                        peminjaman.tanggal_pinjam,
                        peminjaman.tanggal_kembali,
                        peminjaman.status,
                    ),
                )
                id_peminjaman = cur.lastrowid

                for detail in daftar_detail:
                    cur.execute(
                        """INSERT INTO detail_peminjaman
                           (id_peminjaman, id_buku, jumlah)
                           VALUES (%s, %s, %s)""",
                        (id_peminjaman, detail.id_buku, detail.jumlah),
                    )

            conn.commit()
            return id_peminjaman
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def tampilkan_semua(self):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT p.id_peminjaman,
                              a.nomor_anggota,
                              a.nama AS nama_anggota,
                              pt.nama_petugas,
                              p.tanggal_pinjam,
                              p.tanggal_kembali,
                              p.status
                       FROM peminjaman p
                       JOIN anggota a ON a.id_anggota = p.id_anggota
                       JOIN petugas pt ON pt.id_petugas = p.id_petugas
                       ORDER BY p.id_peminjaman DESC"""
                )
                return cur.fetchall()
        finally:
            conn.close()

    def ubah_status(self, id_peminjaman, status_baru):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE peminjaman SET status=%s WHERE id_peminjaman=%s",
                    (status_baru, id_peminjaman),
                )
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def hapus(self, id_peminjaman):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM peminjaman WHERE id_peminjaman=%s",
                    (id_peminjaman,),
                )
                changed = cur.rowcount
            conn.commit()
            return changed > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def laporan_riwayat_peminjaman(self, nomor_anggota=None):
        conn = self.database.connect()
        try:
            with conn.cursor() as cur:
                query = """
                    SELECT
                        p.id_peminjaman,
                        a.nomor_anggota,
                        a.nama AS nama_anggota,
                        pt.nama_petugas,
                        p.tanggal_pinjam,
                        p.tanggal_kembali,
                        p.status,
                        b.kode_buku,
                        b.judul AS judul_buku,
                        dp.jumlah
                    FROM peminjaman p
                    JOIN anggota a
                        ON a.id_anggota = p.id_anggota
                    JOIN petugas pt
                        ON pt.id_petugas = p.id_petugas
                    JOIN detail_peminjaman dp
                        ON dp.id_peminjaman = p.id_peminjaman
                    JOIN buku b
                        ON b.id_buku = dp.id_buku
                """
                params = ()
                if nomor_anggota:
                    query += " WHERE a.nomor_anggota = %s"
                    params = (nomor_anggota,)
                query += " ORDER BY p.tanggal_pinjam DESC, p.id_peminjaman DESC, b.kode_buku"

                cur.execute(query, params)
                return cur.fetchall()
        finally:
            conn.close()
