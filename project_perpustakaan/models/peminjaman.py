class Peminjaman:
    def __init__(
        self,
        id_anggota,
        id_petugas,
        tanggal_pinjam,
        tanggal_kembali,
        status="Dipinjam",
        id_peminjaman=None,
    ):
        self.id_peminjaman = id_peminjaman
        self.id_anggota = id_anggota
        self.id_petugas = id_petugas
        self.tanggal_pinjam = tanggal_pinjam
        self.tanggal_kembali = tanggal_kembali
        self.status = status

    def __str__(self):
        return (
            f"{self.id_peminjaman} | Anggota: {self.id_anggota} | "
            f"Petugas: {self.id_petugas} | Pinjam: {self.tanggal_pinjam} | "
            f"Kembali: {self.tanggal_kembali} | Status: {self.status}"
        )
