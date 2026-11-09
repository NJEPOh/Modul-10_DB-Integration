class DetailPeminjaman:
    def __init__(self, id_buku, jumlah, id_peminjaman=None, id_detail=None):
        self.id_detail = id_detail
        self.id_peminjaman = id_peminjaman
        self.id_buku = id_buku
        self.jumlah = jumlah

    def __str__(self):
        return (
            f"{self.id_detail} | Peminjaman: {self.id_peminjaman} | "
            f"Buku: {self.id_buku} | Jumlah: {self.jumlah}"
        )
