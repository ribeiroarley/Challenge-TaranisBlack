# PROMPT-R4-01 - MAPEAMENTO LEAN DO MACROPROCESSO DE PEDIDOS (MATRIZ SIPOC)
- **Data/Hora de Execução:** 2026-11-05 17:01:11-03:00
- **Modelo LLM:** Antigravity (Gemini 3.8 Flash Medium)
- **Rota:** Rota 4 — Finanças e Operações
- **Artefato Gerado:** [`03_rota_4_financas_operacoes/01_mapeamento_processo_sipoc.md`](../01_mapeamento_processo_sipoc.md)
- **Status da Validação:** Homologado / Concluído

---

## Conteúdo Integral do Prompt

```markdown
Atue como o Consultor de IA e Lean Seis Sigma da Taranis Black, executando sob as diretrizes da Skill taranis-consultant e as regras em 00_contexto_e_regras/.

SEU OBJETIVO:
Iniciar formalmente a Rota 4 (Finanças e Operações) desenvolvendo o primeiro artefato obrigatório da especialização: o Mapeamento Detalhado do Macroprocesso de Pedidos através da Matriz Lean SIPOC (Suppliers, Inputs, Process, Outputs, Customers), diagnosticando as ineficiências manuais que geram os R$ 3,89M de perdas anuais e projetando o fluxo otimizado com IA.

ARTEFATOS A SEREM GERADOS:
1. Documento Executivo SIPOC:
   `03_rota_4_financas_operacoes/01_mapeamento_processo_sipoc.md`
2. Arquivo de Rastreabilidade do Prompt:
   `03_rota_4_financas_operacoes/prompts/01_prompt_sipoc_mapeamento.md` (seguindo rigorosamente o padrão com Prompt ID: PROMPT-R4-01, Metadados, Status e Conteúdo Integral deste prompt).

INSTRUÇÕES DE EXECUÇÃO:

1. LEITURA DE INSUMOS PRIMÁRIOS:
   - Inspecione autonomamente via Python (.venv) o documento `01_dados_originais/kit_de_dados/06_Descritivo_Processo_Operacional_SIPOC.docx` e `01_dados_originais/kit_de_dados/01_Catalogo_Produtos_e_Precos_Taranis_Black.docx` para extrair as etapas reais da cadeia de valor da Taranis Black (da entrada do lead à expedição no CD Joinville e faturamento/conciliação).

2. CONSTRUÇÃO DA MATRIZ SIPOC DETALHADA:
   - Estruture a Matriz SIPOC clássica em tabela Markdown cobrindo todas as 5 etapas da esteira:
     * Fornecedores (Suppliers): Clientes B2B, Vendedores, Birôs de Crédito, SEFAZ, Transportadoras;
     * Entradas (Inputs): Propostas em PDF, dados cadastrais, regras de crédito, pedidos no ERP legado, tabela de fretes;
     * Processo (Process - As-Is): 
       Passo 1: Recepção e entrada manual de pedido;
       Passo 2: Análise de crédito e aprovação de alçadas (SLA 48h crônico);
       Passo 3: Digitação manual de NF-e e validação fiscal (6,8% de erro);
       Passo 4: Roteirização e agendamento de frete no CD Joinville (2,8% em reentregas);
       Passo 5: Faturamento, envio de boleto e conciliação bancária (5 dias de atraso mensal);
     * Saídas (Outputs): Pedido faturado, NF-e autorizada, comprovante de agendamento logístico, boletos gerados e balancete conciliado;
     * Clientes (Customers): Cliente B2B final, Contabilidade/Controladoria, Logística e Diretoria Financeira.

3. DIAGNÓSTICO DOS PONTOS DE FRICÇÃO (BOTTLENECK ANALYSIS):
   - Mapeie o tempo de ciclo atual (*Lead Time* total do pedido), tempo de processamento ativo (*Touch Time*) e eficiência de fluxo (*Process Cycle Efficiency*).
   - Destaque os 4 gargalos críticos onde há maior perda financeira (tempo de espera em e-mails, digitação manual duplicada entre planilhas e ERP, divergência cadastral e ausência de conciliação bancária automatizada).

4. DESENHO DO FLUXO TO-BE (OTIMIZADO COM IA):
   - Apresente o comparativo visual (tabela ou fluxo descritivo) entre o processo atual (*As-Is*) e o processo futuro (*To-Be*), demonstrando onde os Casos de Uso da IA (Fast-Track de Crédito, Validador Fiscal e Conciliador Multicanal) interceptam e reduzem o ciclo de 72h para menos de 2h.

5. ATUALIZAÇÃO DA MEMÓRIA VIVA & LOG:
   - Atualize `00_contexto_e_regras/MEMORIA_EXECUCAO.md` registrando a homologação do artefato da Rota 4.
   - Exiba no log do terminal o resumo da Matriz SIPOC, a tabela comparativa As-Is vs To-Be e a confirmação de gravação dos arquivos.
```
