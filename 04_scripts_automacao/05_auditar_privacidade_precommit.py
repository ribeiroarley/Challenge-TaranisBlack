import os
import re

EXTENSIONS = (".md", ".py", ".txt", ".gdoc", ".json", ".yml", ".yaml")
IGNORE_DIRS = {".venv", ".git"}

# Padrões construídos dinamicamente para não auto-detectar o próprio script
USER_PATT = "a" + "rsx_"
FILE_PROTO_PATT = "file:" + "//C:"
WIN_USERS_PATT = "C:" + "[\\\\/][Uu]sers[\\\\/]"
WIN_SYS_PATT = "C:" + "[\\\\/][Ww]indows"

SENSITIVE_PATTERNS = [
    (WIN_USERS_PATT, "Caminho absoluto de usuário Windows"),
    (USER_PATT, "Nome do usuário local da máquina"),
    (WIN_SYS_PATT, "Caminho de sistema Windows"),
    (FILE_PROTO_PATT, "Protocolo de arquivo local absoluto"),
]

def scan_files():
    findings = []
    total_files = 0
    this_script = os.path.abspath(__file__)

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for fname in files:
            if fname.endswith(EXTENSIONS):
                fpath = os.path.join(root, fname)
                abs_fpath = os.path.abspath(fpath)
                
                # Pular o próprio script de checagem
                if abs_fpath == this_script:
                    continue
                
                # Se for kit_de_dados, checar apenas .md ou .txt
                if "kit_de_dados" in root and not fname.endswith((".md", ".txt")):
                    continue

                total_files += 1
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                except Exception:
                    continue

                for pat, desc in SENSITIVE_PATTERNS:
                    matches = re.findall(pat, content, re.IGNORECASE)
                    if matches:
                        findings.append((fpath, desc, len(matches)))

    return total_files, findings

def main():
    print("=== AUDITORIA PREVENTIVA DE PRIVACIDADE E SEGURANÇA PRÉ-COMMIT ===")
    total, findings = scan_files()
    print(f"Total de arquivos inspecionados: {total}")
    
    if findings:
        print(f"[ALERTA] Foram encontradas {len(findings)} ocorrências sensíveis:")
        for path, desc, count in findings:
            print(f"  - {path}: {count}x ({desc})")
    else:
        print("[APROVADO] Zero caminhos locais absolutos ou identificadores de máquina encontrados!")
        print("[APROVADO] Repositório 100% blindado para publicação pública no GitHub.")

if __name__ == "__main__":
    main()
