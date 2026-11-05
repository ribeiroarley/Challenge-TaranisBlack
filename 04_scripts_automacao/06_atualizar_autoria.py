import os
import re

AUTHOR_NAME = "Arley Ribeiro da Silva Xavier"
AUTHOR_ROLE = "Consultor de IA"
AUTHOR_STR = f"**Autor:** {AUTHOR_NAME} | {AUTHOR_ROLE}"

FILES_TO_UPDATE = [
    # Raiz
    "README.md",
    # 00_contexto_e_regras
    "00_contexto_e_regras/CONTEXTO_PROJETO.md",
    "00_contexto_e_regras/MEMORIA_EXECUCAO.md",
    "00_contexto_e_regras/REGRAS_GOVERNANCA.md",
    # 02_rota_0_estrategia
    "02_rota_0_estrategia/01_ai_canvas_taranis_black.md",
    "02_rota_0_estrategia/02_matriz_esforco_impacto_metricas_mudancas.md",
    "02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md",
    "02_rota_0_estrategia/prompts/01_prompt_ai_canvas.md",
    "02_rota_0_estrategia/prompts/02_prompt_matriz_esforco_impacto.md",
    "02_rota_0_estrategia/prompts/03_prompt_politica_ia_responsavel.md",
    # 03_rota_4_financas_operacoes
    "03_rota_4_financas_operacoes/01_mapeamento_processo_sipoc.md",
    "03_rota_4_financas_operacoes/02_diagrama_ishikawa_6m_causas_raiz.md",
    "03_rota_4_financas_operacoes/03_diagnostico_orcado_vs_realizado.md",
    "03_rota_4_financas_operacoes/prompts/01_prompt_sipoc_mapeamento.md",
    "03_rota_4_financas_operacoes/prompts/02_prompt_ishikawa_causa_raiz.md",
    "03_rota_4_financas_operacoes/prompts/03_prompt_diagnostico_orcado_realizado.md",
    # 05_logs_execucao
    "05_logs_execucao/log_auditoria_reorganizacao.md",
    # .agent
    ".agent/skills/taranis-consultant/SKILL.md"
]

def update_file(filepath):
    if not os.path.exists(filepath):
        return False, 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = 0

    # 1. Substituir linhas explícitas de Autor
    # Ex: **Autor:** Consultor de IA -> **Autor:** Arley Ribeiro da Silva Xavier | Consultor de IA
    sub_patterns = [
        (r"\*\*Autor:\*\* Consultoria de IA", AUTHOR_STR),
        (r"\*\*Autor:\*\* Consultor de IA", AUTHOR_STR),
        (r"\*\*Autor:\*\* Pessoa Consultora de IA", AUTHOR_STR),
        (r"\*\*Engenheiro Responsável:\*\* Senior Software Engineer & AI Enterprise Consultant", f"**Responsável Técnico / Autor:** {AUTHOR_NAME} ({AUTHOR_ROLE})"),
        (r"\*\*De:\*\* Consultor de IA", f"**De:** {AUTHOR_NAME} ({AUTHOR_ROLE})"),
    ]

    for pat, rep in sub_patterns:
        matches = len(re.findall(pat, content))
        if matches > 0:
            content = re.sub(pat, rep, content)
            changes += matches

    # 2. Em arquivos de prompt: garantir que haja metadados de Autor se não houver
    if "/prompts/" in filepath or "\\prompts\\" in filepath:
        if "**Autor:**" not in content:
            # Inserir antes de - **Rota:**
            target = "- **Rota:**"
            replacement = f"- **Autor:** {AUTHOR_NAME}\n- **Papel / Cargo:** {AUTHOR_ROLE}\n- **Rota:**"
            if target in content:
                content = content.replace(target, replacement, 1)
                changes += 1

    # 3. Em arquivos de contexto/regras: garantir linha de autor se não houver
    if filepath in ["00_contexto_e_regras/CONTEXTO_PROJETO.md", "00_contexto_e_regras/REGRAS_GOVERNANCA.md", "02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md"]:
        if "**Autor:**" not in content:
            target = "**Data de"
            replacement = f"{AUTHOR_STR}  \n**Data de"
            if target in content:
                content = content.replace(target, replacement, 1)
                changes += 1

    # 4. No README.md principal
    if filepath == "README.md":
        if "**Autor:**" not in content:
            target = "## 1. Visão Geral e Contexto da Empresa"
            replacement = f"**Autor:** {AUTHOR_NAME} ({AUTHOR_ROLE})  \n**Projeto:** Challenge AI for Business — Taranis Black (ONE G11)  \n\n---\n\n## 1. Visão Geral e Contexto da Empresa"
            if target in content:
                content = content.replace(target, replacement, 1)
                changes += 1

    # 5. Em SKILL.md
    if filepath.endswith("SKILL.md"):
        if "**Autor / Titular:**" not in content:
            target = "* **Papel:**"
            replacement = f"* **Autor / Titular:** {AUTHOR_NAME}  \n* **Papel:**"
            if target in content:
                content = content.replace(target, replacement, 1)
                changes += 1

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True, changes

    return False, 0

def main():
    print("Iniciando consolidação formal de autoria nos arquivos do projeto...")
    updated = []
    total_changes = 0

    for fpath in FILES_TO_UPDATE:
        success, count = update_file(fpath)
        if success:
            updated.append((fpath, count))
            total_changes += count
            print(f"[ATUALIZADO] {fpath} ({count} alterações)")
        else:
            print(f"[SEM ALTERAÇÃO / JÁ ATUALIZADO] {fpath}")

    print(f"\nResumo da Consolidação de Autoria:")
    print(f"- Total de arquivos modificados: {len(updated)}")
    print(f"- Total de alterações de metadados: {total_changes}")
    print(f"- Titular formal homologado: {AUTHOR_NAME} ({AUTHOR_ROLE})")

if __name__ == "__main__":
    main()
