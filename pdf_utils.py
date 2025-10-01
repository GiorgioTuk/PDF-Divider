import PyPDF2
import fitz  # PyMuPDF


def extract_names_from_pdf(pdf_file):
    """
    Estrae i nomi dal PDF usando un'area predefinita.
    """
    doc = fitz.open(pdf_file)
    rect = fitz.Rect(290, 102, 442, 119)
    names = []
    for page in doc:
        text = page.get_text("text", clip=rect).strip()
        names.append(text if text else "Sconosciuto")
    return names


def merge_pdf_pages(nome, pages, output_dir):
    """
    Unisce le pagine per un dato nome e salva un PDF.
    """
    if pages:
        pdf_writer = PyPDF2.PdfWriter()
        for page in pages:
            pdf_writer.add_page(page)
        output_pdf = f"{output_dir}/{nome.replace(' ', '_')}.pdf"
        with open(output_pdf, "wb") as f:
            pdf_writer.write(f)


def split_pdf_by_names(pdf_file, output_dir, progress_callback=None):
    """
    Divide il PDF in più file in base ai nomi trovati.
    """
    lista_nomi = extract_names_from_pdf(pdf_file)
    with open(pdf_file, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)

        current_name = lista_nomi[0]
        pages_to_merge = []

        for i in range(num_pages):
            if lista_nomi[i] == current_name:
                pages_to_merge.append(pdf_reader.pages[i])
            else:
                merge_pdf_pages(current_name, pages_to_merge, output_dir)
                current_name = lista_nomi[i]
                pages_to_merge = [pdf_reader.pages[i]]

            # callback per aggiornare la progress bar
            if progress_callback:
                progress_callback((i + 1) / num_pages)

        # ultimo gruppo
        merge_pdf_pages(current_name, pages_to_merge, output_dir)