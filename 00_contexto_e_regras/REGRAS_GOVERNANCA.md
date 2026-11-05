# ⚖️ REGRAS OPERACIONAIS & DIRETRIZES DE GOVERNANÇA TÉCNICA
**Projeto:** Challenge AI for Business — Taranis Black (ONE | G11)  
**Documento Mestre de Governança:** `00_contexto_e_regras/REGRAS_GOVERNANCA.md`  
**Autor:** Arley Ribeiro da Silva Xavier | Consultor de IA  
**Data de Vigência:** Ano Fiscal 2026 | Versão 1.0  
**Aplicação:** Mandatória para todas as interações e artefatos de IA do projeto  

---

## 1. Princípios Operacionais Inegociáveis

Todo o trabalho de consultoria estratégica, análise de dados e engenharia de software para o Challenge Taranis Black é regido por seis regras operacionais necessárias. O descumprimento de qualquer uma delas invalida o artefato correspondente.

---

### REGRA 1: Isolamento Estrito no Ambiente Virtual Python (`.venv`)
* **Determinação:** Toda e qualquer execução de script, parseamento de planilhas (`openpyxl`, `pandas`), leitura de documentos (`python-docx`), cálculo de hashes criptográficos ou automações locais DEVE ser disparada utilizando exclusivamente o interpretador Python do ambiente virtual local:
  ```powershell
  .\.venv\Scripts\python.exe <caminho_do_script.py>
  ```
* **Preservação de Integridade:** É terminantemente proibido instalar pacotes no ambiente global da máquina do usuário ou modificar arquivos internos da pasta `.venv`. Caso surja controle de versão `.git`, este deve ser mantido estritamente intocado.

---

### REGRA 2: Zero Alucinação & Fidelidade Factual Absoluta
* **Determinação:** Nenhum dado numérico, percentual, nome de cliente, especificação técnica ou métrica orçamentária pode ser inventado, presumido ou alucinado.
* **Origem Compulsória de Dados:** Todos os valores utilizados na Rota 0 e na Rota 4 devem possuir rastreabilidade direta e documental comprovada com os arquivos de insumos oficiais em:
  `01_dados_originais/kit_de_dados/`
  * Faturamento (R$ 48M), EBITDA realizado (R$ 5,77M), estouro de fretes (R$ 960k), perdas totais (R$ 3,89M), atraso no fechamento (+5 dias) $\rightarrow$ derivam fielmente de [`05_Financas_Orcado_vs_Realizado.xlsx`](../01_dados_originais/kit_de_dados/05_Financas_Orcado_vs_Realizado.xlsx).
  * Macroprocesso de 5 passos, SIPOC e causas 6M $\rightarrow$ derivam de [`06_Descritivo_Processo_Operacional_SIPOC.docx`](../01_dados_originais/kit_de_dados/06_Descritivo_Processo_Operacional_SIPOC.docx).
  * Especificações de produto, NR-17 e fretes CIF/FOB $\rightarrow$ derivam de [`01_Catalogo_Produtos_e_Precos_Taranis_Black.docx`](../01_dados_originais/kit_de_dados/01_Catalogo_Produtos_e_Precos_Taranis_Black.docx).

---

### REGRA 3: Rastreabilidade Síncrona e Versionamento de Prompts
* **Determinação:** Nenhum artefato técnico ou estratégico pode ser criado de forma anônima. Para cada novo arquivo gerado nas pastas de entrega (`02_rota_0_estrategia/` e `03_rota_4_financas_operacoes/`), um arquivo espelho de rastreabilidade DEVE ser criado simultaneamente na pasta `prompts/` correspondente.
* **Estrutura Obrigatória de Metadados do Prompt:**
  ```markdown
  # [PROMPT-ID] - [TÍTULO DA ENTREGA]
  - **Data/Hora de Execução:** YYYY-MM-DD HH:MM:SS-03:00
  - **Modelo LLM:** Antigravity (Gemini 3.8 Flash Medium)
  - **Rota:** [Rota 0 ou Rota 4]
  - **Artefato Gerado:** [Caminho do arquivo markdown de entrega]
  - **Status da Validação:** Homologado / Concluído
  ---
  ## Conteúdo Integral do Prompt
  [Instrução literal fornecida pelo usuário, sem omissões]
  ```

---

### REGRA 4: Padrão Executivo C-Level & Qualidade de Entrega Final
* **Determinação:** Todos os documentos devem ser escritos em tom analítico sênior, com linguagem corporativa de alto impacto, diagramas visuais (Mermaid), tabelas quantitativas e memória de cálculo clara.
* **Proibição de Placeholders:** Fica expressamente vedado o uso de termos genéricos como *"lorem ipsum"*, *"[preencher aqui]"*, *"texto a ser adicionado"* ou descrições incompletas. Cada artefato deve estar pronto para submissão no template oficial do Google Docs (`template_rota4_financas.gdoc`) e para escrutínio da banca avaliadora da Alura / ONE G11.

---

### REGRA 5: Privacidade de Infraestrutura Local & Caminhos Relativos
* **Determinação:** É terminantemente proibido registrar caminhos absolutos de sistema de arquivos ou identificadores de usuário de máquina em relatórios, prompts ou scripts. Todos os artefatos devem empregar exclusivamente caminhos relativos ao diretório raiz do projeto (`./`).
* **Proteção de Dados do Ambiente:** Qualquer link ou referência interna deve apontar para a raiz do repositório (ex.: `./01_dados_originais/`, `./02_rota_0_estrategia/`, `./03_rota_4_financas_operacoes/`), garantindo portabilidade entre diferentes sistemas operacionais, isolamento de privacidade de dados locais e total aderência às boas práticas de segurança da informação.

---

### REGRA 6: Clareza, Simplicidade e Moderação no Tom de Voz
* **Determinação:** É obrigatório o emprego de uma linguagem profissional, direta, acessível e colaborativa em português do Brasil. Fica vedado o uso de jargões inflamados, metáforas excessivas (ex.: "sangria", "blindagem", "cirúrgico", "anatomia", "hipercrescimento") ou títulos autoatribuídos inflados ("Sênior", "Arquiteto", etc.).
* **Padrão de Identidade e Canais:** A atuação deve ser identificada como "Consultor de IA" ou "Pessoa Consultora de IA". A comunicação deve refletir a realidade operacional da empresa, mantendo o foco analítico no canal corporativo B2B e tratando vendas diretas pelo site (D2C) como canal complementar secundário, garantindo fácil leitura por qualquer gestor ou colaborador da Taranis Black.

---
*Regras homologadas e em vigor para toda a fase de execução da Rota 4.*
