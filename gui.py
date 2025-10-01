import customtkinter
from tkinter import filedialog, messagebox
from pdf_utils import split_pdf_by_names

class PDFDivider:
    def __init__(self, master):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.master = master
        self.master.iconbitmap("assets/pdf_icon.ico")
        self.master.title("PDF-divider")

        # Frame principale
        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.pack(expand=True, padx=20, pady=20)

        # Riga 1 - PDF input
        self.label_pdf = customtkinter.CTkLabel(
            self.frame, text="PDF di input:", text_color="white"
        )
        self.label_pdf.grid(row=0, column=0, padx=10, pady=8, sticky="e")

        self.pdf_button = customtkinter.CTkButton(
            self.frame, text="📂 Sfoglia", command=self.select_pdf, width=120
        )
        self.pdf_button.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        self.pdf_status = customtkinter.CTkLabel(
            self.frame, text="⬜", text_color="white"
        )
        self.pdf_status.grid(row=0, column=2, padx=5)

        # Riga 2 - Output folder
        self.label_output = customtkinter.CTkLabel(
            self.frame, text="Cartella di output:", text_color="white"
        )
        self.label_output.grid(row=1, column=0, padx=10, pady=8, sticky="e")

        self.output_button = customtkinter.CTkButton(
            self.frame, text="📂 Sfoglia", command=self.select_output, width=120
        )
        self.output_button.grid(row=1, column=1, padx=5, pady=8, sticky="w")

        self.output_status = customtkinter.CTkLabel(
            self.frame, text="⬜", text_color="white"
        )
        self.output_status.grid(row=1, column=2, padx=5)

        # Riga 3 - Bottone divide
        self.divide_button = customtkinter.CTkButton(
            self.frame, text="✂️ Dividi PDF", command=self.divide_pdf,
            state="disabled", width=180, height=32
        )
        self.divide_button.grid(row=2, column=0, columnspan=3, pady=(15, 10))

        # Riga 4 - Progress bar
        self.progressbar = customtkinter.CTkProgressBar(self.frame, height=10)
        self.progressbar.grid(row=3, column=0, columnspan=3,
                              padx=20, pady=(5, 0), sticky="ew")
        self.progressbar.set(0)

        # Configura la griglia
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)

        self.center_window(420, 200)

    def center_window(self, width=500, height=250):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2) - 150)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def select_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file:
            self.pdf_status.configure(text="✅", text_color="green")
            self.update_divide_button()

    def select_output(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_status.configure(text="✅", text_color="green")
            self.update_divide_button()

    def update_divide_button(self):
        if hasattr(self, 'pdf_file') and hasattr(self, 'output_dir'):
            self.divide_button.configure(state="normal")
        else:
            self.divide_button.configure(state="disabled")

    def update_progress(self, value):
        self.progressbar.set(value)
        self.master.update_idletasks()

    def divide_pdf(self):
        if hasattr(self, 'pdf_file') and hasattr(self, 'output_dir'):
            split_pdf_by_names(
                self.pdf_file, self.output_dir, progress_callback=self.update_progress
            )
            self.progressbar.set(1)
            messagebox.showinfo("Operazione completata", "Tutto è andato a buon fine.", icon='info')
            self.reset()

    def reset(self):
        self.pdf_status.configure(text="⬜", text_color="white")
        self.output_status.configure(text="⬜", text_color="white")
        self.divide_button.configure(state="disabled")
        self.progressbar.set(0)
        if hasattr(self, 'pdf_file'):
            delattr(self, 'pdf_file')
        if hasattr(self, 'output_dir'):
            delattr(self, 'output_dir')


if __name__ == "__main__":
    root = customtkinter.CTk()
    app = PDFDivider(root)
    root.mainloop()
