import os
import re

BASE_DIR = os.path.abspath(".")

def get_md_files():
    md_files = []
    for root, _, files in os.walk(BASE_DIR):
        if ".venv" in root or ".git" in root:
            continue
        for f in files:
            if f.endswith(".md"):
                md_files.append(os.path.join(root, f))
    return sorted(md_files)

def audit_links():
    md_files = get_md_files()
    broken = []
    total = 0

    for mdf in md_files:
        dir_of_file = os.path.dirname(mdf)
        with open(mdf, "r", encoding="utf-8", errors="ignore") as fp:
            content = fp.read()
        
        matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, link in matches:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean_link = link.split("#")[0].strip()
            if not clean_link:
                continue
            total += 1
            # Normalizar para verificar no disco
            target_path = os.path.normpath(os.path.join(dir_of_file, clean_link))
            if not os.path.exists(target_path):
                broken.append((mdf, link, clean_link, target_path))
    
    return md_files, total, broken

def fix_links():
    md_files = get_md_files()
    modified_files = []

    for mdf in md_files:
        dir_of_file = os.path.dirname(mdf)
        with open(mdf, "r", encoding="utf-8", errors="ignore") as fp:
            content = fp.read()

        def replacer(match):
            text = match.group(1)
            link = match.group(2)
            
            if link.startswith(("http://", "https://", "mailto:", "#")):
                return match.group(0)
            
            clean_link = link.split("#")[0].strip()
            anchor = ("#" + link.split("#")[1]) if "#" in link else ""
            
            if not clean_link:
                return match.group(0)
            
            target_path = os.path.normpath(os.path.join(dir_of_file, clean_link))
            if os.path.exists(target_path):
                return match.group(0) # Já está correto
            
            # Se não existe a partir de dir_of_file, mas existe a partir da raiz BASE_DIR
            # Por exemplo, clean_link começava com './' achando que a raiz era o ponto de partida
            root_relative = clean_link
            if root_relative.startswith("./"):
                root_relative = root_relative[2:]
            elif root_relative.startswith(".\\"):
                root_relative = root_relative[2:]
            
            candidate_from_root = os.path.normpath(os.path.join(BASE_DIR, root_relative))
            if os.path.exists(candidate_from_root):
                # Calcular o caminho relativo correto de dir_of_file para candidate_from_root
                rel_path = os.path.relpath(candidate_from_root, dir_of_file).replace("\\", "/")
                # Se estiver na mesma pasta e rel_path não começar com '.', podemos adicionar './'
                if not rel_path.startswith("."):
                    rel_path = "./" + rel_path
                return f"[{text}]({rel_path}{anchor})"
            
            return match.group(0)

        new_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replacer, content)

        if new_content != content:
            with open(mdf, "w", encoding="utf-8") as fp:
                fp.write(new_content)
            modified_files.append(mdf)

    return modified_files

def main():
    print("=== AUDITORIA INICIAL DE LINKS MARKDOWN ===")
    md_files, total, broken = audit_links()
    print(f"Total de ficheiros .md avaliados: {len(md_files)}")
    print(f"Total de links internos avaliados: {total}")
    print(f"Total de links quebrados encontrados: {len(broken)}")
    
    for mdf, link, clean, tgt in broken:
        rel_mdf = os.path.relpath(mdf, BASE_DIR).replace("\\", "/")
        print(f"  Em `{rel_mdf}`: link '{link}' não encontrado em '{os.path.relpath(tgt, BASE_DIR).replace('\\', '/')}'")
    
    if broken:
        print("\n=== EXECUTANDO CORREÇÃO AUTOMÁTICA DE CAMINHOS RELATIVOS ===")
        modified = fix_links()
        print(f"Total de ficheiros corrigidos: {len(modified)}")
        for m in modified:
            print(f"  [CORRIGIDO] {os.path.relpath(m, BASE_DIR).replace('\\', '/')}")
        
        print("\n=== AUDITORIA FINAL DE PÓS-CORREÇÃO ===")
        _, total_after, broken_after = audit_links()
        print(f"Total de links internos avaliados: {total_after}")
        print(f"Total de links quebrados restantes: {len(broken_after)}")
        if broken_after:
            for mdf, link, clean, tgt in broken_after:
                rel_mdf = os.path.relpath(mdf, BASE_DIR).replace("\\", "/")
                print(f"  [AINDA QUEBRADO] Em `{rel_mdf}`: '{link}'")
        else:
            print("[SUCESSO ABSOLUTO] ZERO links quebrados no workspace! Todos apontam com precisão para ficheiros existentes.")
    else:
        print("[SUCESSO] Todos os links já estão íntegros.")

if __name__ == "__main__":
    main()
