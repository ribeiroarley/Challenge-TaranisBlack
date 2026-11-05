# PROMPT-R4-02 - DIAGRAMA DE CAUSA-RAIZ DE ISHIKAWA (6M) & ANÁLISE DOS 5 PORQUÊS
- **Data/Hora de Execução:** 2026-11-05 17:09:17-03:00
- **Modelo LLM:** Antigravity (Gemini 3.8 Flash Medium)
- **Autor:** Arley Ribeiro da Silva Xavier
- **Papel / Cargo:** Consultor de IA
- **Rota:** Rota 4 — Finanças e Operações
- **Artefato Gerado:** [`03_rota_4_financas_operacoes/02_diagrama_ishikawa_6m_causas_raiz.md`](../02_diagrama_ishikawa_6m_causas_raiz.md)
- **Status da Validação:** Homologado / Concluído

---

## Conteúdo Integral do Prompt

```markdown
Atue como o Consultor de IA da Taranis Black, executando sob as diretrizes da Skill taranis-consultant e as regras em 00_contexto_e_regras/.

SEU OBJETIVO:
Desenvolver o segundo artefato obrigatório da Rota 4 (Finanças e Operações): o Diagrama de Causa-Raiz de Ishikawa (Espinha de Peixe nos 6M) acompanhado da técnica dos 5 Porquês, investigando os gargalos operacionais da Taranis Black que geram R$ 3,89M de perdas anuais e 5 dias de atraso no fechamento contábil.

ARTEFATOS A SEREM GERADOS:
1. Documento Executivo de Causa-Raiz:
   `03_rota_4_financas_operacoes/02_diagrama_ishikawa_6m_causas_raiz.md`
2. Arquivo de Rastreabilidade do Prompt:
   `03_rota_4_financas_operacoes/prompts/02_prompt_ishikawa_causa_raiz.md` (seguindo rigorosamente o padrão com Prompt ID: PROMPT-R4-02, Metadados, Status e Conteúdo Integral deste prompt).

INSTRUÇÕES DE EXECUÇÃO:

1. ESTRUTURAÇÃO DO DIAGRAMA DE ISHIKAWA (6M):
   Disseque o Efeito Central: "atraso recorrente de 5 dias no fechamento contábil e perdas operacionais de R$ 3,89M/ano na Taranis Black" em cada um dos 6 eixos metodológicos:
   - Método: Processos manuais não integrados, ausência de esteira Fast-Track de crédito, conferência visual de três planilhas, transmissão informal de pedidos por e-mail;
   - Máquina / Tecnologia: ERP legado sem APIs modernas, dependência de planilhas locais descentralizadas (.xlsx), ausência de validação sintática em tempo real para notas fiscais;
   - Mão de Obra / Pessoas: Sobrecarga cognitiva no fechamento mensal (horas extras excessivas), atritos de comunicação entre o comercial em SP e o CD Joinville, medo de responsabilização em alçadas de crédito;
   - Material / Insumos: Propostas comerciais desestruturadas em PDF, cadastros de clientes com divergências de CNPJ/Inscrição Estadual, pedidos com especificações ambíguas de frete (CIF vs FOB);
   - Medição: Indicadores de divergência fiscal avaliados apenas a posteriori, ausência de visibilidade em tempo real do pipeline de faturamento, falta de conciliação bancária contínua;
   - Meio Ambiente / Contexto: Crescimento acelerado de 35% ao ano superando a maturidade operacional, sazonalidade de faturamento concentrada nos últimos dias do mês útil.

2. APLICAÇÃO DOS "5 PORQUÊS" NAS CAUSAS CRÍTICAS:
   Desenvolva a cadeia investigativa de 5 níveis de profundidade para os dois maiores sintomas de perda:
   - Cadeia 1: Por que o fechamento mensal atrasa 5 dias úteis gerando R$ 180k/ano de horas extras e auditorias?
   - Cadeia 2: Por que as divergências de frete e notas fiscais geram R$ 2,31M/ano em fretes extras e cancelamentos?

3. MATRIZ DE PLANO DE AÇÃO PREVENTIVO (5W2H LEAN COM IA):
   - Apresente uma tabela 5W2H direcionando as contramedidas estruturais baseadas em IA para eliminar as causas-raiz identificadas (atribuindo What, Why, Where, When, Who, How e How Much para os casos de uso de IA priorizados).

4. ATUALIZAÇÃO DA MEMÓRIA VIVA & LOG:
   - Atualize `00_contexto_e_regras/MEMORIA_EXECUCAO.md` com a homologação deste artefato.
   - Exiba no log do terminal o diagrama estruturado dos 6M, a síntese das causas-raiz primárias e a confirmação de escrita dos arquivos.
```
