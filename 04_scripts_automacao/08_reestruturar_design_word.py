"""
Script de Reengenharia Visual, Tipografica e de Contrastes
Projeto: Challenge AI for Business — Taranis Black (ONE G11)
Autor: Arley Ribeiro da Silva Xavier | Consultor de IA
Arquivo Alvo: Challenge AI for Business — Taranis Black (ONE G11) - Rota 4 Finanças - Arley Ribeiro da Silva Xavier.docx
Espelho de Seguranca: 03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import re
import os
import shutil

# Caminhos dos arquivos
INPUT_DOCX = "Challenge AI for Business — Taranis Black (ONE G11) - Rota 4 Finanças - Arley Ribeiro da Silva Xavier.docx"
BACKUP_DOCX = "03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx"

# Identificação do Autor
AUTHOR_NAME = "Arley Ribeiro da Silva Xavier"
AUTHOR_ROLE = "Consultor de IA"
AUTHOR_EMAIL = "arleyrsx@gmail.com"
COORTE = "ONE - AI for Business | G11"

# Paleta de Cores Corporativa Homologada
HEX_PRIMARY_DARK = "1A365D"      # Azul-marinho corporativo escuro
RGB_PRIMARY_DARK = (26, 54, 93)

HEX_SECONDARY_SLATE = "2B6CB0"   # Azul ardósia médio institucional
RGB_SECONDARY_SLATE = (43, 108, 176)

HEX_WHITE = "FFFFFF"             # Branco puro
RGB_WHITE = (255, 255, 255)

HEX_TEXT_DARK = "2D3748"         # Cinza-escuro quase preto (alta legibilidade)
RGB_TEXT_DARK = (45, 55, 72)

HEX_TEXT_MUTED = "4A5568"        # Cinza médio para notas e subtítulos
RGB_TEXT_MUTED = (74, 85, 104)

HEX_BG_LABEL = "F0F4F8"          # Cinza-ardósia claro para rótulos/labels
HEX_BG_ZEBRA = "F7FAFC"          # Cinza-gelo suave para linhas alternadas
HEX_BG_CALLOUT = "EDF2F7"        # Cinza suave institucional para caixas de destaque
HEX_BORDER_SUBTLE = "CBD5E0"     # Borda suave neutra (0.5 pt)

HEX_ALERT_RED = "9B2C2C"         # Vermelho corporativo sóbrio para perdas operacionais
RGB_ALERT_RED = (155, 44, 44)

HEX_SUCCESS_GREEN = "276749"     # Verde corporativo escuro para homologado / ganhos
RGB_SUCCESS_GREEN = (39, 103, 73)

# Regex estrita para banimento total de emojis
EMOJI_PATTERN = re.compile(
    r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299\ufe0f]"
)

def remove_emojis_and_fix_spaces(text):
    if not text:
        return ""
    cleaned = EMOJI_PATTERN.sub("", text)
    # Remover quebras de linha manuais indesejadas no meio de frases
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
    """Define margens internas (padding) da célula em dxa (120 dxa = 6pt, 160 dxa = 8pt)."""
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
    """
    Define bordas por lado:
    top/bottom/left/right podem ser dict(val='single', sz='4', color='CBD5E0') ou None (remove borda).
    """
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
            color = spec.get('color', HEX_BORDER_SUBTLE)
            edge_el = parse_xml(
                f'<w:{edge} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            )
        tcBorders.append(edge_el)
    tcPr.append(tcBorders)

def clear_paragraph_runs(p):
    """Remove todos os runs (w:r) de um paragrafo para evitar runs vazios residuais sem cor."""
    for child in list(p._p):
        if child.tag.endswith("r"):
            p._p.remove(child)

def set_callout_style(cell, text):
    """Aplica o padrão institucional de callout: fundo cinza suave, borda esquerda 3pt azul corporativo."""
    set_cell_background(cell, HEX_BG_CALLOUT)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=160)
    set_cell_borders(cell,
        top=None,
        bottom=None,
        right=None,
        left={'val': 'single', 'sz': '24', 'color': HEX_SECONDARY_SLATE} # 3pt = sz 24
    )
    # Limpar parágrafos excedentes
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    p = cell.paragraphs[0]
    clear_paragraph_runs(p)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    add_run_to_paragraph(p, text, font_size=9.5, italic=True, color_rgb=RGB_TEXT_MUTED)

def add_run_to_paragraph(p, text, font_name="Calibri", font_size=10, bold=False, italic=False, color_rgb=RGB_TEXT_DARK):
    cleaned_text = remove_emojis_and_fix_spaces(text)
    r = p.add_run(cleaned_text)
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor(*color_rgb)
    
    # Assegurar no XML w:rFonts para blindagem contra sobrescrita de estilos
    rPr = r._r.get_or_add_rPr()
    clear_element_children(rPr, "rFonts")
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.insert(0, rFonts)
    return r

def format_cell_content(cell, paragraphs_data, bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE, padding=(120, 120, 160, 160)):
    """
    Configura background, margens, bordas e insere parágrafos estilizados na célula.
    paragraphs_data é uma lista de tuplas:
    (texto, font_size, bold, italic, color_rgb, space_after, align)
    """
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=padding[0], bottom=padding[1], left=padding[2], right=padding[3])
    
    # Borda sutil nos 4 lados se especificada
    if border_color:
        b_spec = {'val': 'single', 'sz': '4', 'color': border_color}
        set_cell_borders(cell, top=b_spec, bottom=b_spec, left=b_spec, right=b_spec)
    else:
        set_cell_borders(cell, top=None, bottom=None, left=None, right=None)
        
    # Limpar parágrafos existentes mantendo apenas o primeiro
    for p in cell.paragraphs[1:]:
        p._p.getparent().remove(p._p)
    p0 = cell.paragraphs[0]
    clear_paragraph_runs(p0)
    
    for idx, item in enumerate(paragraphs_data):
        text, f_size, is_bold, is_italic, col_rgb, sp_after, alignment = item
        if idx == 0:
            target_p = p0
        else:
            target_p = cell.add_paragraph()
            
        target_p.alignment = alignment
        target_p.paragraph_format.space_before = Pt(1)
        target_p.paragraph_format.space_after = Pt(sp_after)
        target_p.paragraph_format.line_spacing = 1.15
        
        # Pode haver sub-runs ou um texto único
        if isinstance(text, list):
            for sub_text, sub_bold, sub_italic, sub_rgb in text:
                add_run_to_paragraph(target_p, sub_text, font_size=f_size, bold=sub_bold, italic=sub_italic, color_rgb=sub_rgb)
        else:
            add_run_to_paragraph(target_p, text, font_size=f_size, bold=is_bold, italic=is_italic, color_rgb=col_rgb)

def format_table_structure(table, col_widths=None):
    """Ajusta propriedades estruturais da tabela (100% largura, cantSplit, tblHeader)."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._tbl.tblPr
    
    # Centralização
    clear_element_children(tblPr, "jc")
    tblPr.append(parse_xml(f'<w:jc {nsdecls("w")} w:val="center"/>'))
    
    # Largura 100%
    clear_element_children(tblPr, "tblW")
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="5000" w:type="pct"/>'))
    
    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        
        # cantSplit em todas as linhas
        if not any(child.tag.endswith('cantSplit') for child in list(trPr)):
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
        # tblHeader na linha de cabeçalho
        if r_idx == 0 and len(table.rows) > 1:
            if not any(child.tag.endswith('tblHeader') for child in list(trPr)):
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
                
        # Largura das células se col_widths fornecido
        if col_widths:
            for c_idx, cell in enumerate(row.cells):
                if c_idx < len(col_widths):
                    cell.width = col_widths[c_idx]

def main():
    print("=== INICIANDO REENGENHARIA VISUAL E TIPOGRAFICA DO DOCUMENTO ===")
    print(f"Lendo documento base: {INPUT_DOCX}")
    doc = docx.Document(INPUT_DOCX)
    
    # -------------------------------------------------------------
    # 1. PARÁGRAFOS DO CORPO E TÍTULOS PRINCIPAIS
    # -------------------------------------------------------------
    print("Configurando hierarquia tipografica dos paragrafos fora de tabelas...")
    
    # Localizar e estilizar o título principal (CHALLENGE ONE G11 — AI FOR BUSINESS)
    # e subtítulo (Relatório Executivo — Taranis Black)
    p_title = doc.paragraphs[0]
    p_title.text = ""
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    add_run_to_paragraph(p_title, "CHALLENGE ONE G11 — AI FOR BUSINESS", font_size=20, bold=True, color_rgb=RGB_PRIMARY_DARK)
    
    p_sub = doc.paragraphs[1]
    p_sub.text = ""
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(10)
    add_run_to_paragraph(p_sub, "Relatório Executivo de Consultoria em IA — Taranis Black (Rota 4)", font_size=11, bold=False, italic=False, color_rgb=RGB_TEXT_MUTED)
    
    # Parágrafo 9 (Heading 1: Resumo Executivo)
    for p in doc.paragraphs:
        if "Resumo Executivo" in p.text:
            p.text = ""
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            add_run_to_paragraph(p, "Resumo Executivo", font_size=14, bold=True, color_rgb=RGB_PRIMARY_DARK)
            break
            
    # Reduzir espaçamento de parágrafos vazios residuais entre tabelas
    for p in doc.paragraphs[2:]:
        if not p.text.strip():
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.0

    # -------------------------------------------------------------
    # 2. TABELA 0: BANNER DE CABEÇALHO DA ROTA
    # -------------------------------------------------------------
    print("Diagramando Tabela 0 (Banner Rota)...")
    t0 = doc.tables[0]
    format_table_structure(t0)
    format_cell_content(t0.cell(0, 0), [
        ("ROTA 4 — IA PARA FINANÇAS E OPERAÇÕES", 12.5, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.CENTER)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(140, 140, 160, 160))

    # -------------------------------------------------------------
    # 3. TABELA 1: CABEÇALHO DE IDENTIFICAÇÃO
    # -------------------------------------------------------------
    print("Diagramando Tabela 1 (Header Identificação)...")
    t1 = doc.tables[1]
    format_table_structure(t1)
    format_cell_content(t1.cell(0, 0), [
        ("IDENTIFICAÇÃO DO ALUNO E DO PROJETO", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 4. TABELA 2: CAMPOS DE IDENTIFICAÇÃO (Nome, E-mail, Turma)
    # -------------------------------------------------------------
    print("Diagramando Tabela 2 (Dados de Identificação)...")
    t2 = doc.tables[2]
    format_table_structure(t2, col_widths=[Inches(1.8), Inches(4.5)])
    
    t2_data = [
        ("Nome completo", AUTHOR_NAME, True),
        ("E-mail", AUTHOR_EMAIL, False),
        ("Turma / Coorte", COORTE, True)
    ]
    for idx, (label, val, is_b) in enumerate(t2_data):
        # Coluna 0 (Rótulo)
        format_cell_content(t2.cell(idx, 0), [
            (label, 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
        ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
        
        # Coluna 1 (Valor)
        format_cell_content(t2.cell(idx, 1), [
            (val, 9.5, is_b, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
        ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 5. TABELA 3: ROTA DE ESPECIALIZAÇÃO ESCOLHIDA
    # -------------------------------------------------------------
    print("Diagramando Tabela 3 (Seleção da Rota)...")
    t3 = doc.tables[3]
    format_table_structure(t3)
    format_cell_content(t3.cell(0, 0), [
        ("Rota de Especialização Escolhida:", 10, True, False, RGB_PRIMARY_DARK, 3, WD_ALIGN_PARAGRAPH.LEFT),
        ("[ ]  Rota 1 — IA para Vendas e Comercial", 9.5, False, False, RGB_TEXT_MUTED, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("[ ]  Rota 2 — IA para Marketing e Conteúdo", 9.5, False, False, RGB_TEXT_MUTED, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("[ ]  Rota 3 — IA para RH e People Analytics", 9.5, False, False, RGB_TEXT_MUTED, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("[X] Rota 4 — IA para Finanças e Operações (Selecionada)", 10, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 6. TABELA 4: CABEÇALHO DO CENÁRIO DE NEGÓCIOS
    # -------------------------------------------------------------
    print("Diagramando Tabela 4 (Header Cenário)...")
    t4 = doc.tables[4]
    format_table_structure(t4)
    format_cell_content(t4.cell(0, 0), [
        ("CENÁRIO DE NEGÓCIOS NA TARANIS BLACK — ROTA 4", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 7. TABELA 5: PÚBLICO INDICADO E PROBLEMA A RESOLVER
    # -------------------------------------------------------------
    print("Diagramando Tabela 5 (Público e Problema)...")
    t5 = doc.tables[5]
    format_table_structure(t5, col_widths=[Inches(1.8), Inches(4.5)])
    
    # Linha 0: Público indicado
    format_cell_content(t5.cell(0, 0), [
        ("Público indicado", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t5.cell(0, 1), [
        ("Analistas financeiros, controllers, gerentes de operações e gestores de logística.", 9.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)
    
    # Linha 1: Problema a resolver
    format_cell_content(t5.cell(1, 0), [
        ("Problema a resolver", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t5.cell(1, 1), [
        ("Atraso de 5 dias úteis no fechamento contábil mensal (D+7 vs D+2), 6,8% de divergências fiscais em faturamento gerando R$ 1,875 milhão em fretes de reentrega e multas no CD Joinville/SC, e ciclo de aprovação de crédito B2B travado por 48 horas em caixas de e-mail manuais, totalizando perdas operacionais anuais diretas de R$ 3,89 milhões.", 9.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 8. TABELA 6: CALLOUT INSTRUÇÃO DO RESUMO EXECUTIVO
    # -------------------------------------------------------------
    print("Diagramando Tabela 6 (Callout Resumo)...")
    t6 = doc.tables[6]
    format_table_structure(t6)
    set_callout_style(t6.cell(0, 0), 
        "Instrução: Escreva este resumo como se fosse uma comunicação direta para a CEO da Taranis Black (diagnóstico geral, iniciativas de IA recomendadas e impacto financeiro esperado em até 15 linhas)."
    )

    # -------------------------------------------------------------
    # 9. TABELA 7: COMUNICAÇÃO EXECUTIVA PARA A CEO
    # -------------------------------------------------------------
    print("Diagramando Tabela 7 (Carta Executiva para a CEO)...")
    t7 = doc.tables[7]
    format_table_structure(t7)
    
    # Limpar linhas excedentes vazias se houver mais de 1 linha
    while len(t7.rows) > 1:
        row_to_del = t7.rows[-1]
        t7._tbl.remove(row_to_del._tr)
        
    format_cell_content(t7.cell(0, 0), [
        ("Prezada Diretora-Presidente (CEO) e Conselho de Administração,", 10, True, False, RGB_PRIMARY_DARK, 4, WD_ALIGN_PARAGRAPH.LEFT),
        ("A Taranis Black encerrou o exercício com receita bruta de R$ 48,5 milhões, confirmando o crescimento comercial contínuo de 35% ao ano. Contudo, a ausência de modernização nos processos operacionais gerou um descompasso crítico: o EBITDA realizado recuou 41,4% (atingindo R$ 5,77 milhões frente aos R$ 9,85 milhões orçados), impactado por perdas operacionais diretas de R$ 3,89 milhões ao ano.", 9.5, False, False, RGB_TEXT_DARK, 3, WD_ALIGN_PARAGRAPH.LEFT),
        ("O diagnóstico detalhado aponta três gargalos centrais: (1) ciclo de análise de crédito B2B retido por 48 horas em caixas de e-mail manuais, gerando R$ 1,25 milhão em cancelamentos comerciais e R$ 1,11 milhão em perdas por inadimplência (3,4% da receita); (2) digitação manual de propostas em PDF no ERP legado, provocando 6,8% de divergências fiscais e um estouro de R$ 1,875 milhão em fretes de emergência e reentregas no CD Joinville/SC; e (3) conciliação contábil manual em três planilhas isoladas, atrasando o fechamento mensal em 5 dias úteis.", 9.5, False, False, RGB_TEXT_DARK, 3, WD_ALIGN_PARAGRAPH.LEFT),
        ("Para sanar essas dificuldades sem incorrer nos altos custos e riscos de substituição do ERP legado, recomendamos a implantação de uma camada periférica de Inteligência Artificial em três ondas: Onda 1 (Pré-Validador Fiscal/Logístico de Pedidos em 4 semanas como Quick Win); Onda 2 (Conciliador Contábil Multicanal reduzindo o fechamento para D+2 em 8 semanas); e Onda 3 (Motor Inteligente de Crédito B2B com Fast-Track para 65% dos pedidos em 12 semanas).", 9.5, False, False, RGB_TEXT_DARK, 3, WD_ALIGN_PARAGRAPH.LEFT),
        ("Com um investimento total de R$ 250.000,00 no primeiro ano, a projeção realista recupera R$ 2.501.000,00 anuais de margem líquida direta, alcançando um Retorno sobre o Investimento (ROI) de 900% (9,0x) e Payback em apenas 1,2 meses (36 dias). Recomendamos a aprovação imediata do plano para sustentar o crescimento lucrativo da companhia.", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE, padding=(140, 140, 180, 180))

    # -------------------------------------------------------------
    # 10. TABELA 8: CABEÇALHO PARTE 1 - ROTA 0
    # -------------------------------------------------------------
    print("Diagramando Tabela 8 (Header Rota 0)...")
    t8 = doc.tables[8]
    format_table_structure(t8)
    format_cell_content(t8.cell(0, 0), [
        ("PARTE 1 — BASE ESTRATÉGICA OBRIGATÓRIA (ROTA 0)", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 11. TABELA 9: CALLOUT ORIENTAÇÃO ROTA 0
    # -------------------------------------------------------------
    print("Diagramando Tabela 9 (Callout Rota 0)...")
    t9 = doc.tables[9]
    format_table_structure(t9)
    set_callout_style(t9.cell(0, 0),
        "Orientação: A Rota 0 é a fundação do trabalho corporativo. Ela assegura visão executiva e governança antes do aprofundamento operacional."
    )

    # -------------------------------------------------------------
    # 12. TABELA 10: ROTA 0 - ETAPA 1 (AI Canvas & Casos de Uso)
    # -------------------------------------------------------------
    print("Diagramando Tabela 10 (AI Canvas)...")
    t10 = doc.tables[10]
    format_table_structure(t10, col_widths=[Inches(1.8), Inches(4.5)])
    
    # Cabeçalho da Tabela 10
    format_cell_content(t10.cell(0, 0), [
        ("Etapa 1 — AI Canvas & Mapeamento de Oportunidades", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)
    format_cell_content(t10.cell(0, 1), [
        ("OBRIGATÓRIA", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)

    # Linha 1: Casos de uso
    format_cell_content(t10.cell(1, 0), [
        ("Casos de uso (mín. 3)", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t10.cell(1, 1), [
        ("Foram estruturados e priorizados três casos de uso corporativos no AI Canvas:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("1. Motor Inteligente de Triagem e Análise de Crédito B2B: Extrai dados de propostas comerciais em PDF, consulta a API da Serasa Experian e aplica matriz paramétrica de alçadas. Reduz o SLA de 48h para menos de 15 minutos em 65% dos pedidos, atacando R$ 1,25M em cancelamentos por morosidade e mitigando a inadimplência de 3,4% (R$ 1,11M em PDD).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("2. Assistente de Conciliação Financeira Multicanal e Fechamento Contábil: Realiza ingestão diária de extratos OFX/CSV e relatórios de vendas, executando pareamento probabilístico (fuzzy matching). Elimina 5 dias de atraso no fechamento mensal (atingindo a meta D+2) e economiza R$ 180k/ano em horas extras e auditorias contábeis.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("3. Pré-Validador Semântico de Pedidos, Dados Fiscais (NF-e) e Roteirização de Frete: Realiza conferência cruzada entre o PDF da proposta, o catálogo oficial e as regras CIF/FOB antes da emissão da NF-e e despacho no CD Joinville. Reduz o índice de divergências fiscais de 6,8% para menos de 0,3% e estanca R$ 1,35M/ano em fretes extras e cancelamentos.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 2: Classificação por tipo de IA (Zebra)
    format_cell_content(t10.cell(2, 0), [
        ("Classificação por tipo de IA", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t10.cell(2, 1), [
        ("A classificação tecnológica adota uma arquitetura híbrida periférica complementar:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• IA Generativa (Document AI / LLM Corporativo): Aplicada na leitura, extração semântica e interpretação de propostas em PDF (Casos 1 e 3) e na redação da minuta explicativa de divergências da DRE (Caso 2). Justificativa: flexibilidade no tratamento de documentos não estruturados.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• IA Preditiva / Estatística (Scoring & Clustering): Empregada no cálculo do escore preditivo de inadimplência combinando histórico do ERP e birôs externos, bem como na identificação de anomalias contábeis. Justificativa: precisão analítica e mitigação de risco financeiro.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Regras Tradicionais / Heurísticas: Matriz determinística de alçadas de crédito e tabelas oficiais de fretes homologados do CD Joinville, garantindo conformidade operacional estrita.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # Linha 3: Supervisão Humana
    format_cell_content(t10.cell(3, 0), [
        ("Supervisão humana", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t10.cell(3, 1), [
        ("Diretrizes Mandatórias de Supervisão Humana (Human-in-the-Loop):", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("1. Aprovação de Crédito de Maior Porte: Pedidos acima de R$ 80.000,00 ou clientes com score intermediário/restrições exigem aprovação formal em 1 clique pelo Gerente Financeiro, que recebe o dossiê analítico estruturado pela IA. Decisões 100% autônomas de recusa ou concessão de alto valor são vedadas.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("2. Exceções Fiscais e Divergências: Havendo inconsistência entre a proposta e a SEFAZ ou conflito de frete CIF/FOB, o sistema retém o pedido em quarentena com alerta visual para ajuste pelo analista humano.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("3. Conformidade Legal: O desenho atende expressamente ao Artigo 20 da LGPD (Lei 13.709/2018), assegurando o direito de revisão humana para decisões baseadas em tratamento automatizado de dados.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 13. TABELA 11: ROTA 0 - ETAPA 2 (Priorização & Mudança)
    # -------------------------------------------------------------
    print("Diagramando Tabela 11 (Priorização & ADKAR)...")
    t11 = doc.tables[11]
    format_table_structure(t11, col_widths=[Inches(1.8), Inches(4.5)])
    
    # Cabeçalho da Tabela 11
    format_cell_content(t11.cell(0, 0), [
        ("Etapa 2 — Priorização Baseada em Dados & Gestão de Mudança", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)
    format_cell_content(t11.cell(0, 1), [
        ("OBRIGATÓRIA", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)

    # Linha 1: Matriz Esforço x Impacto
    format_cell_content(t11.cell(1, 0), [
        ("Matriz Esforço × Impacto", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t11.cell(1, 1), [
        ("Estruturação da Matriz de Priorização 2x2 e Sequência de Rollout em Ondas:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Onda 1 (Semanas 1 a 4) — Ganhos Rápidos (Quick Win): Caso 3 (Pré-Validador Fiscal & Logístico). Baixo esforço de integração (não altera o código do ERP legado, atuando como middleware em Python) e alto impacto financeiro imediato (ataca R$ 1,35M/ano de perdas em fretes e cancelamentos).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Onda 2 (Semanas 5 a 8) — Controladoria e Visibilidade: Caso 2 (Conciliador Contábil Multicanal). Médio esforço analítico (ingestão de OFX/CSV e matching probabilístico) e alto retorno executivo, encurtando o fechamento para D+2 e economizando R$ 180k/ano.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Onda 3 (Semanas 9 a 12) — Aposta Estratégica (Major Project): Caso 1 (Motor Inteligente de Crédito B2B). Maior esforço de integração com birô externo (Serasa) e altíssimo impacto de receita (destrava vendas B2B e recupera R$ 1,43M/ano).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Armadilha Evitada (Time Sink): Vetada expressamente a substituição do ERP legado, o que custaria mais de R$ 2 milhões e paralisaria as operações por 12 a 18 meses.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 2: Métricas de sucesso (Zebra)
    format_cell_content(t11.cell(2, 0), [
        ("Métricas de sucesso", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t11.cell(2, 1), [
        ("Painel de Métricas Executivas e OKRs Consolidados (Horizonte de 6 Meses):", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Retorno Financeiro Consolidado: Recuperação projetada de R$ 2.501.000,00/ano em margem operacional líquida com investimento de R$ 250k no primeiro ano (ROI de 9x e Payback em 1,2 meses).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• SLA de Faturamento e Crédito: Redução do Lead Time total do pedido de 5 dias úteis (40h úteis) para menos de 2 horas (com 65% em Fast-Track < 15 min).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Fechamento Contábil Mensal: Redução de 7 dias úteis para 2 dias úteis (meta D+2 cumprida).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Conformidade Fiscal: Redução no índice de divergências de notas fiscais de 6,8% para menos de 0,5% das emissões.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Custos com Fretes Extras e Reentregas: Redução de 2,8% para menos de 1,0% da receita bruta.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # Linha 3: Plano de mudança ADKAR
    format_cell_content(t11.cell(3, 0), [
        ("Plano de mudança", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t11.cell(3, 1), [
        ("Plano de Gestão de Mudanças Organizacionais (Framework ADKAR para 280 Colaboradores):", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Awareness (Conscientização): Reunião geral de alinhamento com a CEO demonstrando abertamente o impacto dos R$ 3,89M de perdas e reforçando que a IA visa eliminar o trabalho manual repetitivo, não reduzir postos de trabalho.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Desire (Engajamento): Compromisso executivo de requalificação profissional (reskilling) dos assistentes e eliminação de sobrejornadas desgastantes de fechamento até tarde da noite.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Knowledge (Capacitação): Trilha prática de engenharia de prompts financeiros, interpretação de relatórios e operação dos validadores com turmas de até 15 profissionais.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Ability (Sustentação): Criação da Rede de 5 Campeões de IA locais em Finanças e no CD Joinville, com suporte em tempo real e ambiente seguro de testes (Sandbox).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Reinforcement (Reforço): Reconhecimento trimestral de colaboradores inovadores e atrelamento da redução do fechamento para D+2 às metas de participação nos lucros (PLR).", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 14. TABELA 12: ROTA 0 - ETAPA 3 (Governança & LGPD)
    # -------------------------------------------------------------
    print("Diagramando Tabela 12 (Governança & LGPD)...")
    t12 = doc.tables[12]
    format_table_structure(t12, col_widths=[Inches(1.8), Inches(4.5)])
    
    # Cabeçalho da Tabela 12
    format_cell_content(t12.cell(0, 0), [
        ("Etapa 3 — Política de Governança, Ética e Conformidade", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)
    format_cell_content(t12.cell(0, 1), [
        ("OBRIGATÓRIA", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)

    # Linha 1: Política de IA Responsável
    format_cell_content(t12.cell(1, 0), [
        ("Política de IA Responsável", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t12.cell(1, 1), [
        ("Política Corporativa de IA Responsável e Classificação em 4 Níveis:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Nível 1 (Dados Públicos): Fichas técnicas de produtos, catálogo e normas NR-17 -> Liberado em qualquer ferramenta.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Nível 2 (Dados Internos): Manuais de processos e procedimentos gerais -> Liberado com cautela e sem identificação institucional.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Nível 3 (Dados Confidenciais): DRE, margens brutas, tabelas de fretes e estratégias B2B -> Proibido em ferramentas gratuitas; permitido unicamente em instâncias corporativas pagas com cláusula de Zero Data Retention.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Nível 4 (Dados Restritos / LGPD): Salários, dados pessoais de colaboradores, feedbacks de saída e CPFs -> Proibido em formato bruto em qualquer IA externa; requer aplicação do Protocolo P4S de anonimização prévia.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Protocolo P4S de 4 Passos: 1. Identificar dados pessoais (PII); 2. Substituir por identificadores genéricos ([Colaborador_A], [Cliente_X]); 3. Normalizar grandezas monetárias em índices base 100; 4. Revisão visual antes do disparo do prompt.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 2: Riscos e LGPD (Zebra)
    format_cell_content(t12.cell(2, 0), [
        ("Riscos e LGPD", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t12.cell(2, 1), [
        ("Mapeamento de Riscos e Diretrizes de Conformidade LGPD:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Risco de Vazamento de Segredos Comerciais: Proibição expressa de inserção de dados contábeis reais em chats abertos (ex: ChatGPT gratuito), cujos termos de uso utilizam prompts para treinamento público de modelos.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Risco de Alucinação em Dados Fiscais e Contábeis: Vedada a aceitação cega de cálculos matemáticos emitidos por modelos de linguagem. Operações contábeis devem ser auditadas deterministicamente em planilhas ou scripts Python.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Princípio da Responsabilidade do Autor: A IA é copiloto; o profissional que valida e submete relatórios ou informações fiscais é o único responsável legal e administrativo pela precisão do conteúdo.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # Linha 3: Comitê e Auditoria
    format_cell_content(t12.cell(3, 0), [
        ("Comitê e auditoria", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t12.cell(3, 1), [
        ("Estrutura do Comitê de Governança de IA e Sanções:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Composição Multidisciplinar: Encarregado de Proteção de Dados (DPO/Jurídico), Gestor de TI & CISO, Gerente Financeiro/Controladoria e Coordenador de Operações do CD Joinville.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Canal Formal de Homologação: Nenhuma ferramenta ou extensão de IA pode ser utilizada sem parecer favorável prévio via ia.governanca@taranisblack.com.br.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Regime Disciplinar: Descumprimentos sujeitam o infrator a advertência, suspensão e demissão por justa causa (Art. 482 da CLT, alíneas a, g e h), além de responsabilização civil por perdas e danos.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 15. TABELA 13: CABEÇALHO PARTE 2 - ROTA 4
    # -------------------------------------------------------------
    print("Diagramando Tabela 13 (Header Rota 4)...")
    t13 = doc.tables[13]
    format_table_structure(t13)
    format_cell_content(t13.cell(0, 0), [
        ("PARTE 2 — ESPECIALIZAÇÃO: IA PARA FINANÇAS E OPERAÇÕES", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 16. TABELA 14: ROTA 4 - ETAPA 1 (SIPOC & Ishikawa 6M)
    # -------------------------------------------------------------
    print("Diagramando Tabela 14 (SIPOC & Ishikawa)...")
    t14 = doc.tables[14]
    format_table_structure(t14, col_widths=[Inches(1.8), Inches(4.5)])
    
    # Cabeçalho da Tabela 14
    format_cell_content(t14.cell(0, 0), [
        ("Etapa 1 — Mapeamento Lean & Diagnóstico de Gargalos (SIPOC & Ishikawa)", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)
    format_cell_content(t14.cell(0, 1), [
        ("OBRIGATÓRIA", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)

    # Linha 1: Matriz SIPOC
    format_cell_content(t14.cell(1, 0), [
        ("Matriz SIPOC", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t14.cell(1, 1), [
        ("Matriz Lean SIPOC do Macroprocesso de Faturamento e Expedição B2B:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Suppliers (Fornecedores): Consultores Comerciais B2B, Clientes Compradores, Birô Serasa Experian, Gerência Financeira, SEFAZ e Transportadoras Homologadas.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Inputs (Entradas): Propostas em PDF assinadas, cadastros de CNPJ/IE, histórico de compras no ERP legado, tabela de preços e matriz de fretes CIF/FOB.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Process (Etapas As-Is): 1. Envio despadronizado de e-mail ao financeiro (>40/dia em pico); 2. Triagem manual e consulta a 3 telas (40 min/pedido); 3. Solicitação de alçada por e-mail; 4. Retenção em fila por 24h a 48h úteis; 5. Digitação manual de NF-e e envio manual ao CD Joinville.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Outputs (Saídas): Ordens de venda gravadas no ERP, dossiês de crédito compilados, autorizações de faturamento, DANFE/XML de NF-e, boletos bancários e Minutas de Embarque (CT-e).", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Customers (Clientes): Comprador B2B corporativo, Equipe do CD Joinville, Transportadoras, Faturamento e Controladoria.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Eficiência de Fluxo (PCE): Touch Time ativo de apenas 1,5 horas frente ao Lead Time de 40 horas úteis (5 dias úteis). Eficiência de Ciclo (PCE) de 3,75%, revelando que 96,25% do tempo é desperdício em filas.", 9, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 2: Diagrama de Ishikawa (Zebra)
    format_cell_content(t14.cell(2, 0), [
        ("Diagrama de Ishikawa", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t14.cell(2, 1), [
        ("Diagrama de Ishikawa nos 6M (Causas dos Atrasos e das Perdas de R$ 3,89M):", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Método: Fluxo de aprovação dependente de comunicação informal por e-mail; inexistência de esteira de alçada automática; dependência de 3 planilhas locais desconectadas (Controle_Limites, Preços e Fretes); regras CIF/FOB não checadas antes da venda.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Máquina / Tecnologia: ERP legado sem APIs modernas de integração; ausência de Document AI / OCR para leitura automática de PDFs; falta de validação sintática e fiscal pré-emissão de NF-e.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Mão de Obra: Assistentes sobrecarregados com digitação mecânica e sujeitos a burnout nos fechamentos; centralização de aprovações rotineiras na gerência financeira; atritos de comunicação entre time comercial (SP) e CD (Joinville/SC).", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Material: Propostas comerciais enviadas com campos incompletos; divergência de códigos SKU entre tabelas de vendas e o ERP; comprovantes de endereço desatualizados.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Medição: Falta de monitoramento de SLAs por etapa em tempo real; ausência de conciliação bancária contínua; diretoria informada sobre atrasos somente no encerramento contábil.", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Meio Ambiente: Crescimento acelerado de 35% ao ano superando a maturidade operacional dos sistemas; concentração de mais de 45% do faturamento nos últimos dias do mês comercial.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # Linha 3: Top 3 causas críticas
    format_cell_content(t14.cell(3, 0), [
        ("Top 3 causas críticas", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t14.cell(3, 1), [
        ("Top 3 Causas Críticas Estruturais (Metodologia dos 5 Porquês):", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("1. Falta de Conciliação Contábil Contínua por Fuzzy Matching: Causa o atraso crônico de 5 dias no fechamento mensal e gera R$ 180k/ano em horas extras, pois analistas conferem manualmente milhares de lançamentos contra extratos e relatórios de vendas.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("2. Ausência de Motor Paramétrico de Crédito B2B com Fast-Track: Provoca a retenção de 48h na caixa de e-mail do gerente, resultando em R$ 1,25M/ano em compras canceladas por morosidade e R$ 1,11M em perdas por inadimplência devido a análises apressadas sob pressão.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("3. Digitação Manual de Propostas para Emissão de NF-e sem Validação Prévia: Causa 6,8% de divergências fiscais e um estouro de R$ 1,875M em fretes duplicados, multas e custos logísticos no CD Joinville/SC decorrentes de erros em acabamentos de produto e regras CIF/FOB.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 4: Recomendação de Intervenção Prioritária (Zebra)
    format_cell_content(t14.cell(4, 0), [
        ("Recomendação de intervenção prioritária", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t14.cell(4, 1), [
        ("Recomendação de Intervenção Prioritária:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("A intervenção prioritária imediata é a implantação do Pré-Validador Fiscal & Logístico (Caso 3) na Onda 1 (4 semanas).", 9, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("Justificativa Técnica e Financeira: Esta solução atua como um middleware leve em Python que intercepta as propostas em PDF e valida códigos SKU, condições de pagamento e regras de frete CIF/FOB antes que o pedido chegue à SEFAZ ou ao CD Joinville. Não exige alterações estruturais no ERP legado, tem baixo custo de desenvolvimento (R$ 50k) e estanca de imediato R$ 1,35 milhão por ano em fretes de emergência e cancelamentos fiscais, trazendo retorno visível já no primeiro mês de operação.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 17. TABELA 15: ROTA 4 - ETAPA 3 (Dashboard & Análise Preditiva)
    # -------------------------------------------------------------
    print("Diagramando Tabela 15 (DRE & Preditivo)...")
    t15 = doc.tables[15]
    format_table_structure(t15, col_widths=[Inches(1.8), Inches(4.5)])
    
    # Cabeçalho da Tabela 15
    format_cell_content(t15.cell(0, 0), [
        ("Etapa 3 — Dashboard Inteligente & Análise Preditiva Financeira", 10, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)
    format_cell_content(t15.cell(0, 1), [
        ("OPCIONAL (CONCLUÍDA)", 9.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.RIGHT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None)

    # Linha 1: Prompts Especializados
    format_cell_content(t15.cell(1, 0), [
        ("Prompts de processamento da planilha financeira", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t15.cell(1, 1), [
        ("Prompts Especializados de Engenharia Financeira Utilizados:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("Prompt 1 (Auditoria DRE e Desvios de Margem): 'Atue como Controller. Analise a planilha 05_Financas_Orcado_vs_Realizado.xlsx. Calcule a variância nominal em R$ e percentual de cada conta da DRE Trimestral. Destaque quais linhas de custo excederam o orçado anual em mais de 15% e correlacione com os desvios de EBITDA. Apresente memória de cálculo.'", 8.5, False, True, RGB_TEXT_MUTED, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("Prompt 2 (Diagnóstico de Fretes e Quebra de EBITDA): 'Cruze os dados da aba Gargalos_Operacionais_Custos com a DRE. Calcule o impacto financeiro consolidado de fretes duplicados, multas por divergência de NF-e e perdas com PDD sobre a receita líquida. Indique a porcentagem da perda de EBITDA atribuível unicamente a falhas de faturamento e logística.'", 8.5, False, True, RGB_TEXT_MUTED, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("Prompt 3 (Modelagem Preditiva Pós-IA): 'Projete o resultado operacional dos próximos 4 trimestres considerando a redução de 65% nos cancelamentos, queda de 70% nas despesas com fretes extras e redução da inadimplência para 1,5%. Calcule o novo EBITDA projetado e o Payback para um investimento de R$ 250k.'", 8.5, False, True, RGB_TEXT_MUTED, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 2: Dashboard / Relatório DRE (Zebra)
    format_cell_content(t15.cell(2, 0), [
        ("Dashboard / relatório gerado", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t15.cell(2, 1), [
        ("Síntese do Demonstrativo de Resultados do Exercício (DRE) Auditado:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Receita Bruta Total: R$ 48.500.000,00 (Orçado: R$ 48.600.000,00 | Variação: -0,2%)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Canal Corporativo B2B (70%): R$ 33.600.000,00 (Orçado: R$ 34.000.000,00 | Retenção por crédito)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Canal Vendas Diretas pelo Site (30%): R$ 14.900.000,00 (Orçado: R$ 14.600.000,00 | +2,1%)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Cancelamentos / Devoluções: R$ 1.235.000,00 (Orçado: R$ 560.000,00 | Aumento crítico de +120,5%)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Receita Líquida Operacional: R$ 39.020.000,00 (Orçado: R$ 39.778.000,00 | Desvio: -1,9%)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Lucro Bruto Operacional: R$ 18.430.000,00 (Margem Bruta realizada de 47,2% vs 49,5% orçada)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Despesas Operacionais (OPEX): R$ 12.660.000,00 (Orçado: R$ 9.850.000,00 | Estouro de +28,5%)", 9, False, False, RGB_TEXT_DARK, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• EBITDA Operacional Realizado: R$ 5.770.000,00 (Orçado: R$ 9.848.000,00 | Perda de -41,4% / -R$ 4,08M)", 9, True, False, RGB_ALERT_RED, 1.5, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Lucro Líquido Realizado: R$ 3.108.600,00 (Orçado: R$ 5.965.080,00 | Redução de -47,9%)", 9, True, False, RGB_ALERT_RED, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # Linha 3: Anomalias identificadas
    format_cell_content(t15.cell(3, 0), [
        ("Anomalias identificadas", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t15.cell(3, 1), [
        ("Anomalias Financeiras Críticas Diagnosticadas na Operação:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("1. Explosão de Despesas com Fretes e Reentregas: O total somado de fretes do CD Joinville e multas por divergência atingiu R$ 4.465.000,00 (9,2% da receita bruta), representando um estouro de R$ 1.875.000,00 acima do planejado (responsável por 46% de toda a quebra de EBITDA da empresa).", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("2. Aumento Agressivo da PDD / Inadimplência B2B: Saltou de R$ 440.000,00 para R$ 1.110.000,00 (+152%), elevando o índice de inadimplência para 3,4% da receita decorrente da falta de motor de crédito.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("3. Descompasso de Margem na Linha SmartDesk: Menor margem bruta entre os móveis corporativos (38,5%) e queda de R$ 550 mil no faturamento anual em razão da retenção de propostas de alto valor na esteira de crédito.", 9, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # Linha 4: Projeção Preditiva (Zebra)
    format_cell_content(t15.cell(4, 0), [
        ("Projeção para o próximo trimestre", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t15.cell(4, 1), [
        ("Projeção Preditiva de Recuperação Financeira Pós-Implementação das 3 Ondas de IA:", 9.5, True, False, RGB_PRIMARY_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Projeção de EBITDA: Elevação de R$ 5.770.000,00 para R$ 8.271.000,00 ao ano (+43,3%), recuperando mais de R$ 2,50 milhões em margem operacional e recompondo a margem EBITDA para 21,2%.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Projeção de Lucro Líquido: Salto de R$ 3.108.600,00 para R$ 4.759.000,00 (+53,1%), restabelecendo a rentabilidade da companhia.", 9, False, False, RGB_TEXT_DARK, 2, WD_ALIGN_PARAGRAPH.LEFT),
        ("• Retorno do Investimento: O aporte de R$ 250 mil é amortizado integralmente em 1,2 meses (36 dias de faturamento com perdas estancadas), com ROI de 9 vezes o valor investido.", 9, True, False, RGB_SUCCESS_GREEN, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_ZEBRA, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 18. TABELA 16: CABEÇALHO ANEXO DE EVIDÊNCIAS
    # -------------------------------------------------------------
    print("Diagramando Tabela 16 (Header Anexo)...")
    t16 = doc.tables[16]
    format_table_structure(t16)
    format_cell_content(t16.cell(0, 0), [
        ("ANEXO DE EVIDÊNCIAS E ARTEFATOS CONSTRUÍDOS", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 19. TABELA 17: CALLOUT ORIENTAÇÃO DO ANEXO
    # -------------------------------------------------------------
    print("Diagramando Tabela 17 (Callout Anexo)...")
    t17 = doc.tables[17]
    format_table_structure(t17)
    set_callout_style(t17.cell(0, 0),
        "Orientação: Lista de evidências e artefatos técnicos desenvolvidos e homologados para avaliação."
    )

    # -------------------------------------------------------------
    # 20. TABELA 18: TABELA DE EVIDÊNCIAS (5 colunas)
    # -------------------------------------------------------------
    print("Diagramando Tabela 18 (Matriz de Evidências)...")
    t18 = doc.tables[18]
    evid_widths = [Inches(1.4), Inches(1.9), Inches(1.4), Inches(0.8), Inches(0.8)]
    format_table_structure(t18, col_widths=evid_widths)
    
    # Cabeçalho da Tabela 18
    headers_t18 = [
        ("Artefato", WD_ALIGN_PARAGRAPH.LEFT),
        ("Descrição", WD_ALIGN_PARAGRAPH.LEFT),
        ("Link no Repositório", WD_ALIGN_PARAGRAPH.LEFT),
        ("Status", WD_ALIGN_PARAGRAPH.CENTER),
        ("Nota de Uso", WD_ALIGN_PARAGRAPH.LEFT)
    ]
    for c_idx, (h_text, h_align) in enumerate(headers_t18):
        format_cell_content(t18.rows[0].cells[c_idx], [
            (h_text, 9, True, False, RGB_WHITE, 1, h_align)
        ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(100, 100, 120, 120))
        
    # Dados da Tabela 18
    evidencias_rows = [
        ("AI Canvas Corporativo & Casos de Uso", 
         "Mapeamento dos 9 blocos estratégicos e detalhamento dos 3 casos de uso da Taranis Black.", 
         "./02_rota_0_estrategia/01_ai_canvas_taranis_black.md", 
         "Homologado", 
         "Base estratégica do projeto e dimensionamento de ROI"),
        ("Matriz Esforço x Impacto & ADKAR", 
         "Priorização em ondas, definição de OKRs de 6 meses e plano de mudanças para 280 colaboradores.", 
         "./02_rota_0_estrategia/02_matriz_esforco_impacto_metricas_mudancas.md", 
         "Homologado", 
         "Roteiro de implantação tática e governança cultural"),
        ("Política Corporativa de IA & LGPD", 
         "Diretrizes de uso responsável, 4 níveis de sensibilidade de dados e protocolo P4S de sanitização.", 
         "./02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md", 
         "Homologado", 
         "Regulamentação corporativa de segurança da informação"),
        ("Mapeamento SIPOC, Ishikawa & DRE", 
         "Matriz Lean As-Is/To-Be, causas 6M, 5 Porquês, 5W2H e análise financeira DRE Orçado vs Realizado.", 
         "./03_rota_4_financas_operacoes/", 
         "Homologado", 
         "Dossiê completo de especialização da Rota 4")
    ]
    
    for r_idx, (art, desc, link, status, nota) in enumerate(evidencias_rows, start=1):
        row = t18.rows[r_idx]
        bg_row = HEX_WHITE if r_idx % 2 != 0 else HEX_BG_ZEBRA
        
        # Coluna 0: Artefato
        format_cell_content(row.cells[0], [(art, 8.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)], bg_hex=bg_row, border_color=HEX_BORDER_SUBTLE, padding=(80, 80, 100, 100))
        # Coluna 1: Descrição
        format_cell_content(row.cells[1], [(desc, 8.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)], bg_hex=bg_row, border_color=HEX_BORDER_SUBTLE, padding=(80, 80, 100, 100))
        # Coluna 2: Link
        format_cell_content(row.cells[2], [(link, 8, False, False, RGB_SECONDARY_SLATE, 1, WD_ALIGN_PARAGRAPH.LEFT)], bg_hex=bg_row, border_color=HEX_BORDER_SUBTLE, padding=(80, 80, 100, 100))
        # Coluna 3: Status
        format_cell_content(row.cells[3], [(status, 8.5, True, False, RGB_SUCCESS_GREEN, 1, WD_ALIGN_PARAGRAPH.CENTER)], bg_hex=bg_row, border_color=HEX_BORDER_SUBTLE, padding=(80, 80, 100, 100))
        # Coluna 4: Nota de uso
        format_cell_content(row.cells[4], [(nota, 8.5, False, False, RGB_TEXT_MUTED, 1, WD_ALIGN_PARAGRAPH.LEFT)], bg_hex=bg_row, border_color=HEX_BORDER_SUBTLE, padding=(80, 80, 100, 100))

    # -------------------------------------------------------------
    # 21. TABELA 19: CABEÇALHO VÍDEO DE DEMONSTRAÇÃO
    # -------------------------------------------------------------
    print("Diagramando Tabela 19 (Header Vídeo)...")
    t19 = doc.tables[19]
    format_table_structure(t19)
    format_cell_content(t19.cell(0, 0), [
        ("VÍDEO DE DEMONSTRAÇÃO (OPCIONAL)", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 22. TABELA 20: CALLOUT ORIENTAÇÃO DO VÍDEO
    # -------------------------------------------------------------
    print("Diagramando Tabela 20 (Callout Vídeo)...")
    t20 = doc.tables[20]
    format_table_structure(t20)
    set_callout_style(t20.cell(0, 0),
        "Formatos aceitos: YouTube (não listado), Loom ou Google Drive. Duração: até 5 minutos."
    )

    # -------------------------------------------------------------
    # 23. TABELA 21: LINK DO VÍDEO
    # -------------------------------------------------------------
    print("Diagramando Tabela 21 (Link do Vídeo)...")
    t21 = doc.tables[21]
    format_table_structure(t21, col_widths=[Inches(1.8), Inches(4.5)])
    format_cell_content(t21.cell(0, 0), [
        ("Link do vídeo", 9.5, True, False, RGB_PRIMARY_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_BG_LABEL, border_color=HEX_BORDER_SUBTLE)
    format_cell_content(t21.cell(0, 1), [
        ("Projeto integralmente documentado com evidências textuais, métricas DRE auditadas e demonstrativos técnicos em anexo.", 9.5, False, True, RGB_TEXT_MUTED, 1, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_WHITE, border_color=HEX_BORDER_SUBTLE)

    # -------------------------------------------------------------
    # 24. TABELA 22: CABEÇALHO PROCEDIMENTO DE SUBMISSÃO
    # -------------------------------------------------------------
    print("Diagramando Tabela 22 (Header Submissão)...")
    t22 = doc.tables[22]
    format_table_structure(t22)
    format_cell_content(t22.cell(0, 0), [
        ("PROCEDIMENTO DE SUBMISSÃO OFICIAL", 11, True, False, RGB_WHITE, 2, WD_ALIGN_PARAGRAPH.LEFT)
    ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(120, 120, 160, 160))

    # -------------------------------------------------------------
    # 25. TABELA 23: INSTRUÇÕES DE SUBMISSÃO
    # -------------------------------------------------------------
    print("Diagramando Tabela 23 (Instruções de Submissão)...")
    t23 = doc.tables[23]
    format_table_structure(t23, col_widths=[Inches(0.5), Inches(5.8)])
    
    submissao_passos = [
        ("1", "Certifique-se de que este documento está compartilhado no Google Drive com permissão pública: 'Qualquer pessoa com o link pode ler'."),
        ("2", "Copie o link público gerado pelo Google Docs."),
        ("3", "Acesse a plataforma da Alura, navegue até a atividade do challenge e cole o link no campo de envio."),
        ("4", "Apenas o link do Google Docs é aceito na submissão. Não envie arquivos PDF ou anexos locais.")
    ]
    for idx, (num, txt) in enumerate(submissao_passos):
        bg_col1 = HEX_WHITE if idx % 2 == 0 else HEX_BG_ZEBRA
        # Coluna 0: Número do Passo
        format_cell_content(t23.cell(idx, 0), [
            (num, 10.5, True, False, RGB_WHITE, 1, WD_ALIGN_PARAGRAPH.CENTER)
        ], bg_hex=HEX_PRIMARY_DARK, border_color=None, padding=(100, 100, 80, 80))
        # Coluna 1: Texto de Instrução
        format_cell_content(t23.cell(idx, 1), [
            (txt, 9.5, False, False, RGB_TEXT_DARK, 1, WD_ALIGN_PARAGRAPH.LEFT)
        ], bg_hex=bg_col1, border_color=HEX_BORDER_SUBTLE, padding=(100, 100, 120, 120))

    # -------------------------------------------------------------
    # 26. SALVAMENTO E DUPLICAÇÃO DE SEGURANÇA
    # -------------------------------------------------------------
    print(f"\nSalvando documento reestruturado em: {INPUT_DOCX}...")
    doc.save(INPUT_DOCX)
    
    print(f"Salvando cópia de segurança homologada em: {BACKUP_DOCX}...")
    shutil.copyfile(INPUT_DOCX, BACKUP_DOCX)

    # -------------------------------------------------------------
    # 27. AUDITORIA QUANTITATIVA FINAL DE CONTRASTE E ZERO EMOJIS
    # -------------------------------------------------------------
    print("\n=== EXECUTANDO AUDITORIA FINAL DE CONTRASTE E ESTILO ===")
    doc_check = docx.Document(INPUT_DOCX)
    
    total_paras = len(doc_check.paragraphs)
    total_tables = len(doc_check.tables)
    emoji_count = 0
    contrast_violations = []

    # Verificar parágrafos do corpo
    for p_idx, p in enumerate(doc_check.paragraphs):
        if EMOJI_PATTERN.search(p.text):
            emoji_count += 1

    # Verificar tabelas
    for t_idx, t in enumerate(doc_check.tables):
        for r_idx, r in enumerate(t.rows):
            for c_idx, c in enumerate(r.cells):
                # Verificar background da célula
                shd_list = c._tc.xpath('.//w:shd/@w:fill')
                fill = shd_list[0].upper() if shd_list else "NONE"
                
                # Verificar runs e contraste
                for p in c.paragraphs:
                    if EMOJI_PATTERN.search(p.text):
                        emoji_count += 1
                    for run in p.runs:
                        if not run.text.strip():
                            continue
                        color_rgb = run.font.color.rgb if (run.font.color and run.font.color.rgb) else None
                        color_hex = f"{color_rgb[0]:02X}{color_rgb[1]:02X}{color_rgb[2]:02X}" if color_rgb else "000000"
                        
                        # Regra de contraste:
                        # Se fundo for escuro (1A365D ou 2B6CB0), texto DEVE ser FFFFFF
                        if fill in ["1A365D", "2B6CB0", "0F294A", "1F3864"] and color_hex != "FFFFFF":
                            contrast_violations.append((t_idx, r_idx, c_idx, fill, color_hex, run.text[:30]))
                        # Se fundo for claro (FFFFFF, F0F4F8, F7FAFC, EDF2F7), texto NÃO pode ser branco
                        if fill in ["FFFFFF", "F0F4F8", "F7FAFC", "EDF2F7", "NONE"] and color_hex in ["FFFFFF"]:
                            contrast_violations.append((t_idx, r_idx, c_idx, fill, color_hex, run.text[:30]))

    print(f"- Total de parágrafos no documento: {total_paras}")
    print(f"- Total de tabelas configuradas: {total_tables}")
    print(f"- Violações de contraste detectadas: {len(contrast_violations)}")
    if contrast_violations:
        for v in contrast_violations[:5]:
            print(f"  [ALERTA CONTRASTE] Tabela {v[0]} L{v[1]} C{v[2]}: Fundo={v[3]}, Texto={v[4]} ('{v[5]}')")
    else:
        print("[APROVADO] 100% de contraste acessível em todas as células e textos!")
        
    print(f"- Total de emojis encontrados: {emoji_count}")
    if emoji_count == 0:
        print("[APROVADO] ZERO EMOJIS! Restrição de estilo formal institucional 100% atendida.")
    else:
        print(f"[FALHA] Foram encontrados {emoji_count} emojis.")

if __name__ == "__main__":
    main()
