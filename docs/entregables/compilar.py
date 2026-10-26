import subprocess
import os
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    tex_file = "EquipoX_Proyecto2_Resumen.tex"
    if len(sys.argv) > 1:
        tex_file = sys.argv[1]
    
    # Rutas posibles del ejecutable tectonic
    possible_paths = [
        os.path.abspath(os.path.join(script_dir, "..", "..", "bin", "tectonic.exe")),
        os.path.join(os.path.expanduser("~"), "bin", "tectonic.exe"),
        "tectonic"
    ]
    
    compiler = None
    for p in possible_paths:
        if os.path.exists(p) or p == "tectonic":
            compiler = p
            break
            
    print(f"[*] Compilando {tex_file} con {compiler}...")
    try:
        subprocess.run([compiler, tex_file], check=True)
        pdf_file = tex_file.replace(".tex", ".pdf")
        if os.path.exists(pdf_file):
            print(f"[OK] Documento PDF generado exitosamente: {os.path.abspath(pdf_file)}")
    except Exception as e:
        print(f"[ERROR] Error al compilar: {e}")

if __name__ == "__main__":
    main()
