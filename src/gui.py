import customtkinter
from tkinter import filedialog, messagebox
from pdf_utils import split_pdf_by_names
import threading
import os
import sys
import updater

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        # Risale di una cartella: da src/ → root del progetto
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


class PDFDivider:
    def __init__(self, master):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        self.master = master
        self.master.iconbitmap(resource_path("assets/pdf_icon.ico"))
        self.master.title("PDF-divider")
        self.center_window(430, 250)

        self.frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.frame.pack(expand=True, padx=20, pady=20)

        self.label_pdf = customtkinter.CTkLabel(self.frame, text="PDF di input:")
        self.label_pdf.grid(row=0, column=0, padx=12, pady=8, sticky="e")

        self.pdf_button = customtkinter.CTkButton(self.frame, text="📂 Sfoglia", command=self.select_pdf, width=120)
        self.pdf_button.grid(row=0, column=1, padx=7, pady=8, sticky="w")

        self.pdf_status = customtkinter.CTkLabel(self.frame, text="⬜")
        self.pdf_status.grid(row=0, column=2, padx=8)

        self.label_output = customtkinter.CTkLabel(self.frame, text="Cartella di output:")
        self.label_output.grid(row=1, column=0, padx=12, pady=8, sticky="e")

        self.output_button = customtkinter.CTkButton(self.frame, text="📂 Sfoglia", command=self.select_output, width=120)
        self.output_button.grid(row=1, column=1, padx=7, pady=8, sticky="w")

        self.output_status = customtkinter.CTkLabel(self.frame, text="⬜")
        self.output_status.grid(row=1, column=2, padx=8)

        self.divide_button = customtkinter.CTkButton(self.frame, text="✂️ Dividi PDF", command=self.divide_pdf,
                                                     state="disabled", width=180, height=32)
        self.divide_button.grid(row=2, column=0, columnspan=3, pady=(15, 10))

        self.progressbar = customtkinter.CTkProgressBar(self.frame, height=10)
        self.progressbar.grid(row=3, column=0, columnspan=3, padx=10, pady=(8, 0), sticky="ew")
        self.progressbar.set(0)

        self.credit_label = customtkinter.CTkLabel(self.frame, text="© 2025 Giorgio Tuccinardi")
        self.credit_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)

        # Check aggiornamenti all'avvio (dopo 1.5 secondi)
        self.master.after(1500, self._check_for_updates)

    def _check_for_updates(self):
        thread = threading.Thread(
            target=updater.check_and_update,
            args=(self.master,), daemon=True
        )
        thread.start()

    def center_window(self, width=440, height=300):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2) - 150)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def select_pdf(self):
        self.pdf_file = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            title="Seleziona il PDF da dividere"
        )
        if self.pdf_file:
            try:
                if os.path.getsize(self.pdf_file) == 0:
                    messagebox.showerror("Errore", "Il file PDF è vuoto.")
                    return
                self.pdf_status.configure(text="✅", text_color="green")
                self.update_divide_button()
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile leggere il file:\n{str(e)}")

    def select_output(self):
        self.output_dir = filedialog.askdirectory(title="Seleziona la cartella di output")
        if self.output_dir:
            if not os.access(self.output_dir, os.W_OK):
                messagebox.showerror("Errore", "La cartella selezionata non è scrivibile.")
                return
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
            self.divide_button.configure(state="disabled", text="⏳ Elaborazione...")
            thread = threading.Thread(target=self._process_pdf, daemon=True)
            thread.start()

    def _process_pdf(self):
        try:
            split_pdf_by_names(
                self.pdf_file, self.output_dir,
                progress_callback=self.update_progress
            )
            self.master.after(0, self._on_completion_success)
        except Exception as e:
            self.master.after(0, lambda: self._on_completion_error(str(e)))

    def _on_completion_success(self):
        self.progressbar.set(1)
        messagebox.showinfo("Operazione completata", "Tutto è andato a buon fine.", icon='info')
        self.reset()
        self.divide_button.configure(text="✂️ Dividi PDF")

    def _on_completion_error(self, error_msg):
        messagebox.showerror("Errore", f"Si è verificato un errore:\n{error_msg}")
        self.reset()
        self.divide_button.configure(state="normal", text="✂️ Dividi PDF")

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
