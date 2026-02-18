import fitz  # PyMuPDF
import os

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
    
    doc.close()
    return names

def split_pdf_by_names(pdf_file, output_dir, progress_callback=None):
    """
    Divide il PDF in più file in base ai nomi trovati.
    """
    doc = fitz.open(pdf_file)
    lista_nomi = extract_names_from_pdf(pdf_file)
    num_pages = len(doc)
    
    current_name = lista_nomi[0]
    pages_indices = []
    
    for i in range(num_pages):
        if lista_nomi[i] == current_name:
            pages_indices.append(i)
        else:
            # Salva il gruppo precedente
            save_pdf_pages(doc, pages_indices, current_name, output_dir)
            
            # Inizia nuovo gruppo
            current_name = lista_nomi[i]
            pages_indices = [i]
        
        # Callback per la progress bar
        if progress_callback:
            progress_callback((i + 1) / num_pages)
    
    # Salva l'ultimo gruppo
    save_pdf_pages(doc, pages_indices, current_name, output_dir)
    doc.close()

def save_pdf_pages(doc, page_indices, nome, output_dir):
    """
    Salva le pagine specificate in un nuovo PDF.
    """
    if page_indices:
        output_pdf = fitz.open()  # Crea nuovo documento
        output_pdf.insert_pdf(doc, from_page=min(page_indices), 
                             to_page=max(page_indices))
        
        filename = f"{output_dir}/{nome.replace(' ', '_')}.pdf"
        output_pdf.save(filename)
        output_pdf.close()
