class Anggota:
    def __init__(self, nomor_anggota, nama, alamat, nomor_telepon, id_anggota=None):
        self.id_anggota = id_anggota
        self.nomor_anggota = nomor_anggota
        self.nama = nama
        self.alamat = alamat
        self.nomor_telepon = nomor_telepon

    def __str__(self):
        return (
            f"{self.id_anggota} | {self.nomor_anggota} | "
            f"{self.nama} | {self.alamat} | {self.nomor_telepon}"
        )
