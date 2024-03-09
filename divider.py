from tkinter import filedialog, messagebox
import csv
import customtkinter
import PyPDF2

class PDFDivider:
    def __init__(self, master):
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.master = master
        master.title("PDF Divider")

        self.label_pdf = customtkinter.CTkLabel(master, text="Seleziona il PDF di input:")
        self.label_pdf.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

        self.pdf_button = customtkinter.CTkButton(master, text="Sfoglia", command=self.select_pdf)
        self.pdf_button.grid(row=0, column=1, padx=(0, 30), pady=(10, 5))

        self.label_csv = customtkinter.CTkLabel(master, text="Seleziona il file CSV di input:")
        self.label_csv.grid(row=1, column=0, padx=(10, 5), pady=5)

        self.csv_button = customtkinter.CTkButton(master, text="Sfoglia", command=self.select_csv)
        self.csv_button.grid(row=1, column=1, padx=(0, 30), pady=5)

        self.label_output = customtkinter.CTkLabel(master, text="Seleziona la cartella di output:")
        self.label_output.grid(row=2, column=0, padx=(10, 5), pady=5)

        self.output_button = customtkinter.CTkButton(master, text="Sfoglia", command=self.select_output)
        self.output_button.grid(row=2, column=1, padx=(0, 30), pady=5)

        self.divide_button = customtkinter.CTkButton(master, text="Dividi PDF", command=self.divide_pdf, state="disabled")
        self.divide_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 20))

        # Modifica la larghezza del frame
        master.grid_columnconfigure(0, minsize=220)

    def select_pdf(self):
        self.pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file:
            messagebox.showinfo("Selezione riuscita", "Il file PDF è stato selezionato correttamente.")
            self.update_divide_button()

    def select_csv(self):
        self.csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.csv_file:
            messagebox.showinfo("Selezione riuscita", "Il file CSV è stato selezionato correttamente.")
            self.update_divide_button()

    def select_output(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            messagebox.showinfo("Selezione riuscita", "La cartella di output è stata selezionata correttamente.")
            self.update_divide_button()

    def update_divide_button(self):
        if hasattr(self, 'pdf_file') and hasattr(self, 'csv_file') and hasattr(self, 'output_dir'):
            self.divide_button.configure(state="normal")
        else:
            self.divide_button.configure(state="disabled")

    def divide_pdf(self):
        if hasattr(self, 'pdf_file') and hasattr(self, 'csv_file') and hasattr(self, 'output_dir'):
            with open(self.csv_file, newline='') as file:
                reader = csv.reader(file)
                lista_nomi = [row[0] for row in reader]

            with open(self.pdf_file, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                current_name = lista_nomi[0]
                pages_to_merge = []

                for i in range(num_pages):
                    if lista_nomi[i] == current_name:
                        pages_to_merge.append(pdf_reader.pages[i])
                    else:
                        self.merge_pdf_pages(current_name, pages_to_merge)
                        current_name = lista_nomi[i]
                        pages_to_merge = [pdf_reader.pages[i]]

                self.merge_pdf_pages(current_name, pages_to_merge)
            messagebox.showinfo("Operazione completata", "Tutto è andato a buon fine.", icon='info')
        else:
            print("Devi selezionare un PDF, un file CSV e una cartella di output.")

    def merge_pdf_pages(self, nome, pages):
        if pages:
            pdf_writer = PyPDF2.PdfWriter()
            for page in pages:
                pdf_writer.add_page(page)
            output_pdf = f"{self.output_dir}/{nome.replace(' ', '_')}.pdf"
            with open(output_pdf, 'wb') as file_out:
                pdf_writer.write(file_out)
        else:
            print("Nessuna pagina da unire per il nome:", nome)

root = customtkinter.CTk()
app = PDFDivider(root)
root.mainloop()
