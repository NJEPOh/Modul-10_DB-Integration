class ProgramStudi:
    def __init__(self, nama_prodi, jenjang, id_prodi=None):
        self.id_prodi = id_prodi
        self.nama_prodi = nama_prodi
        self.jenjang = jenjang

    def __str__(self):
        return f"{self.id_prodi} | {self.nama_prodi} | {self.jenjang}"
