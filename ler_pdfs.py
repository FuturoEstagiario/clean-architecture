import os
import sys

def read_pdf(file_path, out_file):
    out_file.write(f"\n{'='*20} LENDO: {os.path.basename(file_path)} {'='*20}\n")
    print(f"Lendo: {os.path.basename(file_path)}")
    if not os.path.exists(file_path):
        out_file.write(f"Erro: O arquivo '{file_path}' não foi encontrado.\n")
        return

    try:
        import pypdf
    except ImportError:
        print("A biblioteca 'pypdf' não está instalada. Instalando agora via pip...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
        import pypdf

    try:
        reader = pypdf.PdfReader(file_path)
        total_pages = len(reader.pages)
        out_file.write(f"Total de páginas: {total_pages}\n\n")
        
        for i, page in enumerate(reader.pages):
            out_file.write(f"--- Página {i+1} ---\n")
            text = page.extract_text()
            if text.strip():
                out_file.write(text)
            else:
                out_file.write("[Página sem texto extraível ou digitalizada como imagem]")
            out_file.write("\n\n")
        print(f"Concluído: {os.path.basename(file_path)} - {total_pages} páginas salvas.")
    except Exception as e:
        out_file.write(f"Ocorreu um erro ao ler o PDF: {e}\n")

if __name__ == "__main__":
    # Encontra todos os arquivos PDF no diretório atual
    pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]
    print(f"Arquivos PDF encontrados para leitura: {pdf_files}")
    
    with open("pdf_contents.txt", "w", encoding="utf-8") as out_file:
        for pdf in pdf_files:
            read_pdf(pdf, out_file)
    print("Todo o conteúdo foi salvo em 'pdf_contents.txt'.")
