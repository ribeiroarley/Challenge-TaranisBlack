import os
import re

TARGET_DIRS = [
    "00_contexto_e_regras",
    "02_rota_0_estrategia",
    "03_rota_4_financas_operacoes",
    ".agent"
]

# Dicionário de substituições ordenadas por especificidade (das mais longas para as mais curtas)
REPLACEMENTS = [
    # 1. Cargos e identidades infladas
    (r"Engenheiro de Software Sênior & Consultor em IA Corporativa", "Consultor de IA"),
    (r"Engenheiro de Software Sênior e Consultor em IA Corporativa", "Consultor de IA"),
    (r"Consultor Sênior em IA Corporativa, Lean Seis Sigma e Controladoria", "Consultor de IA"),
    (r"Consultor Sênior de Estratégia e Governança em IA Corporativa", "Consultor de IA"),
    (r"Consultor Sênior em Governança de IA, Segurança da Informação e Compliance \(DPO/LGPD\)", "Consultor de IA e Governança"),
    (r"Consultor Sênior de Estratégia em IA Corporativa", "Consultor de IA"),
    (r"Consultoria Sênior em Estratégia de IA Corporativa & Engenharia de Software", "Consultoria de IA"),
    (r"Consultor Sênior em IA Corporativa", "Consultor de IA"),
    (r"Consultor Sênior de Estratégia", "Consultor de IA"),
    (r"Consultor Sênior", "Consultor de IA"),
    (r"Engenheiro de Software Sênior", "Consultor de IA"),
    (r"Engenheiro Sênior", "Consultor de IA"),
    (r"Arquiteto de Processos Lean e Engenheiro de Software Sênior", "Especialista em Processos e Tecnologia"),
    (r"Arquiteto de Sistemas de IA", "Especialista em Sistemas de IA"),
    (r"Arquiteto Corporativo", "Consultor de IA"),
    (r"Senior Enterprise Consultant", "Consultor de IA"),
    (r"Taranis Black Senior Enterprise Consultant", "Consultoria de IA para Taranis Black"),

    # 2. Jargões e expressões exageradas
    (r"[Rr]adiografia [Cc]orporativa", "Diagnóstico inicial da empresa"),
    (r"[Ss]angria de [Mm]argem", "Perda de margem"),
    (r"[Ss]angria de margem", "perda de margem"),
    (r"[Ss]angria de EBITDA", "redução de EBITDA"),
    (r"[Ss]angria de caixa", "perda de caixa"),
    (r"[Ss]angria invisível", "perda invisível"),
    (r"[Ss]angria", "perda"),
    (r"[Ee]stancar a sangria", "reduzir as perdas"),
    (r"[Ee]stancar o retrabalho", "reduzir o retrabalho"),
    (r"[Ee]stancar", "conter"),

    # 3. Metáforas clínicas e bélicas
    (r"[Aa]natomia das ineficiências crônicas", "Análise detalhada das dificuldades operacionais"),
    (r"[Aa]natomia das Ineficiências Crônicas", "Análise Detalhada das Dificuldades Operacionais"),
    (r"[Aa]natomia dos gargalos", "Análise dos gargalos"),
    (r"[Aa]bordagem cirúrgica", "análise detalhada"),
    (r"[Pp]recisão cirúrgica", "precisão analítica"),
    (r"[Bb]lindagem regulatória", "conformidade com a LGPD"),
    (r"[Bb]lindagem institucional", "segurança institucional"),
    (r"[Bb]lindagem da esteira operacional", "padronização da esteira operacional"),
    (r"[Bb]lindagem de segredo", "proteção de dados confidenciais"),
    (r"[Bb]lindadas contra erros", "protegidas contra erros"),
    (r"[Bb]lindar o EBITDA", "proteger o EBITDA"),
    (r"[Bb]lindar", "proteger"),

    # 4. Termos excessivos de tempo/frequência
    (r"[Ii]neficácia crônica", "dificuldade operacional recorrente"),
    (r"[Aa]traso crônico", "atraso recorrente"),
    (r"[Gg]argalos crônicos", "gargalos operacionais"),
    (r"[Gg]argalo crônico", "gargalo operacional"),
    (r"[Hh]ipercrescimento", "crescimento rápido"),
    (r"[Hh]iperacelerado", "acelerado"),
    (r"estouro estrondoso", "aumento significativo"),

    # 5. Termos burocráticos / jurídicos pesados
    (r"Zero [Dd]ata [Ll]oss", "Preservação de dados"),
    (r"zero data loss", "preservação de dados"),
    (r"compulsório", "necessário"),
    (r"compulsória", "necessária"),
    (r"compulsórias", "necessárias"),
    (r"compulsoriamente", "obrigatoriamente"),
    (r"aplicação compulsória", "aplicação obrigatória"),

    # 6. Adequação de canais (B2B vs vendas diretas pelo site)
    (r"Receita Canal D2C / E-commerce \(30%\)", "Receita Vendas Diretas pelo Site (Canal Complementar - 30%)"),
    (r"Canal D2C / E-commerce \(30%\)", "Vendas Diretas pelo Site (Canal Complementar - 30%)"),
    (r"adquirentes do canal D2C/E-commerce", "meios de pagamento de vendas diretas pelo site")
]

def review_text(content):
    modified = content
    changes_count = 0
    for pattern, replacement in REPLACEMENTS:
        matches = len(re.findall(pattern, modified))
        if matches > 0:
            changes_count += matches
            modified = re.sub(pattern, replacement, modified)
    return modified, changes_count

def main():
    print("Iniciando revisão de tom de voz e linguagem no repositório...")
    
    total_files_changed = 0
    total_substitutions = 0
    file_summary = []

    for target in TARGET_DIRS:
        if not os.path.exists(target):
            continue
        for root, _, files in os.walk(target):
            for fname in sorted(files):
                if fname.endswith((".md", ".txt")):
                    fpath = os.path.join(root, fname)
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as fp:
                        original = fp.read()
                    
                    reviewed, count = review_text(original)
                    if count > 0:
                        with open(fpath, "w", encoding="utf-8") as fp:
                            fp.write(reviewed)
                        total_files_changed += 1
                        total_substitutions += count
                        rel_path = os.path.relpath(fpath, ".").replace("\\", "/")
                        file_summary.append((rel_path, count))
                        print(f"[REVISADO] {rel_path} ({count} alterações)")

    print(f"\nResumo da Execução:")
    print(f"- Total de arquivos aprimorados: {total_files_changed}")
    print(f"- Total de termos/expressões calibradas: {total_substitutions}")

if __name__ == "__main__":
    main()
