class KRS:
    def __init__(self, id_mahasiswa, id_matkul, semester,
                 tahun_akademik, id_krs=None):
        self.id_krs = id_krs
        self.id_mahasiswa = id_mahasiswa
        self.id_matkul = id_matkul
        self.semester = semester
        self.tahun_akademik = tahun_akademik

    def __str__(self):
        return (f"{self.id_krs} | Mahasiswa: {self.id_mahasiswa} | "
                f"Mata Kuliah: {self.id_matkul} | Semester: {self.semester} "
                f"| Tahun: {self.tahun_akademik}")
