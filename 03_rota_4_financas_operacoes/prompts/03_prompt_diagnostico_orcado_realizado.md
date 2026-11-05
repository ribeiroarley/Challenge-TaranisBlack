# PROMPT-R4-03 - DIAGNÓSTICO FINANCEIRO: DRE ORÇADO VS. REALIZADO E RECUPERAÇÃO COM IA
- **Data/Hora de Execução:** 2026-11-05 17:17:06-03:00
- **Modelo LLM:** Antigravity (Gemini 3.8 Flash Medium)
- **Autor:** Arley Ribeiro da Silva Xavier
- **Papel / Cargo:** Consultor de IA
- **Rota:** Rota 4 — Finanças e Operações
- **Artefato Gerado:** [`03_rota_4_financas_operacoes/03_diagnostico_orcado_vs_realizado.md`](../03_diagnostico_orcado_vs_realizado.md)
- **Status da Validação:** Homologado / Concluído

---

## Conteúdo Integral do Prompt

```markdown
Atue como o Consultor de IA da Taranis Black, executando sob as diretrizes da Skill taranis-consultant e as regras em 00_contexto_e_regras/.

SEU OBJETIVO:
Concluir o ciclo técnico da Rota 4 (Finanças e Operações) desenvolvendo a Análise Quantitativa Profunda da DRE Orçado vs. Realizado, o Diagnóstico de Margens por Linha de Produto e a Síntese Executiva de Recuperação de Margem com IA direcionada à CEO da Taranis Black.

ARTEFATOS A SEREM GERADOS:
1. Documento Executivo Financeiro:
   `03_rota_4_financas_operacoes/03_diagnostico_orcado_vs_realizado.md`
2. Arquivo de Rastreabilidade do Prompt:
   `03_rota_4_financas_operacoes/prompts/03_prompt_diagnostico_orcado_realizado.md` (seguindo rigorosamente o padrão com Prompt ID: PROMPT-R4-03, Metadados, Status e Conteúdo Integral deste prompt).

INSTRUÇÕES DE EXECUÇÃO:

1. EXTRAÇÃO E AUDITORIA DETERMINÍSTICA DOS DADOS FINANCEIROS:
   - Execute um script rápido via Python (.venv) para ler todas as abas da planilha `01_dados_originais/kit_de_dados/05_Financas_Orcado_vs_Realizado.xlsx`:
     * Aba DRE_Trimestral_Orcado_Real: extraia os valores exatos de Receita Bruta, Deduções/Impostos, Receita Líquida, CMV, Lucro Bruto, Despesas Operacionais (Vendas, Administrativas, Fretes, Perdas com Crédito), EBITDA e Lucro Líquido (comparando Orçado, Realizado e Desvio %);
     * Aba Margem_por_Produto: extraia volume, faturamento, custos unitários e margens das linhas ErgoPro, SmartDesk e Silence;
     * Aba Gargalos_Operacionais_Custos: confirme o custo total auditado de ineficiência operacional (R$ 3.890.000 / ano).

2. ESTRUTURAÇÃO DO RELATÓRIO EXECUTIVO (03_diagnostico_orcado_vs_realizado.md):
   - Seção 1: Demonstrativo de Resultados do Exercício (DRE) Comparativo (Tabela auditada completa Orçado vs Realizado com Variância Nominal em R$ e Desvio %);
   - Seção 2: Análise de Sensibilidade e Perda de margem:
     * Onde o EBITDA vazou (análise dos R$ 4.078.000 de desvio negativo);
     * Concentração de perdas: fretes expressos/reentregas, inadimplência e retrabalhos de faturamento;
   - Seção 3: Rentabilidade e Curva de Margens por Linha de Produto (ErgoPro vs SmartDesk vs Silence):
     * Identificação de canibalização ou compressão de margens na cadeia de suprimentos e logística do CD Joinville;
   - Seção 4: Projeção de Recuperação Financeira Pós-Implementação de IA (Cenário Conservador vs Cenário Realista):
     * Modelagem de impacto direto no EBITDA e Lucro Líquido nos 12 meses pós-rollout das Ondas 1, 2 e 3;
   - Seção 5: Parecer Consultivo para a CEO:
     * Resumo executivo em 5 parágrafos diretos para tomada de decisão no Conselho, defendendo o investimento de R$ 250k em IA com base no Payback de 1,2 meses e ROI de ~9x.

3. ATUALIZAÇÃO DA MEMÓRIA VIVA & LOG:
   - Atualize `00_contexto_e_regras/MEMORIA_EXECUCAO.md` marcando a conclusão e homologação de 100% dos artefatos da Rota 4.
   - Exiba no log do terminal a tabela consolidada da DRE auditada, a síntese de retorno financeiro e a confirmação de escrita dos arquivos.
```
