class Mahasiswa:
    def __init__(self, nim, nama, email, id_prodi, id_mahasiswa=None):
        self.id_mahasiswa = id_mahasiswa
        self.nim = nim
        self.nama = nama
        self.email = email
        self.id_prodi = id_prodi

    def __str__(self):
        return f"{self.id_mahasiswa} | {self.nim} | {self.nama}"
