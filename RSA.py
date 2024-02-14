import tkinter as tk

def encrypt(text, public_key):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in text]
    return cipher

def decrypt(cipher, private_key):
    d, n = private_key
    text = ''.join([chr(pow(char, d, n)) for char in cipher])
    return text

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def generate_keypair(p, q, e):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return ((e, n), (d, n))

class RSAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Kriptografi RSA")
        self.geometry("500x500")  

        # Title label
        title_label = tk.Label(self, text="Mengamankan Pesan Dengan Algoritma RSA", font=("Helvetica", 12, "bold"))
        title_label.pack(pady=10)

        # Text untuk menampilkan petunjuk dan hasil
        self.result_text = tk.Text(self, height=8, width=55)
        self.result_text.pack(pady=10)
        self.show_instructions()

        # Menyimpan referensi ke frame yang digunakan untuk menampilkan label dan teks box
        self.frame = tk.Frame(self)
        self.frame.pack()

        # Button Enkripsi
        encrypt_button = tk.Button(self, text="Enkripsi", command=self.show_encryption_widgets, bg="yellow", fg="red")
        encrypt_button.pack(side=tk.LEFT, padx=10)

        # Button Dekripsi
        decrypt_button = tk.Button(self, text="Dekripsi", command=self.show_decryption_widgets, bg="yellow", fg="red")
        decrypt_button.pack(side=tk.LEFT, padx=10)

        # Button Kunci
        keygen_button = tk.Button(self, text="Kunci", command=self.show_keygen_widgets, bg="yellow", fg="red")
        keygen_button.pack(side=tk.LEFT, padx=10)

        # Button Tentang
        about_button = tk.Button(self, text="Tentang", command=self.show_about, bg="yellow", fg="red")
        about_button.pack(side=tk.LEFT, padx=10)

        # Button Keluar
        exit_button = tk.Button(self, text="Keluar", command=self.destroy, bg="yellow", fg="red")
        exit_button.pack(side=tk.LEFT, padx=10)

    def show_instructions(self):
        instructions = "Tekan Tombol Untuk Menjalankan Fungsi yang Diinginkan!"
        self.result_text.insert(tk.END, instructions)

    def show_encryption_widgets(self):
        self.clear_result_text()
        self.clear_current_widgets()

        # Frame untuk label dan teks box
        frame = tk.Frame(self.frame)
        frame.pack()

        # Label Kunci Publik
        public_key_label = tk.Label(frame, text="Masukkan Kunci Publik (e, n):")
        public_key_label.pack()

        # Entry untuk Kunci Publik
        public_key_entry = tk.Entry(frame)
        public_key_entry.pack(pady=5)

        # Label Plaintext
        plaintext_label = tk.Label(frame, text="Masukkan Plaintext:")
        plaintext_label.pack()

        # Entry untuk Plaintext
        plaintext_entry = tk.Entry(frame)
        plaintext_entry.pack(pady=5)

        # Button untuk Enkripsi
        encrypt_button = tk.Button(frame, text="Enkripsi", command=lambda: self.perform_encryption(public_key_entry.get(), plaintext_entry.get()), bg="yellow", fg="red")
        encrypt_button.pack(pady=10)

    def show_decryption_widgets(self):
        self.clear_result_text()
        self.clear_current_widgets()

        # Frame untuk label dan teks box
        frame = tk.Frame(self.frame)
        frame.pack()

        # Label Kunci Privat
        private_key_label = tk.Label(frame, text="Masukkan Kunci Privat (d, n):")
        private_key_label.pack()

        # Entry untuk Kunci Privat
        private_key_entry = tk.Entry(frame)
        private_key_entry.pack(pady=5)

        # Label Ciphertext
        ciphertext_label = tk.Label(frame, text="Masukkan Ciphertext:")
        ciphertext_label.pack()

        # Entry untuk Ciphertext
        ciphertext_entry = tk.Entry(frame)
        ciphertext_entry.pack(pady=5)

        # Button untuk Dekripsi
        decrypt_button = tk.Button(frame, text="Dekripsi", command=lambda: self.perform_decryption(private_key_entry.get(), ciphertext_entry.get()), bg="yellow", fg="red")
        decrypt_button.pack(pady=10)

    def show_keygen_widgets(self):
        self.clear_result_text()
        self.clear_current_widgets()

        # Frame untuk label dan teks box
        frame = tk.Frame(self.frame)
        frame.pack()

        # Label Nilai e
        e_label = tk.Label(frame, text="Masukkan Nilai e:(Disarankan menggunakan 65537)")
        e_label.pack()

        # Entry untuk Nilai e
        e_entry = tk.Entry(frame)
        e_entry.pack(pady=5)

        # Label Nilai p
        p_label = tk.Label(frame, text="Masukkan Nilai p(Bilangan Prima):")
        p_label.pack()

        # Entry untuk Nilai p
        p_entry = tk.Entry(frame)
        p_entry.pack(pady=5)

        # Label Nilai q
        q_label = tk.Label(frame, text="Masukkan Nilai q(Bilangan Prima):")
        q_label.pack()

        # Entry untuk Nilai q
        q_entry = tk.Entry(frame)
        q_entry.pack(pady=5)

        # Button untuk Generasi Kunci
        keygen_button = tk.Button(frame, text="Generasi Kunci", command=lambda: self.perform_key_generation(p_entry.get(), q_entry.get(), e_entry.get()), bg="yellow", fg="red")
        keygen_button.pack(pady=10)

    def show_about(self):
        about_text = "Aplikasi Kriptografi RSA\n\n"
        about_text += "1. Klik 'Enkripsi' untuk melakukan enkripsi teks dengan kunci publik.\n"
        about_text += "2. Klik 'Dekripsi' untuk melakukan dekripsi teks dengan kunci privat.\n"
        about_text += "3. Klik 'Kunci' untuk menghasilkan kunci publik dan privat jika belum memilikinya.\n"
        about_text += "4. Klik 'Tentang' untuk informasi lebih lanjut tentang aplikasi."

        self.clear_result_text()
        self.insert_result_text(about_text)

    def perform_encryption(self, public_key_str, plaintext):
        try:
            e, n = map(int, public_key_str.split(','))
            public_key = (e, n)
        except ValueError:
            self.clear_result_text()
            self.insert_result_text("Format kunci publik tidak valid. Masukkan dua bilangan bulat yang dipisahkan dengan koma.")
            return

        encrypted_text = encrypt(plaintext, public_key)
        self.clear_result_text()
        self.insert_result_text("Teks terenkripsi: {}".format(' '.join(map(str, encrypted_text))))

    def perform_decryption(self, private_key_str, ciphertext_str):
        try:
            d, n = map(int, private_key_str.split(','))
            private_key = (d, n)
        except ValueError:
            self.clear_result_text()
            self.insert_result_text("Format kunci pribadi tidak valid. Masukkan dua bilangan bulat yang dipisahkan dengan koma.")
            return

        try:
            ciphertext = list(map(int, ciphertext_str.split()))
        except ValueError:
            self.clear_result_text()
            self.insert_result_text("Format teks terenkripsi tidak valid. Masukkan bilangan bulat yang dipisahkan dengan spasi.")
            return

        decrypted_text = decrypt(ciphertext, private_key)
        self.clear_result_text()
        self.insert_result_text("Teks terdekripsi: {}".format(decrypted_text))

    def perform_key_generation(self, p_str, q_str, e_str):
        try:
            p = int(p_str)
            q = int(q_str)
            e = int(e_str)
        except ValueError:
            self.clear_result_text()
            self.insert_result_text("Masukkan nilai bilangan bulat yang valid untuk p, q, dan e.")
            return

        public_key, private_key = generate_keypair(p, q, e)
        self.clear_result_text()
        self.insert_result_text("Kunci Publik: {}\nKunci Privat: {}".format(public_key, private_key))

    def clear_result_text(self):
        self.result_text.delete(1.0, tk.END)

    def insert_result_text(self, text):
        self.result_text.insert(tk.END, text + "\n")

    def clear_current_widgets(self):
        # Menghapus frame yang berisi label dan entry yang sedang ditampilkan
        for widget in self.frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = RSAApp()
    app.mainloop()
