import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import re
import os
import shutil

INPUT_DOCX = "Challenge AI for Business — Taranis Black (ONE G11) - Rota 4 Finanças - Arley Ribeiro da Silva Xavier.docx"
BACKUP_DOCX = "03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx"

AUTHOR_NAME = "Arley Ribeiro da Silva Xavier"
AUTHOR_ROLE = "Consultor de IA"
AUTHOR_EMAIL = "arleyrsx@gmail.com"
COORTE = "ONE - AI for Business | G11"

# Regex para limpar qualquer emoji ou caractere pictográfico
EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299\ufe0f]"
)

def remove_emojis(text):
    if not text:
        return ""
    cleaned = EMOJI_PATTERN.sub("", text)
    # Limpar espacos duplicados decorrentes da remocao de emojis
    return re.sub(r" +", " ", cleaned).strip()

def set_cell_background(cell, fill_hex):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def style_paragraph(p, font_name="Calibri", font_size=10.5, bold=False, italic=False, color_rgb=(0, 0, 0), space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT):
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    for r in p.runs:
        r.font.name = font_name
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = RGBColor(*color_rgb)

def add_styled_paragraph(cell, text, font_name="Calibri", font_size=10, bold=False, italic=False, color_rgb=(51, 51, 51), space_after=3, align=WD_ALIGN_PARAGRAPH.LEFT):
    text_clean = remove_emojis(text)
    p = cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    r = p.add_run(text_clean)
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor(*color_rgb)
    return p

def set_table_header(row, col_widths=None):
    for idx, cell in enumerate(row.cells):
        set_cell_background(cell, "1F3864") # Azul marinho institucional escuro
        for p in cell.paragraphs:
            p.text = remove_emojis(p.text)
            style_paragraph(p, font_name="Calibri", font_size=9.5, bold=True, color_rgb=(255, 255, 255), space_after=2)
        if col_widths and idx < len(col_widths):
            cell.width = col_widths[idx]

def clean_all_emojis_in_doc(doc):
    for p in doc.paragraphs:
        p.text = remove_emojis(p.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.text = remove_emojis(p.text)

def main():
    print(f"Abrindo documento template: {INPUT_DOCX}...")
    doc = docx.Document(INPUT_DOCX)

    # 1. Limpeza global preventiva de qualquer emoji pré-existente
    clean_all_emojis_in_doc(doc)

    print("Configurando seções e preenchendo tabelas institucionais...")

    # Tabela 0: Header da Rota
    cell_0 = doc.tables[0].cell(0, 0)
    cell_0.text = ""
    set_cell_background(cell_0, "1F3864")
    add_styled_paragraph(cell_0, "ROTA 4 - IA PARA FINANCAS E OPERACOES", font_size=13, bold=True, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.CENTER)

    # Tabela 1: Header de Identificação
    cell_1 = doc.tables[1].cell(0, 0)
    cell_1.text = ""
    set_cell_background(cell_1, "2F5597")
    add_styled_paragraph(cell_1, "IDENTIFICACAO DO ALUNO E DO PROJETO", font_size=11, bold=True, color_rgb=(255, 255, 255))

    # Tabela 2: Campos de Identificação
    t2 = doc.tables[2]
    t2.cell(0, 1).text = ""
    add_styled_paragraph(t2.cell(0, 1), AUTHOR_NAME, font_size=10, bold=True)
    t2.cell(1, 1).text = ""
    add_styled_paragraph(t2.cell(1, 1), AUTHOR_EMAIL, font_size=10)
    t2.cell(2, 1).text = ""
    add_styled_paragraph(t2.cell(2, 1), COORTE, font_size=10, bold=True)

    # Tabela 3: Rota Escolhida
    cell_3 = doc.tables[3].cell(0, 0)
    cell_3.text = ""
    set_cell_background(cell_3, "F2F4F7")
    add_styled_paragraph(cell_3, "Rota de Especializacao Escolhida:", font_size=10, bold=True)
    add_styled_paragraph(cell_3, "[ ]  Rota 1 - IA para Vendas e Comercial", font_size=9.5)
    add_styled_paragraph(cell_3, "[ ]  Rota 2 - IA para Marketing e Conteudo", font_size=9.5)
    add_styled_paragraph(cell_3, "[ ]  Rota 3 - IA para RH e People Analytics", font_size=9.5)
    add_styled_paragraph(cell_3, "[X] Rota 4 - IA para Financas e Operacoes (Selecionada)", font_size=10, bold=True, color_rgb=(31, 56, 100))

    # Tabela 4: Header do Cenário
    cell_4 = doc.tables[4].cell(0, 0)
    cell_4.text = ""
    set_cell_background(cell_4, "2F5597")
    add_styled_paragraph(cell_4, "CENARIO DE NEGOCIOS NA TARANIS BLACK - ROTA 4", font_size=11, bold=True, color_rgb=(255, 255, 255))

    # Tabela 5: Público e Problema
    t5 = doc.tables[5]
    for r in t5.rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.text = remove_emojis(p.text)
                style_paragraph(p, font_size=9.5)

    # Tabela 6: Instrução do Resumo Executivo
    cell_6 = doc.tables[6].cell(0, 0)
    cell_6.text = ""
    set_cell_background(cell_6, "E9EEF4")
    add_styled_paragraph(cell_6, "Instrucao: Escreva este resumo como se fosse uma comunicacao direta para a CEO da Taranis Black (diagnostico geral, iniciativas de IA recomendadas e impacto financeiro esperado em ate 15 linhas).", font_size=9, italic=True, color_rgb=(80, 80, 80))

    # Tabela 7: Preenchimento do Resumo Executivo para a CEO
    t7 = doc.tables[7]
    # Limpar todas as linhas da tabela 7 e utilizar as primeiras celulas com conteudo fluido
    for r in t7.rows:
        for c in r.cells:
            c.text = ""

    c_exec = t7.cell(0, 0)
    set_cell_background(c_exec, "FAFAFA")
    add_styled_paragraph(c_exec, "Prezada Diretora Presidente (CEO) e Conselho de Administracao,", font_size=10, bold=True, space_after=4)
    add_styled_paragraph(c_exec, "A Taranis Black encerrou o exercicio com receita bruta de R$ 48,5 milhoes, confirmando o crescimento comercial continuo de 35% ao ano. Contudo, a ausencia de modernizacao nos processos operacionais gerou um descompasso critico: o EBITDA realizado recuou 41,4% (atingindo R$ 5,77 milhoes frente aos R$ 9,85 milhoes orcados), impactado por perdas operacionais diretas de R$ 3,89 milhoes por ano.", font_size=9.5, space_after=3)
    add_styled_paragraph(c_exec, "O diagnostico detalhado aponta tres gargalos centrais: (1) ciclo de analise de credito B2B retido por 48 horas em caixas de e-mail manuais, gerando R$ 1,25 milhao em cancelamentos comerciais e R$ 1,11 milhao em perdas por inadimplencia (3,4% da receita); (2) digitacao manual de propostas em PDF no ERP legado, provocando 6,8% de divergencias fiscais e um estouro de R$ 1,875 milhao em fretes de emergencia e reentregas no CD Joinville/SC; e (3) conciliacao contabil manual em tres planilhas isoladas, atrasando o fechamento mensal em 5 dias uteis.", font_size=9.5, space_after=3)
    add_styled_paragraph(c_exec, "Para sanar essas dificuldades sem incorrer nos altos custos e riscos de substituicao do ERP legado, recomendamos a implantacao de uma camada periferica de Inteligencia Artificial em tres ondas: Onda 1 (Pre-Validador Fiscal/Logistico de Pedidos em 4 semanas como Quick Win); Onda 2 (Conciliador Contabil Multicanal reduzindo o fechamento para D+2 em 8 semanas); e Onda 3 (Motor Inteligente de Credito B2B com Fast-Track para 65% dos pedidos em 12 semanas).", font_size=9.5, space_after=3)
    add_styled_paragraph(c_exec, "Com um investimento total de R$ 250.000,00 no primeiro ano, a projecao realista recupera R$ 2.501.000,00 anuais de margem liquida direta, alcancando um Retorno sobre o Investimento (ROI) de aproximadamente 900% (9,0x) e Payback em apenas 1,2 meses (36 dias). Recomendamos a aprovacao imediata do plano para sustentar o crescimento lucrativo da companhia.", font_size=9.5, bold=True, color_rgb=(31, 56, 100), space_after=4)

    # Tabela 8 & 9: Header Rota 0
    doc.tables[8].cell(0, 0).text = ""
    set_cell_background(doc.tables[8].cell(0, 0), "1F3864")
    add_styled_paragraph(doc.tables[8].cell(0, 0), "PARTE 1 - BASE ESTRATEGICA OBRIGATORIA (ROTA 0)", font_size=11, bold=True, color_rgb=(255, 255, 255))

    doc.tables[9].cell(0, 0).text = ""
    set_cell_background(doc.tables[9].cell(0, 0), "E9EEF4")
    add_styled_paragraph(doc.tables[9].cell(0, 0), "Orientacao: A Rota 0 e a fundacao do trabalho corporativo. Ela assegura visao executiva e governanca antes do aprofundamento operacional.", font_size=9, italic=True)

    # Tabela 10: Rota 0 - Etapa 1 (AI Canvas & Casos de Uso)
    t10 = doc.tables[10]
    set_cell_background(t10.cell(0, 0), "2F5597")
    set_cell_background(t10.cell(0, 1), "2F5597")
    t10.cell(0, 0).text = ""
    t10.cell(0, 1).text = ""
    add_styled_paragraph(t10.cell(0, 0), "Etapa 1 - AI Canvas & Mapeamento de Oportunidades", font_size=10, bold=True, color_rgb=(255, 255, 255))
    add_styled_paragraph(t10.cell(0, 1), "OBRIGATORIA", font_size=9.5, bold=True, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.RIGHT)

    # Casos de uso (mín. 3)
    c10_1 = t10.cell(1, 1)
    c10_1.text = ""
    add_styled_paragraph(c10_1, "Foram estruturados e priorizados tres casos de uso corporativos no AI Canvas:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c10_1, "1. Motor Inteligente de Triagem e Analise de Credito B2B: Extrai dados de propostas comerciais em PDF, consulta a API da Serasa Experian e aplica matriz parametrica de alçadas. Reduz o SLA de 48h para menos de 15 minutos em 65% dos pedidos, atacando R$ 1,25M em cancelamentos por morosidade e mitigando a inadimplencia de 3,4% (R$ 1,11M em PDD).", font_size=9, space_after=2)
    add_styled_paragraph(c10_1, "2. Assistente de Conciliacao Financeira Multicanal e Fechamento Contabil: Realiza ingestao diaria de extratos OFX/CSV e relatorios de vendas, executando pareamento probabilistico (fuzzy matching). Elimina 5 dias de atraso no fechamento mensal (atingindo a meta D+2) e economiza R$ 180k/ano em horas extras e auditorias contabeis.", font_size=9, space_after=2)
    add_styled_paragraph(c10_1, "3. Pre-Validador Semantico de Pedidos, Dados Fiscais (NF-e) e Roteirizacao de Frete: Realiza conferencia cruzada entre o PDF da proposta, o catalogo oficial e as regras CIF/FOB antes da emissao da NF-e e despacho no CD Joinville. Reduz o indice de divergencias fiscais de 6,8% para menos de 0,3% e estanca R$ 1,35M/ano em fretes extras e cancelamentos.", font_size=9, space_after=2)

    # Classificação por tipo de IA
    c10_2 = t10.cell(2, 1)
    c10_2.text = ""
    add_styled_paragraph(c10_2, "A classificacao tecnologica das iniciativas adota uma arquitetura hibrida complementar:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c10_2, "• IA Generativa (Document AI / LLM Corporativo): Aplicada na leitura, extracao semantica e interpretacao de PDFs despadronizados de propostas comerciais (Caso 1 e Caso 3) e na redacao automatizada da minuta explicativa de divergencias na DRE para a diretoria (Caso 2). Justificativa: flexibilidade no tratamento de documentos nao estruturados.", font_size=9, space_after=2)
    add_styled_paragraph(c10_2, "• IA Preditiva / Estatistica (Scoring & Clustering): Empregada no calculo do escore preditivo de inadimplencia combinando dados historicos do ERP e birôs externos, bem como na identificacao de anomalias de lancamentos contabeis. Justificativa: precisao analitica e mitigacao de risco financeiro.", font_size=9, space_after=2)
    add_styled_paragraph(c10_2, "• Regras Tradicionais / Heuristicas: Matriz deterministica de limites de credito e tabelas oficiais de fretes homologados do CD Joinville, garantindo regras rigidas de conformidade corporativa.", font_size=9, space_after=2)

    # Supervisão humana (Human-in-the-Loop)
    c10_3 = t10.cell(3, 1)
    c10_3.text = ""
    add_styled_paragraph(c10_3, "Diretrizes Mandatorias de Supervisao Humana (Human-in-the-Loop):", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c10_3, "1. Aprovacao de Credito de Maior Porte: Pedidos acima de R$ 80.000,00 ou clientes com score intermediario/restricoes exigem aprovacao formal em 1 clique pelo Gerente Financeiro, que recebe o dossie analitico estruturado gerado pela IA. Decisoes 100% autonomas de recusa ou concessao de alto valor sao vedadas.", font_size=9, space_after=2)
    add_styled_paragraph(c10_3, "2. Excecoes Fiscais e Divergencias: Havendo inconsistencia entre a proposta e a SEFAZ ou conflito de frete CIF/FOB, o sistema retem o pedido em quarentena com alerta visual para ajuste pelo analista humano.", font_size=9, space_after=2)
    add_styled_paragraph(c10_3, "3. Conformidade Legal: O desenho atende expressamente ao Artigo 20 da LGPD (Lei 13.709/2018), assegurando o direito de revisao humana para decisoes baseadas em tratamento automatizado de dados.", font_size=9, space_after=2)

    # Tabela 11: Rota 0 - Etapa 2 (Priorização & Mudança)
    t11 = doc.tables[11]
    set_cell_background(t11.cell(0, 0), "2F5597")
    set_cell_background(t11.cell(0, 1), "2F5597")
    t11.cell(0, 0).text = ""
    t11.cell(0, 1).text = ""
    add_styled_paragraph(t11.cell(0, 0), "Etapa 2 - Priorizacao Baseada em Dados & Gestao de Mudanca", font_size=10, bold=True, color_rgb=(255, 255, 255))
    add_styled_paragraph(t11.cell(0, 1), "OBRIGATORIA", font_size=9.5, bold=True, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.RIGHT)

    # Matriz Esforço x Impacto
    c11_1 = t11.cell(1, 1)
    c11_1.text = ""
    add_styled_paragraph(c11_1, "Estruturacao da Matriz de Priorizacao 2x2 e Sequencia de Rollout em Ondas:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c11_1, "• Onda 1 (Semanas 1 a 4) - Ganhos Rapidos (Quick Win): Caso 3 (Pre-Validador Fiscal & Logistico). Baixo esforco de integracao (nao altera o codigo do ERP legado, atuando como middleware em Python) e alto impacto financeiro imediato (ataca R$ 1,35M/ano de perdas em fretes e cancelamentos).", font_size=9, space_after=2)
    add_styled_paragraph(c11_1, "• Onda 2 (Semanas 5 a 8) - Controladoria e Visibilidade: Caso 2 (Conciliador Contabil Multicanal). Medio esforco analitico (ingestao de OFX/CSV e matching probabilistico) e alto retorno executivo, encurtando o fechamento para D+2 e economizando R$ 180k/ano.", font_size=9, space_after=2)
    add_styled_paragraph(c11_1, "• Onda 3 (Semanas 9 a 12) - Aposta Estrategica (Major Project): Caso 1 (Motor Inteligente de Credito B2B). Maior esforco de integracao com birô externo (Serasa) e altissimo impacto de receita (destrava vendas B2B e recupera R$ 1,43M/ano).", font_size=9, space_after=2)
    add_styled_paragraph(c11_1, "• Armadilha Evitada (Time Sink): Vetada expressamente a substituicao do ERP legado, o que custaria mais de R$ 2 milhoes e paralisaria as operacoes por 12 a 18 meses.", font_size=9, space_after=2)

    # Métricas de sucesso
    c11_2 = t11.cell(2, 1)
    c11_2.text = ""
    add_styled_paragraph(c11_2, "Painel de Metricas Executivas e OKRs Consolidados (Horizonte de 6 Meses):", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c11_2, "• Retorno Financeiro Consolidado: Recuperacao projetada de R$ 2.501.000,00/ano em margem operacional liquida com investimento de R$ 250k no primeiro ano (ROI de 9x e Payback em 1,2 meses).", font_size=9, space_after=2)
    add_styled_paragraph(c11_2, "• SLA de Faturamento e Credito: Reducao do Lead Time total do pedido de 5 dias uteis (40h uteis) para menos de 2 horas (com 65% em Fast-Track < 15 min).", font_size=9, space_after=2)
    add_styled_paragraph(c11_2, "• Fechamento Contabil Mensal: Reducao de 7 dias uteis para 2 dias uteis (meta D+2 cumprida).", font_size=9, space_after=2)
    add_styled_paragraph(c11_2, "• Conformidade Fiscal: Reducao no indice de divergencias de notas fiscais de 6,8% para menos de 0,5% das emissoes.", font_size=9, space_after=2)
    add_styled_paragraph(c11_2, "• Custos com Fretes Extras e Reentregas: Reducao de 2,8% para menos de 1,0% da receita bruta.", font_size=9, space_after=2)

    # Plano de mudança ADKAR
    c11_3 = t11.cell(3, 1)
    c11_3.text = ""
    add_styled_paragraph(c11_3, "Plano de Gestao de Mudancas Organizacionais (Framework ADKAR para 280 Colaboradores):", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c11_3, "• Awareness (Conscientizacao): Reuniao geral de alinhamento com a CEO demonstrando abertamente o impacto dos R$ 3,89M de perdas e reforçando que a IA visa eliminar o trabalho manual repetitivo, nao reduzir postos de trabalho.", font_size=9, space_after=2)
    add_styled_paragraph(c11_3, "• Desire (Engajamento): Compromisso executivo de requalificacao profissional (reskilling) dos assistentes e eliminacao de sobrejornadas desgastantes de fechamento ate tarde da noite.", font_size=9, space_after=2)
    add_styled_paragraph(c11_3, "• Knowledge (Capacitacao): Trilha pratica de engenharia de prompts financeiros, interpretacao de relatorios e operacao dos validadores com turmas de ate 15 profissionais.", font_size=9, space_after=2)
    add_styled_paragraph(c11_3, "• Ability (Sustentacao): Criacao da Rede de 5 Campeoes de IA locais em Financas e no CD Joinville, com suporte em tempo real e ambiente seguro de testes (Sandbox).", font_size=9, space_after=2)
    add_styled_paragraph(c11_3, "• Reinforcement (Reforco): Reconhecimento trimestral de colaboradores inovadores e atrelamento da reducao do fechamento para D+2 as metas de participacao nos lucros (PLR).", font_size=9, space_after=2)

    # Tabela 12: Rota 0 - Etapa 3 (Governança & LGPD)
    t12 = doc.tables[12]
    set_cell_background(t12.cell(0, 0), "2F5597")
    set_cell_background(t12.cell(0, 1), "2F5597")
    t12.cell(0, 0).text = ""
    t12.cell(0, 1).text = ""
    add_styled_paragraph(t12.cell(0, 0), "Etapa 3 - Politica de Governanca, Etica e Conformidade", font_size=10, bold=True, color_rgb=(255, 255, 255))
    add_styled_paragraph(t12.cell(0, 1), "OBRIGATORIA", font_size=9.5, bold=True, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.RIGHT)

    # Política de IA Responsável
    c12_1 = t12.cell(1, 1)
    c12_1.text = ""
    add_styled_paragraph(c12_1, "Politica Corporativa de IA Responsavel e Classificacao em 4 Niveis:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c12_1, "• Nivel 1 (Dados Publicos): Fichas tecnicas de produtos, catalogo e normas NR-17 -> Liberado em qualquer ferramenta.", font_size=9, space_after=2)
    add_styled_paragraph(c12_1, "• Nivel 2 (Dados Internos): Manuais de processos e procedimentos gerais -> Liberado com cautela e sem identificacao institucional.", font_size=9, space_after=2)
    add_styled_paragraph(c12_1, "• Nivel 3 (Dados Confidenciais): DRE, margens brutas, tabelas de fretes e estrategias B2B -> Proibido em ferramentas gratuitas; permitido unicamente em instancias corporativas pagas com clausula de Zero Data Retention.", font_size=9, space_after=2)
    add_styled_paragraph(c12_1, "• Nivel 4 (Dados Restritos / LGPD): Salarios, dados pessoais de colaboradores, feedbacks de saida e CPFs -> Proibido em formato bruto em qualquer IA externa; requer aplicacao do Protocolo P4S de anonimizacao prévia.", font_size=9, space_after=2)
    add_styled_paragraph(c12_1, "• Protocolo P4S de 4 Passos: 1. Identificar dados pessoais (PII); 2. Substituir por identificadores genericos ([Colaborador_A], [Cliente_X]); 3. Normalizar grandezas monetarias em indices base 100; 4. Revisao visual antes do disparo do prompt.", font_size=9, space_after=2)

    # Riscos e LGPD
    c12_2 = t12.cell(2, 1)
    c12_2.text = ""
    add_styled_paragraph(c12_2, "Mapeamento de Riscos e Diretrizes de Conformidade LGPD:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c12_2, "• Risco de Vazamento de Segredos Comerciais: Proibicao expressa de insercao de dados contabeis reais em chats abertos (ex: ChatGPT gratuito), cujos termos de uso utilizam prompts para treinamento público de modelos.", font_size=9, space_after=2)
    add_styled_paragraph(c12_2, "• Risco de Alucinacao em Dados Fiscais e Contabeis: Vedada a aceitacao cega de calculos matematicos emitidos por modelos de linguagem. Operacoes contabeis devem ser auditadas deterministicamente em planilhas ou scripts Python.", font_size=9, space_after=2)
    add_styled_paragraph(c12_2, "• Principio da Responsabilidade do Autor: A IA e co-piloto; o profissional que valida e submete relatorios ou informacoes fiscais e o unico responsavel legal e administrativo pela precisao do conteudo.", font_size=9, space_after=2)

    # Comitê e auditoria
    c12_3 = t12.cell(3, 1)
    c12_3.text = ""
    add_styled_paragraph(c12_3, "Estrutura do Comite de Governanca de IA e Sanções:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c12_3, "• Composicao Multidisciplinar: Encarregado de Protecao de Dados (DPO/Juridico), Gestor de TI & CISO, Gerente Financeiro/Controladoria e Coordenador de Operacoes do CD Joinville.", font_size=9, space_after=2)
    add_styled_paragraph(c12_3, "• Canal Formal de Homologacao: Nenhuma ferramenta ou extensao de IA pode ser utilizada sem parecer favoravel prévio via ia.governanca@taranisblack.com.br.", font_size=9, space_after=2)
    add_styled_paragraph(c12_3, "• Regime Disciplinar: Descumprimentos sujeitam o infrator a advertencia, suspensao e demissao por justa causa (Art. 482 da CLT, alineas a, g e h), alem de responsabilizacao civil por perdas e danos.", font_size=9, space_after=2)

    # Tabela 13: Header Parte 2 - Rota 4
    doc.tables[13].cell(0, 0).text = ""
    set_cell_background(doc.tables[13].cell(0, 0), "1F3864")
    add_styled_paragraph(doc.tables[13].cell(0, 0), "PARTE 2 - ESPECIALIZACAO: IA PARA FINANCAS E OPERACOES", font_size=11, bold=True, color_rgb=(255, 255, 255))

    # Tabela 14: Rota 4 - Etapa 1 (SIPOC & Ishikawa)
    t14 = doc.tables[14]
    set_cell_background(t14.cell(0, 0), "2F5597")
    set_cell_background(t14.cell(0, 1), "2F5597")
    t14.cell(0, 0).text = ""
    t14.cell(0, 1).text = ""
    add_styled_paragraph(t14.cell(0, 0), "Etapa 1 - Mapeamento Lean & Diagnostico de Gargalos (SIPOC & Ishikawa)", font_size=10, bold=True, color_rgb=(255, 255, 255))
    add_styled_paragraph(t14.cell(0, 1), "OBRIGATORIA", font_size=9.5, bold=True, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.RIGHT)

    # Matriz SIPOC
    c14_1 = t14.cell(1, 1)
    c14_1.text = ""
    add_styled_paragraph(c14_1, "Matriz Lean SIPOC do Macroprocesso de Faturamento e Expedicao B2B:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c14_1, "• Suppliers (Fornecedores): Consultores Comerciais B2B, Clientes Compradores, Birô Serasa Experian, Gerencia Financeira, SEFAZ e Transportadoras Homologadas.", font_size=9, space_after=1)
    add_styled_paragraph(c14_1, "• Inputs (Entradas): Propostas em PDF assinadas, cadastros de CNPJ/IE, historico de compras no ERP legado, tabela de precos e matriz de fretes CIF/FOB.", font_size=9, space_after=1)
    add_styled_paragraph(c14_1, "• Process (Etapas As-Is): 1. Envio despadronizado de e-mail ao financeiro (>40/dia em pico); 2. Triagem manual e consulta a 3 telas (40 min/pedido); 3. Solicitacao de alçada por e-mail; 4. Retencao em fila por 24h a 48h uteis; 5. Digitacao manual de NF-e e envio manual ao CD Joinville.", font_size=9, space_after=1)
    add_styled_paragraph(c14_1, "• Outputs (Saidas): Ordens de venda gravadas no ERP, dossies de credito compilados, autorizacoes de faturamento, DANFE/XML de NF-e, boletos bancarios e Minutas de Embarque (CT-e).", font_size=9, space_after=1)
    add_styled_paragraph(c14_1, "• Customers (Clientes): Comprador B2B corporativo, Equipe do CD Joinville, Transportadoras, Faturamento e Controladoria.", font_size=9, space_after=1)
    add_styled_paragraph(c14_1, "• Eficiencia de Fluxo (PCE): Touch Time ativo de apenas 1,5 horas frente ao Lead Time de 40 horas uteis (5 dias uteis). Eficiencia de Ciclo (PCE) de 3,75%, revelando que 96,25% do tempo e desperdicio em filas.", font_size=9, bold=True, color_rgb=(31, 56, 100), space_after=2)

    # Diagrama de Ishikawa
    c14_2 = t14.cell(2, 1)
    c14_2.text = ""
    add_styled_paragraph(c14_2, "Diagrama de Ishikawa nos 6M (Causas dos Atrasos e das Perdas de R$ 3,89M):", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c14_2, "• Metodo: Fluxo de aprovacao dependente de comunicacao informal por e-mail; inexistencia de esteira de alcada automatica; dependencia de 3 planilhas locais desconectadas (Controle_Limites, Precos e Fretes); regras CIF/FOB nao checadas antes da venda.", font_size=9, space_after=1)
    add_styled_paragraph(c14_2, "• Maquina / Tecnologia: ERP legado sem APIs modernas de integracao; ausencia de Document AI / OCR para leitura automatica de PDFs; falta de validacao sintatica e fiscal pre-emissao de NF-e.", font_size=9, space_after=1)
    add_styled_paragraph(c14_2, "• Mao de Obra: Assistentes sobrecarregados com digitacao mecanica e sujeitos a burnout nos fechamentos; centralizacao de aprovacoes rotineiras na gerencia financeira; atritos de comunicacao entre o time comercial (SP) e o CD (Joinville/SC).", font_size=9, space_after=1)
    add_styled_paragraph(c14_2, "• Material: Propostas comerciais enviadas com campos incompletos; divergencia de codigos SKU entre tabelas de vendas e o ERP; comprovantes de endereco desatualizados.", font_size=9, space_after=1)
    add_styled_paragraph(c14_2, "• Medicao: Falta de monitoramento de SLAs por etapa em tempo real; ausencia de conciliacao bancaria continua; diretoria informada sobre atrasos somente no encerramento contabil.", font_size=9, space_after=1)
    add_styled_paragraph(c14_2, "• Meio Ambiente: Crescimento acelerado de 35% ao ano superando a maturidade operacional dos sistemas; concentracao de mais de 45% do faturamento nos ultimos dias do mes comercial.", font_size=9, space_after=2)

    # Top 3 causas críticas
    c14_3 = t14.cell(3, 1)
    c14_3.text = ""
    add_styled_paragraph(c14_3, "Top 3 Causas Criticas Estruturais (Metodologia dos 5 Porques):", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c14_3, "1. Falta de Conciliacao Contabil Continua por Fuzzy Matching: Causa o atraso cronico de 5 dias no fechamento mensal e gera R$ 180k/ano em horas extras, pois analistas conferem manualmente milhares de lancamentos contra extratos e relatorios de vendas.", font_size=9, space_after=2)
    add_styled_paragraph(c14_3, "2. Ausencia de Motor Parametrico de Credito B2B com Fast-Track: Provoca a retencao de 48h na caixa de e-mail do gerente, resultando em R$ 1,25M/ano em compras canceladas por morosidade e R$ 1,11M em perdas por inadimplencia devido a analises apressadas sob pressao.", font_size=9, space_after=2)
    add_styled_paragraph(c14_3, "3. Digitacao Manual de Propostas para Emissao de NF-e sem Validacao Previa: Causa 6,8% de divergencias fiscais e um estouro de R$ 1,875M em fretes duplicados, multas e custos logisticos no CD Joinville/SC decorrentes de erros em acabamentos de produto e regras CIF/FOB.", font_size=9, space_after=2)

    # Recomendação de intervenção prioritária
    c14_4 = t14.cell(4, 1)
    c14_4.text = ""
    add_styled_paragraph(c14_4, "Recomendacao de Intervencao Prioritaria:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c14_4, "A intervencao prioritaria imediata e a implantacao do Pre-Validador Fiscal & Logistico (Caso 3) na Onda 1 (4 semanas).", font_size=9, bold=True, color_rgb=(31, 56, 100), space_after=2)
    add_styled_paragraph(c14_4, "Justificativa Tecnica e Financeira: Esta solucao atua como um middleware leve em Python que intercepta as propostas em PDF e valida codigos SKU, condicoes de pagamento e regras de frete CIF/FOB antes que o pedido chegue a SEFAZ ou ao CD Joinville. Nao exige alteracoes estruturais no ERP legado, tem baixo custo (R$ 50k) e estanca de imediato R$ 1,35 milhao por ano em fretes de emergencia e cancelamentos fiscais, trazendo retorno visivel ja no primeiro mes de operacao.", font_size=9, space_after=2)

    # Tabela 15: Rota 4 - Etapa 3 (Dashboard & Análise Preditiva - Opcional)
    t15 = doc.tables[15]
    set_cell_background(t15.cell(0, 0), "2F5597")
    set_cell_background(t15.cell(0, 1), "2F5597")
    t15.cell(0, 0).text = ""
    t15.cell(0, 1).text = ""
    add_styled_paragraph(t15.cell(0, 0), "Etapa 3 - Dashboard Inteligente & Analise Preditiva Financeira", font_size=10, bold=True, color_rgb=(255, 255, 255))
    add_styled_paragraph(t15.cell(0, 1), "OPCIONAL (CONCLUIDA)", font_size=9.5, bold=True, color_rgb=(255, 255, 255), align=WD_ALIGN_PARAGRAPH.RIGHT)

    # Prompts de processamento
    c15_1 = t15.cell(1, 1)
    c15_1.text = ""
    add_styled_paragraph(c15_1, "Prompts Especializados de Engenharia Financeira Utilizados:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c15_1, "Prompt 1 (Auditoria DRE e Desvios de Margem): 'Atue como Controller. Analise a planilha 05_Financas_Orcado_vs_Realizado.xlsx. Calcule a variancia nominal em R$ e percentual de cada conta da DRE Trimestral. Destaque quais linhas de custo excederam o orcado anual em mais de 15% e correlacione com os desvios de EBITDA. Apresente memoria de calculo.'", font_size=8.5, italic=True, space_after=2)
    add_styled_paragraph(c15_1, "Prompt 2 (Diagnostico de Fretes e Quebra de EBITDA): 'Cruze os dados da aba Gargalos_Operacionais_Custos com a DRE. Calcule o impacto financeiro consolidado de fretes duplicados, multas por divergencia de NF-e e perdas com PDD sobre a receita liquida. Indique a porcentagem da perda de EBITDA atribuivel unicamente a falhas de faturamento e logistica.'", font_size=8.5, italic=True, space_after=2)
    add_styled_paragraph(c15_1, "Prompt 3 (Modelagem Preditiva Pós-IA): 'Projete o resultado operacional dos proximos 4 trimestres considerando a reducao de 65% nos cancelamentos, queda de 70% nas despesas com fretes extras e reducao da inadimplencia para 1,5%. Calcule o novo EBITDA projetado e o Payback para um investimento de R$ 250k.'", font_size=8.5, italic=True, space_after=2)

    # Dashboard / relatório gerado
    c15_2 = t15.cell(2, 1)
    c15_2.text = ""
    add_styled_paragraph(c15_2, "Sintese do Demonstrativo de Resultados do Exercicio (DRE) Auditado:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c15_2, "• Receita Bruta Total: R$ 48.500.000,00 (Orcado: R$ 48.600.000,00 | Variacao: -0,2%)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• Canal Corporativo B2B (70%): R$ 33.600.000,00 (Orcado: R$ 34.000.000,00 | Retencao por credito)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• Canal Vendas Diretas pelo Site (30%): R$ 14.900.000,00 (Orcado: R$ 14.600.000,00 | +2,1%)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• Cancelamentos/Devolucoes: R$ 1.235.000,00 (Orcado: R$ 560.000,00 | Aumento critico de +120,5%)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• Receita Liquida Operacional: R$ 39.020.000,00 (Orcado: R$ 39.778.000,00 | Desvio: -1,9%)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• Lucro Bruto Operacional: R$ 18.430.000,00 (Margem Bruta realizada de 47,2% vs 49,5% orcada)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• Despesas Operacionais (OPEX): R$ 12.660.000,00 (Orcado: R$ 9.850.000,00 | Estouro de +28,5%)", font_size=9, space_after=1)
    add_styled_paragraph(c15_2, "• EBITDA Operacional Realizado: R$ 5.770.000,00 (Orcado: R$ 9.848.000,00 | Perda de -41,4% / -R$ 4,08M)", font_size=9, bold=True, color_rgb=(150, 0, 0), space_after=1)
    add_styled_paragraph(c15_2, "• Lucro Liquido Realizado: R$ 3.108.600,00 (Orcado: R$ 5.965.080,00 | Reducao de -47,9%)", font_size=9, bold=True, color_rgb=(150, 0, 0), space_after=2)

    # Anomalias identificadas
    c15_3 = t15.cell(3, 1)
    c15_3.text = ""
    add_styled_paragraph(c15_3, "Anomalias Financeiras Criticas Diagnosticadas na Operacao:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c15_3, "1. Explosao de Despesas com Fretes e Reentregas: O total somado de fretes do CD Joinville e multas por divergencia atingiu R$ 4.465.000,00 (9,2% da receita bruta), representando um estouro de R$ 1.875.000,00 acima do planejado (responsavel por 46% de toda a quebra de EBITDA da empresa).", font_size=9, space_after=2)
    add_styled_paragraph(c15_3, "2. Aumento Agressivo da PDD / Inadimplencia B2B: Saltou de R$ 440.000,00 para R$ 1.110.000,00 (+152%), elevando o indice de inadimplencia para 3,4% da receita decorrente da falta de motor de credito.", font_size=9, space_after=2)
    add_styled_paragraph(c15_3, "3. Descompasso de Margem na Linha SmartDesk: Menor margem bruta entre os moveis corporativos (38,5%) e queda de R$ 550 mil no faturamento anual em razao da retencao de propostas de alto valor na esteira de credito.", font_size=9, space_after=2)

    # Projeção para o próximo trimestre / 12 meses
    c15_4 = t15.cell(4, 1)
    c15_4.text = ""
    add_styled_paragraph(c15_4, "Projecao Preditiva de Recuperacao Financeira Pós-Implementacao das 3 Ondas de IA:", font_size=9.5, bold=True, space_after=2)
    add_styled_paragraph(c15_4, "• Projecao de EBITDA: Elevacao de R$ 5.770.000,00 para R$ 8.271.000,00 ao ano (+43,3%), recuperando mais de R$ 2,50 milhoes em margem operacional e recompondo a margem EBITDA para 21,2%.", font_size=9, space_after=2)
    add_styled_paragraph(c15_4, "• Projecao de Lucro Liquido: Salto de R$ 3.108.600,00 para R$ 4.759.000,00 (+53,1%), restabelecendo a rentabilidade da companhia.", font_size=9, space_after=2)
    add_styled_paragraph(c15_4, "• Retorno do Investimento: O aporte de R$ 250 mil e amortizado integralmente em 1,2 meses (36 dias de faturamento com perdas estancadas), com ROI de 9 vezes o valor investido.", font_size=9, space_after=2)

    # Tabela 16: Anexo de Evidências
    doc.tables[16].cell(0, 0).text = ""
    set_cell_background(doc.tables[16].cell(0, 0), "1F3864")
    add_styled_paragraph(doc.tables[16].cell(0, 0), "ANEXO DE EVIDENCIAS E ARTEFATOS CONSTRUIDOS", font_size=11, bold=True, color_rgb=(255, 255, 255))

    doc.tables[17].cell(0, 0).text = ""
    set_cell_background(doc.tables[17].cell(0, 0), "E9EEF4")
    add_styled_paragraph(doc.tables[17].cell(0, 0), "Orientacao: Lista de evidencias e artefatos tecnicos desenvolvidos e homologados para avaliacao.", font_size=9, italic=True)

    # Tabela 18: Tabela de Evidências (5x5)
    t18 = doc.tables[18]
    set_table_header(t18.rows[0], col_widths=[Inches(1.5), Inches(2.0), Inches(1.8), Inches(1.2), Inches(1.5)])

    evidencias_data = [
        ("AI Canvas Corporativo & Casos de Uso", "Mapeamento dos 9 blocos estrategicos e detalhamento dos 3 casos de uso da Taranis Black.", "./02_rota_0_estrategia/01_ai_canvas_taranis_black.md", "Homologado", "Base estrategica do projeto e dimensionamento de ROI"),
        ("Matriz Esforço x Impacto & ADKAR", "Priorizacao em ondas, definicao de OKRs de 6 meses e plano de mudancas para 280 colaboradores.", "./02_rota_0_estrategia/02_matriz_esforco_impacto_metricas_mudancas.md", "Homologado", "Roteiro de implantacao tatica e governanca cultural"),
        ("Politica Corporativa de IA & LGPD", "Diretrizes de uso responsavel, 4 niveis de sensibilidade de dados e protocolo P4S de sanitizacao.", "./02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md", "Homologado", "Regulamentacao corporativa de seguranca da informacao"),
        ("Mapeamento SIPOC, Ishikawa & DRE", "Matriz Lean As-Is/To-Be, causas 6M, 5 Porques, 5W2H e analise financeira DRE Orcado vs Realizado.", "./03_rota_4_financas_operacoes/", "Homologado", "Dossie completo de especializacao da Rota 4")
    ]

    for idx, (art, desc, link, print_cap, nota) in enumerate(evidencias_data, start=1):
        row = t18.rows[idx]
        for c_idx, val in enumerate([art, desc, link, print_cap, nota]):
            c = row.cells[c_idx]
            c.text = ""
            is_bold = (c_idx == 0 or c_idx == 3)
            col_color = (31, 56, 100) if c_idx == 0 else (51, 51, 51)
            add_styled_paragraph(c, val, font_size=8.5, bold=is_bold, color_rgb=col_color)

    # Tabela 19, 20, 21: Vídeo de Demonstração
    doc.tables[19].cell(0, 0).text = ""
    set_cell_background(doc.tables[19].cell(0, 0), "1F3864")
    add_styled_paragraph(doc.tables[19].cell(0, 0), "VIDEO DE DEMONSTRACAO (OPCIONAL)", font_size=11, bold=True, color_rgb=(255, 255, 255))

    doc.tables[20].cell(0, 0).text = ""
    set_cell_background(doc.tables[20].cell(0, 0), "E9EEF4")
    add_styled_paragraph(doc.tables[20].cell(0, 0), "Formatos aceitos: YouTube (nao listado), Loom ou Google Drive. Duracao: ate 5 minutos.", font_size=9, italic=True)

    c21 = doc.tables[21].cell(0, 1)
    c21.text = ""
    add_styled_paragraph(c21, "Projeto integralmente documentado com evidencias textuais, metricas DRE auditadas e demonstrativos tecnicos em anexo.", font_size=9, italic=True)

    # Tabela 22, 23: Como Entregar
    doc.tables[22].cell(0, 0).text = ""
    set_cell_background(doc.tables[22].cell(0, 0), "1F3864")
    add_styled_paragraph(doc.tables[22].cell(0, 0), "PROCEDIMENTO DE SUBMISSAO OFICIAL", font_size=11, bold=True, color_rgb=(255, 255, 255))

    # Limpar emojis nas linhas de instruções da tabela 23
    for r in doc.tables[23].rows:
        for c in r.cells:
            for p in c.paragraphs:
                p.text = remove_emojis(p.text)
                style_paragraph(p, font_size=9)

    # 4. Limpeza final de conferência contra qualquer caractere pictográfico remanescente
    clean_all_emojis_in_doc(doc)

    print(f"Salvando documento principal em: {INPUT_DOCX}...")
    doc.save(INPUT_DOCX)

    print(f"Salvando copia de seguranca em: {BACKUP_DOCX}...")
    shutil.copyfile(INPUT_DOCX, BACKUP_DOCX)

    # 5. Auditoria de pós-checagem de emojis e integridade
    doc_check = docx.Document(INPUT_DOCX)
    emoji_count = 0
    total_paras = len(doc_check.paragraphs)
    total_tables = len(doc_check.tables)

    for p in doc_check.paragraphs:
        if EMOJI_PATTERN.search(p.text):
            emoji_count += 1
    for t in doc_check.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    if EMOJI_PATTERN.search(p.text):
                        emoji_count += 1

    print("\n=== AUDITORIA DE FINALIZACAO DO DOCUMENTO ===")
    print(f"- Total de paragrafos no documento: {total_paras}")
    print(f"- Total de tabelas preenchidas: {total_tables}")
    print(f"- Contagem de emojis encontrados: {emoji_count}")
    if emoji_count == 0:
        print("[SUCESSO ABSOLUTO] ZERO EMOJIS! O documento atende rigorosamente a restricao de estilo formal corporativo.")
    else:
        print(f"[ALERTA] Foram detectados {emoji_count} emojis residuais.")

if __name__ == "__main__":
    main()
