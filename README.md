# Challenge AI for Business — Taranis Black

Projeto consultivo de Inteligência Artificial aplicada à estratégia, finanças, controladoria e operações corporativas da **Taranis Black**, desenvolvido no âmbito da Formação **AI for Business (Alura / ONE G11)**.

---

## 1. Visão Geral e Contexto da Empresa

A **Taranis Black** é uma fabricante e distribuidora brasileira de mobiliário corporativo de alta performance e ergonomia ativa (cadeiras de trabalho ErgoPro, mesas com ajuste elétrico de altura SmartDesk e cabines acústicas Silence).

* **Faturamento Anual:** R$ 48.000.000,00 (Ano Fiscal 2026).
* **Quadro de Colaboradores:** 280 profissionais.
* **Crescimento:** 35% ao ano nos últimos três exercícios.
* **Operação:** Matriz comercial em São Paulo / SP e Centro de Distribuição (CD) com montagem fabril em Joinville / SC.
* **Canais de Distribuição:** Fornecimento corporativo B2B (70% da receita, com 180 a 220 pedidos mensais) e vendas diretas pelo site como canal complementar (30% da receita).

### O Desafio Operacional
A expansão rápida sobrecarregou os processos manuais da empresa, que permaneceram dependentes de três planilhas locais do Excel e de um ERP legado desconectado. Isso resultou em uma perda operacional de **R$ 3.890.000,00 por ano** em fretes de emergência duplicados, pedidos cancelados por lentidão na esteira de crédito (SLA de 48h) e atraso de 5 dias úteis no fechamento contábil mensal.

---

## 2. Estrutura do Repositório

O projeto adota uma arquitetura modular, com separação estrita entre dados brutos, fundação estratégica, esteira de operações, scripts utilitários e logs de auditoria:

```text
├── 00_contexto_e_regras/           # Documento de contexto contínuo, memória viva e regras de governança
├── 01_dados_originais/             # Insumos originais e imutáveis (kit de dados e briefings)
│   ├── briefings_desafio/          # Transcrições das instruções e templates oficiais
│   └── kit_de_dados/               # Planilhas (.xlsx), documentos (.docx, .pdf) e catálogo oficial
├── 02_rota_0_estrategia/           # Fundação Estratégica (Rota 0 - Obrigatória)
│   ├── 01_ai_canvas_taranis_black.md
│   ├── 02_matriz_esforco_impacto_metricas_mudancas.md
│   ├── 03_politica_corporativa_ia_lgpd.md
│   └── prompts/                    # Versionamento auditável dos prompts da Rota 0
├── 03_rota_4_financas_operacoes/   # Especialização em Controladoria & Operações (Rota 4)
│   ├── 01_mapeamento_processo_sipoc.md
│   ├── 02_diagrama_ishikawa_6m_causas_raiz.md
│   ├── 03_diagnostico_orcado_vs_realizado.md
│   └── prompts/                    # Versionamento auditável dos prompts da Rota 4
├── 04_scripts_automacao/           # Scripts Python determinísticos de auditoria, cálculo e segurança
├── 05_logs_execucao/               # Registros formais de execução, integridade SHA-256 e auditoria
└── .agent/skills/                  # Configuração de Skill personalizada para o consultor de IA
```

---

## 3. Metodologias Empregadas

O projeto combina frameworks de estratégia de negócios, metodologias ágeis, gestão da qualidade e inteligência artificial generativa:

1. **AI Canvas Corporativo:** Mapeamento estruturado em 9 blocos para alinhamento entre estratégia de negócio, dados internos e arquitetura técnica.
2. **Matriz Impacto × Esforço:** Priorização de iniciativas em ondas de implementação (Onda 1: Quick Wins fiscais; Onda 2: Fechamento contábil em D+2; Onda 3: Fast-Track de crédito B2B).
3. **Plano de Gestão de Mudanças (Modelo ADKAR):** Conscientização, engajamento, capacitação prática, sustentação em sandbox e reforço por reconhecimento para os 280 colaboradores.
4. **Governança de IA & Conformidade com a LGPD:** Classificação da informação em 4 níveis de sensibilidade, protocolo P4S de sanitização prévia e princípio da responsabilidade do autor.
5. **Mapeamento Lean SIPOC:** Análise detalhada da cadeia de valor do pedido B2B (Suppliers, Inputs, Process, Outputs, Customers) e cálculo de eficiência de ciclo de processo (PCE).
6. **Diagrama de Causa-Raiz de Ishikawa (6M) & 5 Porquês:** Investigação profunda nos eixos Método, Máquina, Mão de Obra, Material, Medição e Meio Ambiente.
7. **Matriz de Ação Preventiva 5W2H:** Definição clara de What, Why, Where, When, Who, How e How Much para cada solução de IA.
8. **Análise de Variância DRE Orçado vs. Realizado:** Auditoria contábil com decomposição de perdas de EBITDA, análise de margem por linha de produto e modelagem preditiva de cenários.

---

## 4. Principais Resultados e Impactos Projetados

* **Recuperação Financeira Anual:** Projeção realista de **+R$ 2.501.000,00 por ano** de retorno em margem operacional líquida.
* **Retorno sobre o Investimento (ROI):** **~900% (9,0x)** sobre o investimento inicial de R$ 250 mil no primeiro ano.
* **Período de Payback:** **1,2 meses (36 dias)** de operação pós-rollout.
* **Lead Time de Pedidos B2B:** Redução do ciclo entre proposta assinada e expedição de **5 dias úteis para menos de 2 horas** (com 65% das propostas em Fast-Track de crédito em < 15 minutos).
* **Fechamento Contábil Mensal:** Redução do prazo de fechamento de **7 dias úteis para 2 dias úteis (D+2)** via conciliação por pareamento probabilístico (*fuzzy matching*).
* **Qualidade Fiscal e Logística:** Queda no índice de erros em notas fiscais e boletos de **6,8% para menos de 0,3%**, estancando despesas de fretes de emergência e multas.

---

## 5. Como Reproduzir e Navegar pelo Projeto

### Pré-requisitos
* Git instalado.
* Python 3.10 ou superior.

### Passo a Passo
1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/Challenge-TaranisBlack.git
   cd Challenge-TaranisBlack
   ```

2. **Configurar o Ambiente Virtual Python:**
   ```bash
   python -m venv .venv
   # No Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # No Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instalar Dependências de Análise:**
   ```bash
   pip install pandas openpyxl python-docx
   ```

4. **Executar Auditorias e Testes Internos:**
   ```bash
   # Auditoria preventiva de privacidade pré-commit:
   python 04_scripts_automacao/05_auditar_privacidade_precommit.py

   # Verificação de integridade das hiperligações Markdown:
   python 04_scripts_automacao/03_auditar_corrigir_links.py
   ```

5. **Navegar pelos Artefatos:**
   * Inicie pelo diagnóstico corporativo em [`00_contexto_e_regras/CONTEXTO_PROJETO.md`](./00_contexto_e_regras/CONTEXTO_PROJETO.md).
   * Explore as entregas estratégicas da Rota 0 em [`02_rota_0_estrategia/`](./02_rota_0_estrategia/).
   * Explore o mapeamento operacional e financeiro da Rota 4 em [`03_rota_4_financas_operacoes/`](./03_rota_4_financas_operacoes/).

---

## 6. Governança e Segurança da Informação

Este repositório segue padrões de desenvolvimento seguro e proteção de dados:
* **Privacidade de Infraestrutura:** 100% das referências a caminhos de arquivos empregam notação relativa à raiz do projeto (`./`), sem expor identificadores ou diretórios locais da máquina de desenvolvimento.
* **Conformidade LGPD:** As bases simuladas de dados brutos são mantidas exclusivamente em seus formatos originais, sem dispersão indevida de dados fictícios de colaboradores em arquivos abertos de texto.
* **Isolamento de Ambiente:** O arquivo `.gitignore` previne o envio de ambientes virtuais, arquivos temporários de suítes de escritório e caches de execução.

---
*Projeto desenvolvido para fins educacionais e de consultoria simulada — Formação ONE (Oracle Next Education) & Alura.*
