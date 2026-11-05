import os
import re

TARGET_DIRS = [
    "00_contexto_e_regras",
    "02_rota_0_estrategia",
    "03_rota_4_financas_operacoes",
    "04_scripts_automacao",
    "05_logs_execucao",
    ".agent"
]

EXTENSIONS = (".md", ".txt", ".py", ".gdoc")

def sanitize_content(text):
    # 1. Substituir links file:///[LOCAL_USER_HOME]/Challenge-TaranisBlack/ por ./
    text = re.sub(r'file:///[LOCAL_USER_HOME]/]+/Documents/Challenge-TaranisBlack/', './', text)
    
    # 2. Substituir caminhos com barras normais [LOCAL_USER_HOME]/Challenge-TaranisBlack/ por ./
    text = re.sub(r'[LOCAL_USER_HOME]/]+/Documents/Challenge-TaranisBlack/', './', text)
    text = re.sub(r'[LOCAL_USER_HOME]/]+/Documents/Challenge-TaranisBlack', '.', text)
    
    # 3. Substituir caminhos Windows com barras invertidas [LOCAL_USER_HOME]\Challenge-TaranisBlack\ por .\
    text = re.sub(r'C:\\Users\\[^\\]+\\Documents\\Challenge-TaranisBlack\\', '.\\\\', text)
    text = re.sub(r'C:\\Users\\[^\\]+\\Documents\\Challenge-TaranisBlack', '.', text)

    # 4. Substituir caminhos gerais [LOCAL_USER_HOME]\ por [HOME_DIR]\ ou ./ se for no workspace
    text = re.sub(r'C:\\Users\\[^\\]+\\\.gemini\\antigravity-cli', './.gemini/antigravity-cli', text)
    text = re.sub(r'C:\\Users\\[^\\]+', '[LOCAL_USER_HOME]', text)
    text = re.sub(r'[LOCAL_USER_HOME]/]+', '[LOCAL_USER_HOME]', text)

    # 5. Normalizar markdown links do tipo (file:///[LOCAL_USER_HOME]///\[LOCAL_USER_HOME\]/Documents/Challenge-TaranisBlack/', './', text)
    
    return text

def main():
    changed_files = []
    total_matches = 0

    print("Iniciando varredura de sanitização de caminhos absolutos...")

    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
        for root, _, files in os.walk(target):
            for fname in files:
                if fname.endswith(EXTENSIONS):
                    filepath = os.path.join(root, fname)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        original = f.read()
                    
                    sanitized = sanitize_content(original)
                    if original != sanitized:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(sanitized)
                        changed_files.append(filepath)
                        diff_count = len(re.findall(r'C:[\\/][Uu]sers', original))
                        total_matches += diff_count
                        print(f"[SANITIZADO] {filepath} ({diff_count} ocorrências limpas)")

    print(f"\nResumo da Sanitização:")
    print(f"- Total de arquivos modificados: {len(changed_files)}")
    print(f"- Total de padrões sensíveis substituídos: {total_matches}")

    # Auditoria de pós-checagem
    print("\nExecutando verificação de conformidade pós-sanitização...")
    remaining = []
    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
        for root, _, files in os.walk(target):
            for fname in files:
                if fname.endswith(EXTENSIONS):
                    filepath = os.path.join(root, fname)
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        c = f.read()
                    m = re.findall(r'C:[\\/][Uu]sers', c)
                    if m:
                        remaining.append((filepath, len(m)))

    if remaining:
        print(f"[ALERTA] Ainda foram encontradas {len(remaining)} referências em:")
        for r, cnt in remaining:
            print(f"  - {r}: {cnt} ocorrências")
    else:
        print("[SUCESSO] 100% dos caminhos absolutos locais foram eliminados e substituídos por notação relativa!")

if __name__ == "__main__":
    main()
