"""
Script Definitivo de Geracao e Diagramacao Executiva do Relatorio Oficial
Projeto: Challenge AI for Business — Taranis Black (ONE G11)
Autor: Arley Ribeiro da Silva Xavier | Consultor de IA
Arquivo Alvo: Challenge AI for Business — Taranis Black (ONE G11) - Rota 4 Finanças - Arley Ribeiro da Silva Xavier.docx
Espelho de Seguranca: 03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import re
import os
import shutil

# Caminhos dos arquivos de saida
OUTPUT_DOCX = "Challenge AI for Business — Taranis Black (ONE G11) - Rota 4 Finanças - Arley Ribeiro da Silva Xavier.docx"
BACKUP_DOCX = "03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx"

# Identificacao do Autor e do Programa
AUTHOR_NAME = "Arley Ribeiro da Silva Xavier"
AUTHOR_ROLE = "Consultor de IA"
AUTHOR_EMAIL = "arleyrsx@gmail.com"
COORTE = "ONE - AI for Business | G11"

# Paleta de Cores Corporativa
HEX_PRIMARY = "1A365D"       # Azul-marinho corporativo escuro
RGB_PRIMARY = (26, 54, 93)

HEX_SECONDARY = "2B6CB0"     # Azul ardósia médio institucional
RGB_SECONDARY = (43, 108, 176)

HEX_WHITE = "FFFFFF"         # Branco puro
RGB_WHITE = (255, 255, 255)

HEX_TEXT_DARK = "2D3748"     # Cinza-escuro quase preto (alta legibilidade)
RGB_TEXT_DARK = (45, 55, 72)

HEX_TEXT_MUTED = "4A5568"    # Cinza médio para legendas e notas
RGB_TEXT_MUTED = (74, 85, 104)

HEX_BG_LABEL = "F0F4F8"      # Cinza-ardósia claro para rótulos/labels
HEX_BG_ZEBRA = "F7FAFC"      # Cinza-gelo suave para linhas alternadas
HEX_BG_CALLOUT = "EDF2F7"    # Cinza suave institucional para caixas de destaque
HEX_BORDER = "CBD5E0"        # Borda neutra sutil (0.5 pt)

HEX_ALERT_RED = "9B2C2C"     # Vermelho corporativo sóbrio para perdas operacionais
RGB_ALERT_RED = (155, 44, 44)

HEX_SUCCESS_GREEN = "276749" # Verde corporativo escuro para homologado / ganhos
RGB_SUCCESS_GREEN = (39, 103, 73)

# Regex estrita para banimento total de emojis
EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299\ufe0f]"
)

def clean_text(text):
    if not text:
        return ""
    cleaned = EMOJI_PATTERN.sub("", text)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    return cleaned.strip()

def clear_element_children(parent, tag_name):
    for child in list(parent):
        if child.tag.endswith(tag_name):
            parent.remove(child)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    clear_element_children(tcPr, "shd")
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Margens internas em dxa (120 dxa = 6pt, 160 dxa = 8pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    clear_element_children(tcPr, "tcMar")
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    clear_element_children(tcPr, "tcBorders")
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}/>')
    
    borders = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for edge, spec in borders.items():
        if spec is None:
            edge_el = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="none"/>')
        else:
            val = spec.get('val', 'single')
            sz = spec.get('sz', '4')
            color = spec.get('color', HEX_BORDER)
            edge_el = parse_xml(
                f'<w:{edge} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            )
        tcBorders.append(edge_el)
    tcPr.append(tcBorders)

def format_table_structure(table, col_widths=None):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    
    clear_element_children(tblPr, "jc")
    tblPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
    
    clear_element_children(tblPr, "tblW")
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>'))
    
    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if not any(child.tag.endswith('cantSplit') for child in list(trPr)):
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_idx == 0 and len(table.rows) > 1:
            if not any(child.tag.endswith('tblHeader') for child in list(trPr)):
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        if col_widths:
            for c_idx, cell in enumerate(row.cells):
                if c_idx < len(col_widths):
                    cell.width = col_widths[c_idx]

def add_run(paragraph, text, font_name="Calibri", font_size=9.5, bold=False, italic=False, color_rgb=RGB_TEXT_DARK):
    cleaned = clean_text(text)
    r = paragraph.add_run(cleaned)
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor(*color_rgb)
    
    rPr = r._r.get_or_add_rPr()
    clear_element_children(rPr, "rFonts")
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.insert(0, rFonts)
    return r

def add_styled_paragraph(doc, text="", font_name="Calibri", font_size=10, bold=False, italic=False, color_rgb=RGB_TEXT_DARK, space_before=0, space_after=3, line_spacing=1.15, align=WD_ALIGN_PARAGRAPH.LEFT, bold_prefix=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    
    if bold_prefix:
        add_run(p, bold_prefix, font_name=font_name, font_size=font_size, bold=True, italic=italic, color_rgb=color_rgb)
    if text:
        add_run(p, text, font_name=font_name, font_size=font_size, bold=bold, italic=italic, color_rgb=color_rgb)
    return p

def add_heading_1(doc, text):
    return add_styled_paragraph(doc, text, font_name="Calibri", font_size=13.5, bold=True, color_rgb=RGB_PRIMARY, space_before=11, space_after=3, align=WD_ALIGN_PARAGRAPH.LEFT)

def add_heading_2(doc, text):
    return add_styled_paragraph(doc, text, font_name="Calibri", font_size=11, bold=True, color_rgb=RGB_SECONDARY, space_before=8, space_after=2, align=WD_ALIGN_PARAGRAPH.LEFT)

def add_callout(doc, text, bold_prefix=None):
    tbl = doc.add_table(rows=1, cols=1)
    format_table_structure(tbl)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_BG_CALLOUT)
    set_cell_margins(cell, top=130, bottom=130, left=180, right=160)
    set_cell_borders(cell, top=None, bottom=None, right=None, left={'val': 'single', 'sz': '24', 'color': HEX_SECONDARY})
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        add_run(p, bold_prefix, font_name="Calibri", font_size=9.5, bold=True, italic=False, color_rgb=RGB_PRIMARY)
    add_run(p, text, font_name="Calibri", font_size=9.5, bold=False, italic=True, color_rgb=RGB_TEXT_MUTED)

def add_prompt_callout(doc, prompt_id, prompt_title, prompt_text):
    tbl = doc.add_table(rows=2, cols=1)
    format_table_structure(tbl)
    
    # Linha 0: Cabeçalho do Prompt
    c0 = tbl.cell(0, 0)
    set_cell_background(c0, HEX_PRIMARY)
    set_cell_margins(c0, top=100, bottom=100, left=140, right=140)
    set_cell_borders(c0, top=None, bottom=None, left=None, right=None)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p0.paragraph_format.space_before = Pt(1)
    p0.paragraph_format.space_after = Pt(1)
    add_run(p0, f"{prompt_id} — {prompt_title}", font_name="Calibri", font_size=9.5, bold=True, color_rgb=RGB_WHITE)
    
    # Linha 1: Conteúdo Integral em Fonte Monoespaçada
    c1 = tbl.cell(1, 0)
    set_cell_background(c1, HEX_BG_LABEL)
    set_cell_margins(c1, top=120, bottom=120, left=160, right=160)
    set_cell_borders(c1, 
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        left={'val': 'single', 'sz': '24', 'color': HEX_PRIMARY}
    )
    
    # Processar linhas do prompt
    lines = prompt_text.strip().splitlines()
    for idx, line in enumerate(lines):
        if idx == 0:
            p = c1.paragraphs[0]
        else:
            p = c1.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.05
        add_run(p, line, font_name="Consolas", font_size=8, bold=False, italic=False, color_rgb=RGB_TEXT_DARK)

def extract_prompt_info(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    title_m = re.search(r"^#\s*(.+)$", content, re.M)
    title = title_m.group(1).strip() if title_m else os.path.basename(file_path)
    # Extrair ID e nome amigável
    prompt_id = "PROMPT"
    if " - " in title:
        parts = title.split(" - ", 1)
        prompt_id = parts[0].strip()
        title = parts[1].strip()
    # Extrair bloco de código markdown
    code_m = re.search(r"```(?:markdown)?\s*\n(.*?)\n```", content, re.DOTALL)
    prompt_text = code_m.group(1).strip() if code_m else content.strip()
    return prompt_id, title, prompt_text

def format_cell(cell, paragraphs_data, bg_hex=HEX_WHITE, border_color=HEX_BORDER, padding=(110, 110, 140, 140)):
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=padding[0], bottom=padding[1], left=padding[2], right=padding[3])
    if border_color:
        b_spec = {'val': 'single', 'sz': '4', 'color': border_color}
        set_cell_borders(cell, top=b_spec, bottom=b_spec, left=b_spec, right=b_spec)
    else:
        set_cell_borders(cell, top=None, bottom=None, left=None, right=None)
        
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    p0 = cell.paragraphs[0]
    clear_element_children(p0._p, "r")
    
    for idx, item in enumerate(paragraphs_data):
        text, f_size, is_bold, is_italic, col_rgb, sp_after, alignment, prefix = item
        if idx == 0:
            target_p = p0
        else:
            target_p = cell.add_paragraph()
            
        target_p.alignment = alignment
        target_p.paragraph_format.space_before = Pt(1)
        target_p.paragraph_format.space_after = Pt(sp_after)
        target_p.paragraph_format.line_spacing = 1.15
        
        if prefix:
            add_run(target_p, prefix, font_name="Calibri", font_size=f_size, bold=True, italic=is_italic, color_rgb=col_rgb)
        if text:
            add_run(target_p, text, font_name="Calibri", font_size=f_size, bold=is_bold, italic=is_italic, color_rgb=col_rgb)

def main():
    print("=== INICIANDO CONSTRUCAO INTEGRAL DO RELATORIO EXECUTIVO ===")
    doc = docx.Document()
    
    # Configuração de Página: Formato A4 com Margens Otimizadas (0.75 in = ~1.9 cm)
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    
    # =========================================================================
    # PÁGINA 1 — CAPA E IDENTIFICAÇÃO OFICIAL
    # =========================================================================
    print("Gerando Página 1: Capa e Identificação Oficial...")
    add_styled_paragraph(doc, "CHALLENGE ONE G11 — AI FOR BUSINESS", font_size=20, bold=True, color_rgb=RGB_PRIMARY, space_before=0, space_after=2)
    add_styled_paragraph(doc, "Relatório Executivo de Consultoria em IA — Taranis Black (Rota 4: Finanças e Operações)", font_size=11, bold=False, italic=False, color_rgb=RGB_TEXT_MUTED, space_before=0, space_after=10)
    
    # Tabela 1: Identificação
    t1 = doc.add_table(rows=6, cols=2)
    format_table_structure(t1, col_widths=[Inches(2.2), Inches(4.5)])
    
    # Header T1
    format_cell(t1.cell(0, 0), [("IDENTIFICAÇÃO DO PROJETO E DO CONSULTOR", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_PRIMARY, border_color=None)
    format_cell(t1.cell(0, 1), [("ESPECIALIZAÇÃO EM IA", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=HEX_PRIMARY, border_color=None)
    
    t1_rows = [
        ("Nome do Autor", AUTHOR_NAME, True),
        ("E-mail de Contato", AUTHOR_EMAIL, False),
        ("Programa / Turma", COORTE, True),
        ("Papel Corporativo", f"{AUTHOR_ROLE} (Responsável Técnico e Governança)", False),
        ("Rota Escolhida", "[X] Rota 4 — IA para Finanças e Operações (Selecionada)", True)
    ]
    for idx, (lbl, val, is_b) in enumerate(t1_rows, start=1):
        format_cell(t1.cell(idx, 0), [(lbl, 9.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_BG_LABEL)
        format_cell(t1.cell(idx, 1), [(val, 9.5, is_b, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)
        
    add_styled_paragraph(doc, "", space_before=4, space_after=4)
    
    # Tabela 2: Cenário de Negócios na Taranis Black
    t2 = doc.add_table(rows=5, cols=2)
    format_table_structure(t2, col_widths=[Inches(2.2), Inches(4.5)])
    
    format_cell(t2.cell(0, 0), [("CENÁRIO DE NEGÓCIOS NA TARANIS BLACK — ROTA 4", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_PRIMARY, border_color=None)
    format_cell(t2.cell(0, 1), [("DIAGNÓSTICO QUANTITATIVO", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=HEX_PRIMARY, border_color=None)
    
    t2_rows = [
        ("Público Indicado", "Analistas financeiros, controllers, gerentes de operações, gestores de logística e diretoria executiva da Taranis Black."),
        ("Problema a Resolver", "Atraso de 5 dias úteis no fechamento contábil mensal (D+7 vs D+2), 6,8% de divergências fiscais em faturamento e devoluções gerando R$ 1,875M em fretes e multas, e ciclo de aprovação de crédito B2B retido por 48 horas em caixas de e-mail manuais, totalizando R$ 3,89 milhões de perdas operacionais anuais."),
        ("Métricas Vitais da Empresa", "Faturamento Anual de R$ 48,5 milhões | 280 colaboradores diretos | Crescimento de 35% ao ano | Matriz Corporativa em SP e Centro de Distribuição em Joinville/SC | Portfólio focado em ergonomia corporativa (ErgoPro, SmartDesk e Silence)."),
        ("Gargalos e Dores Centrais", "Perdas operacionais anuais de R$ 3,89 milhões | Queda de 41,4% no EBITDA realizado (R$ 5,77M vs R$ 9,85M orçado) | Inadimplência PDD de 3,4% da receita (R$ 1,11M) | Estouro logístico com fretes de emergência atingindo 2,8% da receita bruta.")
    ]
    for idx, (lbl, val) in enumerate(t2_rows, start=1):
        format_cell(t2.cell(idx, 0), [(lbl, 9.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_BG_LABEL)
        format_cell(t2.cell(idx, 1), [(val, 9.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2 — RESUMO EXECUTIVO DIRECIONADO À CEO
    # =========================================================================
    print("Gerando Página 2: Resumo Executivo & Parecer à CEO...")
    add_heading_1(doc, "RESUMO EXECUTIVO & PARECER DIRECIONADO À CEO")
    add_callout(doc, "Comunicação estratégica e executiva direcionada à Diretora-Presidente (CEO) e ao Conselho de Administração da Taranis Black, consolidando o diagnóstico quantitativo, o plano de modernização com Inteligência Artificial e a viabilidade econômico-financeira do investimento.")
    
    add_styled_paragraph(doc, "", space_before=2, space_after=3)
    add_styled_paragraph(doc, "Prezada Diretora-Presidente e Membros do Conselho de Administração,", bold=True, color_rgb=RGB_PRIMARY, space_after=4)
    
    add_styled_paragraph(doc, 
        "A Taranis Black encerrou o exercício de 2026 com receita bruta realizada de R$ 48,50 milhões, sustentando a trajetória vigorosa de expansão de 35% ao ano. Contudo, a ausência de modernização nos processos operacionais gerou um descompasso crítico de rentabilidade: o EBITDA realizado recuou 41,4% (atingindo R$ 5,77 milhões frente aos R$ 9,85 milhões orçados), pressionado por perdas operacionais diretas de R$ 3,89 milhões ao ano.",
        bold_prefix="1. Diagnóstico da Operação e Perdas Financeiras: ", space_after=4
    )
    
    add_styled_paragraph(doc,
        "O diagnóstico detalhado aponta três gargalos centrais: (1) ciclo de análise de crédito B2B retido por 48 horas úteis em caixas de e-mail manuais, gerando R$ 1,25 milhão em cancelamentos comerciais e elevando a perda por inadimplência (PDD) para R$ 1,11 milhão (3,4% da receita); (2) digitação manual de propostas em PDF no ERP legado, provocando 6,8% de divergências fiscais e um estouro de R$ 1,875 milhão em fretes de emergência e reentregas no CD Joinville/SC; e (3) conciliação contábil manual em três planilhas isoladas, atrasando o fechamento mensal em 5 dias úteis.",
        bold_prefix="2. Gargalos Estruturais Auditados: ", space_after=4
    )
    
    add_styled_paragraph(doc,
        "Para sanar essas dores sem incorrer nos altos custos, paradas e riscos de substituição do ERP legado (orçada em mais de R$ 2 milhões e 18 meses de prazo), desenhamos uma arquitetura de inteligência periférica não invasiva (wrapper). A solução emprega modelos de IA Generativa para extração semântica de propostas em PDF (Document AI), modelos preditivos para cálculo do escore de crédito e algoritmos de pareamento probabilístico (fuzzy matching) para conciliação contábil contínua.",
        bold_prefix="3. Estratégia de Modernização Periférica com IA: ", space_after=4
    )
    
    add_styled_paragraph(doc,
        "A implantação ocorre em três ondas sequenciais: Onda 1 (Semanas 1 a 4 — Quick Win): Pré-Validador Fiscal e Logístico de Pedidos antes do despacho; Onda 2 (Semanas 5 a 8): Assistente de Conciliação Contábil Multicanal acelerando o fechamento para a meta D+2; e Onda 3 (Semanas 9 a 12 — Aposta Estratégica): Motor Paramétrico de Crédito B2B com esteira Fast-Track para 65% dos pedidos.",
        bold_prefix="4. Plano Tático de Implantação em Três Ondas: ", space_after=4
    )
    
    add_styled_paragraph(doc,
        "Com um aporte de capital total de R$ 250.000,00 no primeiro ano, a modelagem preditiva projeta a recuperação direta de R$ 2.501.000,00 anuais em margem operacional líquida. Essa recuperação proporciona um Retorno sobre o Investimento (ROI) de 900% (9,0x) e um Payback simples de apenas 1,2 meses (36 dias de faturamento com perdas estancadas). O EBITDA projetado se recupera para R$ 8,27 milhões ao ano (+43,3%), restabelecendo a margem EBITDA em 21,2%.",
        bold_prefix="5. Retorno Econômico e Payback Projetado: ", space_after=4
    )
    
    add_styled_paragraph(doc,
        "Todas as soluções foram concebidas em estrito alinhamento com o Artigo 20 da LGPD (revisão humana obrigatória em decisões de crédito acima de R$ 80k), com o Protocolo P4S de anonimização e supervisão do Comitê de Governança de IA. Recomendamos a homologação e início imediato da Onda 1 para blindar a lucratividade do negócio.",
        bold_prefix="6. Governança, LGPD e Parecer Final: ", space_after=2
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3 — ROTA 0: BASE ESTRATÉGICA CORPORATIVA (PARTE 1)
    # =========================================================================
    print("Gerando Página 3: Rota 0 — Base Estratégica Corporativa (Parte 1)...")
    add_heading_1(doc, "PARTE 1 — BASE ESTRATÉGICA CORPORATIVA (ROTA 0)")
    add_heading_2(doc, "1. AI Canvas Corporativo — Mapeamento Estratégico em 9 Blocos")
    
    # Tabela 3: AI Canvas (Matriz 9 Blocos)
    t_canvas = doc.add_table(rows=4, cols=3)
    format_table_structure(t_canvas, col_widths=[Inches(2.2), Inches(2.2), Inches(2.3)])
    
    canvas_blocks = [
        # Linha 0 (Header da Matriz)
        [("PROPOSTA DE VALOR", "Recuperar R$ 2,50M/ano de margem estancando perdas operacionais e acelerando o Lead Time de 5 dias para < 2h sem trocar o ERP."),
         ("PROBLEMAS & DORES", "R$ 3,89M em perdas anuais, fechamento contábil atrasado em 5 dias (D+7), fila de 48h no crédito e estouro de fretes de R$ 1,875M."),
         ("BENEFICIÁRIOS", "Diretoria Executiva (EBITDA), Controladoria (fechamento D+2), Operações/CD Joinville (zero retrabalho) e Clientes B2B.")],
        # Linha 1
        [("SOLUÇÕES DE IA", "Motor de Crédito B2B Fast-Track, Conciliador Contábil Multicanal Fuzzy Matching e Pré-Validador Fiscal/Logístico semântico."),
         ("DADOS & ATIVOS", "Histórico de vendas ERP legado, extratos bancários OFX, relatórios fiscais SPED, matriz de fretes CIF/FOB e birô Serasa."),
         ("INFRAESTRUTURA", "Camada periférica em Python, instâncias LLM corporativas com Zero Data Retention, OCR Document AI e microsserviços seguros.")],
        # Linha 2
        [("CUSTOS & APORTE", "Investimento total de R$ 250k no Ano 1: R$ 120k em desenvolvimento, R$ 50k em licenças de IA, R$ 50k em integração e R$ 30k em capacitação."),
         ("RETORNO / ROI", "Recuperação líquida de R$ 2.501.000,00/ano, Payback em 1,2 meses (36 dias) e ROI de 900% (9,0x o valor investido)."),
         ("GOVERNANÇA & RISCOS", "Artigo 20 da LGPD (revisão humana), Protocolo P4S de anonimização, auditoria de alucinações e Comitê Multidisciplinar de IA.")]
    ]
    
    # Renderizar blocos
    for r_idx, row_blocks in enumerate(canvas_blocks):
        for c_idx, (b_title, b_desc) in enumerate(row_blocks):
            cell = t_canvas.cell(r_idx, c_idx)
            format_cell(cell, [
                (b_title, 9, True, False, RGB_PRIMARY, 2, WD_ALIGN_PARAGRAPH.LEFT, None),
                (b_desc, 8.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)
            ], bg_hex=HEX_BG_ZEBRA if r_idx % 2 == 0 else HEX_WHITE, padding=(90, 90, 110, 110))
            
    add_heading_2(doc, "2. Detalhamento dos Três Casos de Uso Corporativos Priorizados")
    
    t_cases = doc.add_table(rows=4, cols=4)
    format_table_structure(t_cases, col_widths=[Inches(1.8), Inches(1.8), Inches(1.6), Inches(1.5)])
    
    headers_cases = [("Iniciativa de IA", WD_ALIGN_PARAGRAPH.LEFT), ("Mecanismo Tecnológico", WD_ALIGN_PARAGRAPH.LEFT), ("Impacto Financeiro Direto", WD_ALIGN_PARAGRAPH.LEFT), ("Métrica / KPI", WD_ALIGN_PARAGRAPH.LEFT)]
    for c_idx, (h_txt, h_alg) in enumerate(headers_cases):
        format_cell(t_cases.cell(0, c_idx), [(h_txt, 9, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 100, 100))
        
    cases_data = [
        ("Caso 1: Motor Inteligente de Crédito B2B", "LLM Document AI para leitura de propostas + escore preditivo de inadimplência + API Serasa.", "Recupera R$ 1,43M/ano (destrava vendas e reduz inadimplência de 3,4% para 1,5%).", "SLA de crédito reduzido de 48h para < 15 min em 65% dos pedidos."),
        ("Caso 2: Conciliador Contábil Multicanal", "Pareamento probabilístico (fuzzy matching) entre extratos bancários e ERP legado.", "Economiza R$ 180k/ano em horas extras e auditorias contábeis de fechamento.", "Fechamento mensal reduzido de D+7 para D+2 (elimina 5 dias de atraso)."),
        ("Caso 3: Pré-Validador Fiscal e Logístico", "Validação sintática e semântica de pedidos contra catálogo, regras SEFAZ e fretes CIF/FOB.", "Estanca R$ 1,35M/ano em fretes extras de devolução, reentregas e multas fiscais.", "Divergências fiscais de NF-e reduzidas de 6,8% para menos de 0,3%.")
    ]
    for r_idx, (c_name, c_mec, c_imp, c_kpi) in enumerate(cases_data, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        format_cell(t_cases.cell(r_idx, 0), [(c_name, 8.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(80, 80, 90, 90))
        format_cell(t_cases.cell(r_idx, 1), [(c_mec, 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(80, 80, 90, 90))
        format_cell(t_cases.cell(r_idx, 2), [(c_imp, 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(80, 80, 90, 90))
        format_cell(t_cases.cell(r_idx, 3), [(c_kpi, 8, True, False, RGB_SUCCESS_GREEN, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(80, 80, 90, 90))

    add_heading_2(doc, "3. Classificação Tecnológica e Diretrizes Human-in-the-Loop (LGPD)")
    add_styled_paragraph(doc, 
        "A arquitetura combina IA Generativa (extração de documentos não estruturados em PDF e redação de minutas), IA Preditiva (scoring estatístico de risco e anomalias contábeis) e Heurísticas Determinísticas (tabelas rígidas de alçadas e fretes). Sob a ótica de supervisão humana (Art. 20 da LGPD), pedidos com valor superior a R$ 80.000,00 ou clientes com score intermediário exigem validação em 1 clique do Gerente Financeiro, sendo terminantemente proibida a rejeição 100% autônoma.",
        space_after=2
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 4 — ROTA 0: PRIORIZAÇÃO, GESTÃO DE MUDANÇA E GOVERNANÇA (PARTE 2)
    # =========================================================================
    print("Gerando Página 4: Rota 0 — Priorização, Mudança e Governança...")
    add_heading_1(doc, "ROTA 0 — PRIORIZAÇÃO, GESTÃO DE MUDANÇAS E GOVERNANÇA")
    add_heading_2(doc, "4. Matriz Esforço × Impacto e Sequenciamento de Rollout em Ondas")
    
    t_matriz = doc.add_table(rows=5, cols=4)
    format_table_structure(t_matriz, col_widths=[Inches(1.8), Inches(1.8), Inches(1.2), Inches(1.9)])
    
    headers_m = [("Quadrante / Onda", WD_ALIGN_PARAGRAPH.LEFT), ("Iniciativa Priorizada", WD_ALIGN_PARAGRAPH.LEFT), ("Relação Esforço x Impacto", WD_ALIGN_PARAGRAPH.CENTER), ("Justificativa Estratégica", WD_ALIGN_PARAGRAPH.LEFT)]
    for c_idx, (h_txt, h_alg) in enumerate(headers_m):
        format_cell(t_matriz.cell(0, c_idx), [(h_txt, 9, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 90, 90))
        
    matriz_data = [
        ("Onda 1 (Sem 1 a 4) — Quick Win", "Caso 3: Pré-Validador Fiscal & Logístico", "Baixo Esforço / Alto Impacto", "Middleware em Python sem alteração no código do ERP; estanca R$ 1,35M/ano no primeiro mês."),
        ("Onda 2 (Sem 5 a 8) — Melhoria", "Caso 2: Conciliador Contábil Multicanal", "Médio Esforço / Alto Impacto", "Matching probabilístico OFX/ERP; encurta fechamento para D+2 e economiza R$ 180k/ano."),
        ("Onda 3 (Sem 9 a 12) — Estratégico", "Caso 1: Motor de Crédito B2B Fast-Track", "Médio Esforço / Altíssimo Impacto", "Integração via API Serasa; destrava R$ 1,43M/ano em vendas e corta inadimplência."),
        ("VETO ESTRATÉGICO (Time Sink)", "Substituição do ERP Legado Central", "Esforço Extremo / Retorno Incerto", "VETADA: custo superior a R$ 2M e paralisação de 12 a 18 meses com altíssimo risco.")
    ]
    for r_idx, (q_onda, q_inic, q_esf, q_just) in enumerate(matriz_data, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        is_veto = (r_idx == 4)
        c_color = RGB_ALERT_RED if is_veto else RGB_PRIMARY
        format_cell(t_matriz.cell(r_idx, 0), [(q_onda, 8.5, True, False, c_color, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))
        format_cell(t_matriz.cell(r_idx, 1), [(q_inic, 8, True, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))
        format_cell(t_matriz.cell(r_idx, 2), [(q_esf, 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=bg, padding=(70, 70, 80, 80))
        format_cell(t_matriz.cell(r_idx, 3), [(q_just, 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))

    add_heading_2(doc, "5. Plano de Gestão de Mudanças Organizacionais (Framework ADKAR)")
    add_styled_paragraph(doc, "Para engajar os 280 colaboradores e assegurar adoção plena sem resistências culturais, o plano estruturou os 5 pilares:", space_after=2)
    
    adkar_items = [
        ("• Awareness (Conscientização): ", "Town Hall executivo com a CEO demonstrando que a IA visa eliminar digitação repetitiva e horas extras, e não reduzir postos de trabalho."),
        ("• Desire (Engajamento): ", "Compromisso de requalificação (reskilling) dos analistas financeiros para atuarem como controladores analíticos e consultores de negócios."),
        ("• Knowledge (Capacitação): ", "Trilha prática com turmas de 15 colaboradores em engenharia de prompts financeiros, validação fiscal e operação das esteiras de IA."),
        ("• Ability (Sustentação): ", "Rede de 5 Campeões de IA locais alocados em Finanças e no CD Joinville/SC prestando suporte operacional contínuo em ambiente Sandbox."),
        ("• Reinforcement (Reforço): ", "Vincular a redução do fechamento contábil para a meta D+2 e a redução de divergências fiscais aos bônus semestrais de PLR.")
    ]
    for b_pref, b_txt in adkar_items:
        add_styled_paragraph(doc, b_txt, bold_prefix=b_pref, space_after=1.5)

    add_heading_2(doc, "6. Política Corporativa de IA Responsável, LGPD e Comitê de Ética")
    add_styled_paragraph(doc, 
        "A governança institui 4 Níveis de Sensibilidade: Nível 1 (Público — liberado), Nível 2 (Interno — restrito a processos gerais), Nível 3 (Confidencial — DRE e fretes, exclusivo para ferramentas corporativas pagas com cláusula Zero Data Retention) e Nível 4 (Restrito/LGPD — salários e CPFs, exigindo anonimização obrigatória via Protocolo P4S de 4 passos). O Comitê Multidisciplinar (DPO, TI, Finanças e Operações) homologa ferramentas, aplicando o Artigo 482 da CLT em casos de descumprimento.",
        space_after=2
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 5 — ROTA 4: MAPEAMENTO LEAN SIPOC & EFICIÊNCIA DE FLUXO
    # =========================================================================
    print("Gerando Página 5: Rota 4 — Mapeamento Lean SIPOC...")
    add_heading_1(doc, "PARTE 2 — ESPECIALIZAÇÃO: IA PARA FINANÇAS E OPERAÇÕES (ROTA 4)")
    add_heading_2(doc, "1. Mapeamento do Macroprocesso de Pedidos B2B — Matriz Lean SIPOC")
    
    t_sipoc = doc.add_table(rows=2, cols=5)
    format_table_structure(t_sipoc, col_widths=[Inches(1.3), Inches(1.3), Inches(1.7), Inches(1.3), Inches(1.2)])
    
    sipoc_headers = [("Suppliers", WD_ALIGN_PARAGRAPH.LEFT), ("Inputs", WD_ALIGN_PARAGRAPH.LEFT), ("Process (As-Is)", WD_ALIGN_PARAGRAPH.LEFT), ("Outputs", WD_ALIGN_PARAGRAPH.LEFT), ("Customers", WD_ALIGN_PARAGRAPH.LEFT)]
    for c_idx, (h_txt, h_alg) in enumerate(sipoc_headers):
        format_cell(t_sipoc.cell(0, c_idx), [(h_txt, 9, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 90, 90))
        
    format_cell(t_sipoc.cell(1, 0), [("• Vendedores B2B\n• Clientes Corporativos\n• Birô Serasa Experian\n• Gerência Financeira\n• SEFAZ / Transportadoras", 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)
    format_cell(t_sipoc.cell(1, 1), [("• Propostas em PDF\n• Ficha Cadastral / CNPJ\n• Histórico de Compras\n• Tabela de Preços\n• Matriz de Fretes CIF/FOB", 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)
    format_cell(t_sipoc.cell(1, 2), [("1. Envio por e-mail manual\n2. Triagem e consulta telas\n3. Retenção na alçada (48h)\n4. Digitação de NF-e no ERP\n5. Separação CD e despacho", 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)
    format_cell(t_sipoc.cell(1, 3), [("• Pedidos de Venda no ERP\n• Parecer de Crédito\n• DANFE / XML da NF-e\n• Boletos Bancários\n• Minutas de Despacho", 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)
    format_cell(t_sipoc.cell(1, 4), [("• Cliente Comprador B2B\n• Expedição CD Joinville\n• Transportadoras\n• Faturamento / Fiscal\n• Controladoria Contábil", 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_WHITE)

    add_heading_2(doc, "2. Diagnóstico da Eficiência do Ciclo de Processo (Process Cycle Efficiency — PCE)")
    
    t_pce = doc.add_table(rows=2, cols=4)
    format_table_structure(t_pce, col_widths=[Inches(1.6), Inches(1.6), Inches(1.8), Inches(1.7)])
    
    pce_headers = [("Touch Time (Trabalho Útil)", WD_ALIGN_PARAGRAPH.CENTER), ("Lead Time Total Atual", WD_ALIGN_PARAGRAPH.CENTER), ("PCE Atual (Eficiência)", WD_ALIGN_PARAGRAPH.CENTER), ("Desperdício em Fila", WD_ALIGN_PARAGRAPH.CENTER)]
    for c_idx, (h_txt, h_alg) in enumerate(pce_headers):
        format_cell(t_pce.cell(0, c_idx), [(h_txt, 9, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 90, 90))
        
    format_cell(t_pce.cell(1, 0), [("1,5 horas (90 min)", 10, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=HEX_WHITE)
    format_cell(t_pce.cell(1, 1), [("40,0 horas úteis (5 dias)", 10, True, False, RGB_ALERT_RED, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=HEX_WHITE)
    format_cell(t_pce.cell(1, 2), [("3,75% (Altamente Crítico)", 10, True, False, RGB_ALERT_RED, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=HEX_WHITE)
    format_cell(t_pce.cell(1, 3), [("96,25% (38,5h em filas)", 10, True, False, RGB_ALERT_RED, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=HEX_WHITE)

    add_heading_2(doc, "3. Comparativo de Fluxo: Cenário Atual (As-Is) vs. Fluxo Otimizado com IA (To-Be)")
    
    t_comp = doc.add_table(rows=6, cols=3)
    format_table_structure(t_comp, col_widths=[Inches(1.8), Inches(2.5), Inches(2.5)])
    
    comp_headers = [("Etapa Operacional", WD_ALIGN_PARAGRAPH.LEFT), ("Fluxo Atual Manual (As-Is)", WD_ALIGN_PARAGRAPH.LEFT), ("Fluxo Otimizado com IA (To-Be)", WD_ALIGN_PARAGRAPH.LEFT)]
    for c_idx, (h_txt, h_alg) in enumerate(comp_headers):
        format_cell(t_comp.cell(0, c_idx), [(h_txt, 9, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 90, 90))
        
    comp_data = [
        ("1. Recepção da Proposta", "Consultor comercial envia PDF solto por e-mail; analista tria manualmente.", "Ingestão automática via Document AI com extração instantânea dos campos em JSON."),
        ("2. Análise de Crédito", "Fila de espera de até 48h na caixa postal do gerente; consultas manuais.", "Fast-Track em < 15 min para 65% dos pedidos via motor preditivo integrado à Serasa."),
        ("3. Validação Fiscal / Frete", "Sem conferência prévia; erros de alíquota e frete CIF/FOB detectados na entrega.", "Pré-validador cruza itens contra o catálogo SEFAZ e tabelas de fretes antes da NF-e."),
        ("4. Emissão de NF-e", "Digitação manual dos itens no ERP legado (40 min por pedido); 6,8% de erros.", "Geração automática da ordem no ERP e disparo de NF-e em segundos com < 0,3% de erros."),
        ("5. Fechamento Contábil", "Fechamento manual em D+7 com 3 planilhas isoladas e conferência linha a linha.", "Conciliação contínua diária por pareamento probabilístico atingindo a meta D+2.")
    ]
    for r_idx, (etp, as_is, to_be) in enumerate(comp_data, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        format_cell(t_comp.cell(r_idx, 0), [(etp, 8.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))
        format_cell(t_comp.cell(r_idx, 1), [(as_is, 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))
        format_cell(t_comp.cell(r_idx, 2), [(to_be, 8, False, False, RGB_SUCCESS_GREEN, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 6 — ROTA 4: CAUSA-RAIZ (ISHIKAWA 6M), 5 PORQUÊS E PLANO 5W2H
    # =========================================================================
    print("Gerando Página 6: Rota 4 — Ishikawa, 5 Porquês e 5W2H...")
    add_heading_1(doc, "ROTA 4 — DIAGNÓSTICO DE CAUSA-RAIZ E PLANO DE AÇÃO 5W2H")
    add_heading_2(doc, "4. Diagrama de Ishikawa Estruturado nos 6M (Causa-Raiz das Perdas de R$ 3,89M)")
    
    t_ishi = doc.add_table(rows=7, cols=2)
    format_table_structure(t_ishi, col_widths=[Inches(1.8), Inches(4.9)])
    
    format_cell(t_ishi.cell(0, 0), [("Dimensão (6M)", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 90, 90))
    format_cell(t_ishi.cell(0, 1), [("Vulnerabilidade Crítica Auditada na Taranis Black", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(80, 80, 90, 90))
    
    ishi_data = [
        ("1. Método", "Fluxo de aprovação dependente de e-mails informais; falta de esteira de alçadas; dependência de 3 planilhas locais desconectadas; regras CIF/FOB não checadas antes da venda."),
        ("2. Máquina / Tecnologia", "ERP legado sem APIs modernas de integração; ausência de OCR/Document AI para propostas comerciais; inexistência de validação sintática antes do faturamento."),
        ("3. Mão de Obra", "Assistentes sobrecarregados com digitação mecânica repetitiva; centralização de alçadas de baixo valor no gerente; estresse e turnover nos fechamentos contábeis."),
        ("4. Material", "Propostas comerciais em PDF com especificações incompletas; divergência de códigos SKU entre vendas e ERP; cadastros de clientes com CNPJ desatualizado."),
        ("5. Medição", "Inexistência de monitoramento de SLAs por etapa em tempo real; diretoria informada sobre atrasos e divergências de frete apenas no encerramento contábil mensal."),
        ("6. Meio Ambiente", "Crescimento acelerado de 35% ao ano superando a maturidade operacional dos sistemas; pico comercial concentrando mais de 45% do faturamento no final do mês.")
    ]
    for r_idx, (m_dim, m_vul) in enumerate(ishi_data, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        format_cell(t_ishi.cell(r_idx, 0), [(m_dim, 8.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))
        format_cell(t_ishi.cell(r_idx, 1), [(m_vul, 8, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(70, 70, 80, 80))

    add_heading_2(doc, "5. Cadeia Causal dos 5 Porquês para os Três Gargalos Estruturais")
    
    pq_items = [
        ("• Gargalo 1 — Fechamento em D+7: ", "Por que atrasa 5 dias? Porque conciliação é manual. Por que manual? Porque dados vêm em 3 planilhas isoladas. Por que isoladas? ERP não cruza extratos OFX. Por que não cruza? Falta pareamento probabilístico. Causa-raiz: Ausência de conciliador com fuzzy matching."),
        ("• Gargalo 2 — Retenção de Crédito em 48h: ", "Por que demora 48h? Propostas ficam paradas no e-mail do gerente. Por que no e-mail? Faltam alçadas automáticas. Por que faltam? ERP não possui motor de scoring. Causa-raiz: Inexistência de motor preditivo de crédito B2B com Fast-Track."),
        ("• Gargalo 3 — Estouro de R$ 1,875M em Fretes: ", "Por que estourou fretes? 6,8% de divergências fiscais e reentregas. Por que divergências? Erros de digitação de SKU e frete CIF/FOB. Por que erros? Propostas digitadas à mão sem pré-validação. Causa-raiz: Ausência de pré-validador fiscal/logístico.")
    ]
    for b_pref, b_txt in pq_items:
        add_styled_paragraph(doc, b_txt, bold_prefix=b_pref, space_after=2)

    add_heading_2(doc, "6. Matriz de Plano de Ação Preventivo 5W2H Lean para as Três Iniciativas")
    
    t_5w2h = doc.add_table(rows=4, cols=7)
    format_table_structure(t_5w2h, col_widths=[Inches(1.1), Inches(1.2), Inches(0.8), Inches(0.7), Inches(0.9), Inches(1.3), Inches(0.7)])
    
    headers_5w = [("O que (What)", WD_ALIGN_PARAGRAPH.LEFT), ("Por que (Why)", WD_ALIGN_PARAGRAPH.LEFT), ("Onde (Where)", WD_ALIGN_PARAGRAPH.LEFT), ("Quando (When)", WD_ALIGN_PARAGRAPH.CENTER), ("Quem (Who)", WD_ALIGN_PARAGRAPH.LEFT), ("Como (How)", WD_ALIGN_PARAGRAPH.LEFT), ("Custo (R$)", WD_ALIGN_PARAGRAPH.RIGHT)]
    for c_idx, (h_txt, h_alg) in enumerate(headers_5w):
        format_cell(t_5w2h.cell(0, c_idx), [(h_txt, 8, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(70, 70, 80, 80))
        
    w2h_data = [
        ("Pré-Validador Fiscal/Logístico", "Estancar R$ 1,35M em fretes e divergências de NF-e.", "CD Joinville / Faturamento", "Onda 1 (Sem 1-4)", "Engenheiro de IA & Faturamento", "Script Python interceptando propostas em PDF contra tabelas.", "R$ 50k"),
        ("Conciliador Contábil Multicanal", "Encurtar fechamento mensal para D+2 e poupar R$ 180k.", "Controladoria Corporativa", "Onda 2 (Sem 5-8)", "Consultor IA & Controller", "Algoritmo de fuzzy matching pareando OFX e ERP legado.", "R$ 80k"),
        ("Motor de Crédito B2B Fast-Track", "Destravar R$ 1,43M em vendas e cortar inadimplência.", "Financeiro / Comercial", "Onda 3 (Sem 9-12)", "Engenheiro IA & Gerente Fin.", "Modelagem preditiva integrada à API Serasa Experian.", "R$ 120k")
    ]
    for r_idx, (w_o, w_p, w_on, w_q, w_qm, w_c, w_cs) in enumerate(w2h_data, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        format_cell(t_5w2h.cell(r_idx, 0), [(w_o, 7.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_5w2h.cell(r_idx, 1), [(w_p, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_5w2h.cell(r_idx, 2), [(w_on, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_5w2h.cell(r_idx, 3), [(w_q, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_5w2h.cell(r_idx, 4), [(w_qm, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_5w2h.cell(r_idx, 5), [(w_c, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_5w2h.cell(r_idx, 6), [(w_cs, 7.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=bg, padding=(60, 60, 70, 70))

    doc.add_page_break()

    # =========================================================================
    # PÁGINA 7 — ROTA 4: DRE AUDITADA ORÇADO VS. REALIZADO & RECUPERAÇÃO DE MARGEM
    # =========================================================================
    print("Gerando Página 7: Rota 4 — DRE Auditada e Projeções...")
    add_heading_1(doc, "ROTA 4 — DRE AUDITADA, MARGENS E RECUPERAÇÃO COM IA")
    add_heading_2(doc, "7. Demonstrativo de Resultados do Exercício (DRE 2026 Auditada) — Orçado vs. Realizado")
    
    t_dre = doc.add_table(rows=12, cols=6)
    format_table_structure(t_dre, col_widths=[Inches(1.8), Inches(1.0), Inches(1.0), Inches(0.9), Inches(0.8), Inches(1.2)])
    
    dre_headers = [("Conta da DRE", WD_ALIGN_PARAGRAPH.LEFT), ("Orçado 2026", WD_ALIGN_PARAGRAPH.RIGHT), ("Realizado 2026", WD_ALIGN_PARAGRAPH.RIGHT), ("Desvio (R$)", WD_ALIGN_PARAGRAPH.RIGHT), ("Var %", WD_ALIGN_PARAGRAPH.CENTER), ("Impacto / Causa", WD_ALIGN_PARAGRAPH.LEFT)]
    for c_idx, (h_txt, h_alg) in enumerate(dre_headers):
        format_cell(t_dre.cell(0, c_idx), [(h_txt, 8, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(60, 60, 70, 70))
        
    dre_rows = [
        ("Receita Bruta Total", "R$ 48.600.000", "R$ 48.500.000", "-R$ 100.000", "-0,2%", "Meta de vendas mantida", False, False),
        ("(-) Deduções / Cancelamentos", "-R$ 560.000", "-R$ 1.235.000", "-R$ 675.000", "+120,5%", "Cancelamentos por morosidade", True, False),
        ("(-) Impostos sobre Vendas (17%)", "-R$ 8.262.000", "-R$ 8.245.000", "+R$ 17.000", "-0,2%", "Dentro do padrão", False, False),
        ("(=) Receita Líquida Operacional", "R$ 39.778.000", "R$ 39.020.000", "-R$ 758.000", "-1,9%", "Pressionada por cancelamentos", False, False),
        ("(-) Custos dos Produtos (CPV/CMV)", "-R$ 20.078.000", "-R$ 20.590.000", "-R$ 512.000", "+2,5%", "Pequeno desvio em insumos", False, False),
        ("(=) Lucro Bruto Operacional", "R$ 19.700.000", "R$ 18.430.000", "-R$ 1.270.000", "-6,4%", "Margem Bruta realizada 47,2%", False, False),
        ("(-) OPEX: Fretes CD & Reentregas", "-R$ 2.590.000", "-R$ 4.465.000", "-R$ 1.875.000", "+72,4%", "Estouro em fretes e multas", True, False),
        ("(-) OPEX: Provisão PDD (Inadimplência)", "-R$ 440.000", "-R$ 1.110.000", "-R$ 670.000", "+152,3%", "Inadimplência de 3,4% da receita", True, False),
        ("(-) OPEX: Horas Extras & Auditorias", "-R$ 120.000", "-R$ 300.000", "-R$ 180.000", "+150,0%", "Gargalo no fechamento contábil", True, False),
        ("(=) EBITDA Operacional Realizado", "R$ 9.848.000", "R$ 5.770.000", "-R$ 4.078.000", "-41,4%", "Quebra crítica de rentabilidade", True, True),
        ("(=) Lucro Líquido Realizado", "R$ 5.965.080", "R$ 3.108.600", "-R$ 2.856.480", "-47,9%", "Margem Líquida recuou para 8,0%", True, True)
    ]
    for r_idx, (c_cta, c_orc, c_rea, c_des, c_var, c_imp, is_bad, is_total) in enumerate(dre_rows, start=1):
        bg = HEX_BG_ZEBRA if r_idx % 2 == 0 else HEX_WHITE
        txt_col = RGB_ALERT_RED if is_bad else RGB_TEXT_DARK
        b_font = is_total or is_bad
        format_cell(t_dre.cell(r_idx, 0), [(c_cta, 7.5, b_font, False, RGB_PRIMARY if is_total else RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_dre.cell(r_idx, 1), [(c_orc, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_dre.cell(r_idx, 2), [(c_rea, 7.5, b_font, False, txt_col, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_dre.cell(r_idx, 3), [(c_des, 7.5, b_font, False, txt_col, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_dre.cell(r_idx, 4), [(c_var, 7.5, b_font, False, txt_col, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_dre.cell(r_idx, 5), [(c_imp, 7.5, False, False, RGB_TEXT_MUTED, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(50, 50, 60, 60))

    add_heading_2(doc, "8. Análise de Margens de Contribuição e Gargalos por Linha de Produto")
    
    t_prod = doc.add_table(rows=5, cols=5)
    format_table_structure(t_prod, col_widths=[Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.6)])
    
    prod_headers = [("Linha de Produto", WD_ALIGN_PARAGRAPH.LEFT), ("Preço Médio", WD_ALIGN_PARAGRAPH.RIGHT), ("Volume Anual", WD_ALIGN_PARAGRAPH.CENTER), ("Margem Bruta", WD_ALIGN_PARAGRAPH.CENTER), ("Gargalo Operacional Diagnosticado", WD_ALIGN_PARAGRAPH.LEFT)]
    for c_idx, (h_txt, h_alg) in enumerate(prod_headers):
        format_cell(t_prod.cell(0, c_idx), [(h_txt, 8, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(60, 60, 70, 70))
        
    prod_data = [
        ("ErgoPro (Cadeiras Ergonômicas)", "R$ 1.850", "14.500 un", "44,2% (Orç: 48%)", "6,8% de divergências em opcionais de braço e NF-e."),
        ("SmartDesk (Mesas Ajustáveis)", "R$ 3.400", "3.200 un", "38,5% (Orç: 45%)", "Menor margem; frete pesado e propostas retidas 48h."),
        ("Silence (Painéis Acústicos)", "R$ 950", "8.800 un", "52,0% (Orç: 55%)", "Maior margem líquida; atrasos na expedição do CD."),
        ("Acessórios & Suportes Ergonômicos", "R$ 320", "7.600 un", "48,0% (Orç: 50%)", "Envio fracionado com pequenas divergências de estoque.")
    ]
    for r_idx, (p_lin, p_prc, p_vol, p_mrg, p_gar) in enumerate(prod_data, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        format_cell(t_prod.cell(r_idx, 0), [(p_lin, 7.5, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_prod.cell(r_idx, 1), [(p_prc, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.RIGHT, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_prod.cell(r_idx, 2), [(p_vol, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_prod.cell(r_idx, 3), [(p_mrg, 7.5, True, False, RGB_ALERT_RED if "38,5%" in p_mrg else RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=bg, padding=(50, 50, 60, 60))
        format_cell(t_prod.cell(r_idx, 4), [(p_gar, 7.5, False, False, RGB_TEXT_MUTED, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(50, 50, 60, 60))

    add_heading_2(doc, "9. Projeção Orçamentária Preditiva Pós-Implementação de IA")
    add_styled_paragraph(doc,
        "Com a implantação das três ondas de IA e investimento de R$ 250.000,00, a companhia estanca perdas operacionais anuais de R$ 2.501.000,00 (R$ 1,35M em fretes, R$ 680k em PDD, R$ 291k em vendas destravadas e R$ 180k em horas extras). O EBITDA projetado atinge R$ 8.271.000,00 (+43,3% sobre 2026), o Lucro Líquido atinge R$ 4.759.000,00 (+53,1%), proporcionando um Payback em apenas 1,2 meses (36 dias) e um ROI consolidado de 9,0x (900%).",
        space_after=2
    )

    doc.add_page_break()

    # =========================================================================
    # PÁGINAS 8 A 10 — ANEXO DE EVIDÊNCIAS & ENGENHARIA DE PROMPTS COMPLETA
    # =========================================================================
    print("Gerando Páginas 8 a 10: Anexo de Evidências e Engenharia de Prompts Completa...")
    add_heading_1(doc, "ANEXO DE EVIDÊNCIAS E ENGENHARIA DE PROMPTS")
    add_heading_2(doc, "1. Matriz de Artefatos Desenvolvidos e Versionados no Repositório")
    
    t_evid = doc.add_table(rows=5, cols=4)
    format_table_structure(t_evid, col_widths=[Inches(1.8), Inches(2.3), Inches(1.8), Inches(0.8)])
    
    evid_headers = [("Artefato Técnico", WD_ALIGN_PARAGRAPH.LEFT), ("Descrição do Conteúdo", WD_ALIGN_PARAGRAPH.LEFT), ("Caminho Físico no Projeto", WD_ALIGN_PARAGRAPH.LEFT), ("Status", WD_ALIGN_PARAGRAPH.CENTER)]
    for c_idx, (h_txt, h_alg) in enumerate(evid_headers):
        format_cell(t_evid.cell(0, c_idx), [(h_txt, 8.5, True, False, RGB_WHITE, 1, h_alg, None)], bg_hex=HEX_PRIMARY, border_color=None, padding=(70, 70, 80, 80))
        
    evid_rows = [
        ("AI Canvas Corporativo & Casos de Uso", "Mapeamento dos 9 blocos estratégicos e detalhamento das 3 soluções de IA.", "02_rota_0_estrategia/01_ai_canvas_taranis_black.md", "Homologado"),
        ("Matriz Esforço x Impacto & ADKAR", "Priorização em 3 ondas, definição de OKRs corporativos e gestão de mudanças.", "02_rota_0_estrategia/02_matriz_esforco_impacto_metricas_mudancas.md", "Homologado"),
        ("Política de IA Corporativa & LGPD", "Diretrizes de uso responsável, matriz de 4 níveis e protocolo P4S de anonimização.", "02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md", "Homologado"),
        ("Mapeamento SIPOC, Ishikawa & DRE", "Dossiê completo da Rota 4 com PCE, 6M, 5 Porquês, 5W2H e auditoria da DRE.", "03_rota_4_financas_operacoes/", "Homologado")
    ]
    for r_idx, (art, dsc, cam, stt) in enumerate(evid_rows, start=1):
        bg = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        format_cell(t_evid.cell(r_idx, 0), [(art, 8, True, False, RGB_PRIMARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_evid.cell(r_idx, 1), [(dsc, 7.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_evid.cell(r_idx, 2), [(cam, 7.5, False, False, RGB_SECONDARY, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 70, 70))
        format_cell(t_evid.cell(r_idx, 3), [(stt, 8, True, False, RGB_SUCCESS_GREEN, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=bg, padding=(60, 60, 70, 70))

    add_heading_2(doc, "2. Engenharia de Prompts Corporativos — Íntegra das Instruções Operacionais")
    add_styled_paragraph(doc, "Abaixo estão reproduzidas na íntegra as instruções operacionais de engenharia de prompts utilizadas nas Rotas 0 e 4:", space_after=3)
    
    prompt_file_paths = [
        "02_rota_0_estrategia/prompts/01_prompt_ai_canvas.md",
        "02_rota_0_estrategia/prompts/02_prompt_matriz_esforco_impacto.md",
        "02_rota_0_estrategia/prompts/03_prompt_politica_ia_responsavel.md",
        "03_rota_4_financas_operacoes/prompts/01_prompt_sipoc_mapeamento.md",
        "03_rota_4_financas_operacoes/prompts/02_prompt_ishikawa_causa_raiz.md",
        "03_rota_4_financas_operacoes/prompts/03_prompt_diagnostico_orcado_realizado.md"
    ]
    
    prompts_count = 0
    for p_path in prompt_file_paths:
        if os.path.exists(p_path):
            p_id, p_title, p_text = extract_prompt_info(p_path)
            add_prompt_callout(doc, p_id, p_title, p_text)
            add_styled_paragraph(doc, "", space_before=2, space_after=3)
            prompts_count += 1
            print(f"  [PROMPT INSERIDO] {p_id}: {p_title} ({len(p_text)} caracteres)")
            
    add_heading_2(doc, "3. Procedimento de Submissão Oficial na Plataforma Alura")
    t_sub = doc.add_table(rows=4, cols=2)
    format_table_structure(t_sub, col_widths=[Inches(0.6), Inches(6.1)])
    
    sub_steps = [
        ("1", "Certifique-se de que este documento foi carregado no Google Drive com permissão pública: 'Qualquer pessoa com o link pode ler'."),
        ("2", "Copie o link público gerado pelo Google Docs."),
        ("3", "Acesse a plataforma da Alura, navegue até a atividade de entrega do challenge e cole o link no campo designado."),
        ("4", "Apenas o link do Google Docs é aceito para a banca examinadora. Não envie arquivos PDF ou anexos locais.")
    ]
    for idx, (num, txt) in enumerate(sub_steps):
        bg = HEX_WHITE if idx % 2 == 0 else HEX_BG_ZEBRA
        format_cell(t_sub.cell(idx, 0), [(num, 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.CENTER, None)], bg_hex=HEX_PRIMARY, padding=(60, 60, 70, 70))
        format_cell(t_sub.cell(idx, 1), [(txt, 8.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT, None)], bg_hex=bg, padding=(60, 60, 80, 80))

    # =========================================================================
    # SALVAMENTO E DUPLICAÇÃO DE SEGURANÇA
    # =========================================================================
    print(f"\nSalvando documento executivo oficial em: {OUTPUT_DOCX}...")
    doc.save(OUTPUT_DOCX)
    
    print(f"Salvando espelho de segurança homologado em: {BACKUP_DOCX}...")
    shutil.copyfile(OUTPUT_DOCX, BACKUP_DOCX)

    # =========================================================================
    # AUDITORIA FINAL DE CONFORMIDADE E ZERO EMOJIS
    # =========================================================================
    print("\n=== AUDITORIA FINAL DO DOCUMENTO GERADO ===")
    doc_audit = docx.Document(OUTPUT_DOCX)
    
    total_paras = len(doc_audit.paragraphs)
    total_tables = len(doc_audit.tables)
    emoji_count = 0
    
    for p in doc_audit.paragraphs:
        if EMOJI_PATTERN.search(p.text):
            emoji_count += 1
            
    for t in doc_audit.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    if EMOJI_PATTERN.search(p.text):
                        emoji_count += 1
                        
    print(f"- Total de tabelas estruturadas: {total_tables}")
    print(f"- Total de parágrafos gerados: {total_paras}")
    print(f"- Total de prompts completos inseridos: {prompts_count} de 6")
    print(f"- Contagem de emojis encontrados: {emoji_count}")
    if emoji_count == 0:
        print("[SUCESSO ABSOLUTO] ZERO EMOJIS! O documento atende com rigor institucional a restrição de estilo formal.")
    else:
        print(f"[ALERTA] Foram detectados {emoji_count} emojis residuais.")

if __name__ == "__main__":
    main()
