class MataKuliah:
    def __init__(self, kode_matkul, nama_matkul, sks, id_matkul=None):
        self.id_matkul = id_matkul
        self.kode_matkul = kode_matkul
        self.nama_matkul = nama_matkul
        self.sks = sks

    def __str__(self):
        return f"{self.id_matkul} | {self.kode_matkul} | {self.nama_matkul}"
