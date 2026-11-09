class Petugas:
    def __init__(self, nama_petugas, username, id_petugas=None):
        self.id_petugas = id_petugas
        self.nama_petugas = nama_petugas
        self.username = username

    def __str__(self):
        return f"{self.id_petugas} | {self.nama_petugas} | {self.username}"
