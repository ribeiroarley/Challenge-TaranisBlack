# 🧠 MEMÓRIA OPERACIONAL VIVA & REGISTRO DE DECISÕES TÉCNICAS
**Projeto:** Challenge AI for Business — Taranis Black (ONE | G11)  
**Documento Mestre de Memória e Rastreamento:** `00_contexto_e_regras/MEMORIA_EXECUCAO.md`  
**Autor:** Arley Ribeiro da Silva Xavier | Consultor de IA  
**Última Atualização:** 2026-11-05 18:08 | Versão 1.1  
**Status de Execução:** Rota 0 & Rota 4 100% Homologadas | Pronto para Consolidação Final no Google Docs  

---

## 1. Tabela Cronológica de Execução de Artefatos & Status

| Fase / Escopo | Identificador do Artefato | Caminho do Arquivo Físico | Hash SHA-256 (Início) | Status de Homologação |
|---|---|---|---|:---:|
| **Setup & Auditoria** | Auditoria e Inventário Inicial | [`05_logs_execucao/log_auditoria_reorganizacao.md`](../05_logs_execucao/log_auditoria_reorganizacao.md) | `7daad3081069...` | **CONCLUÍDO (100% Íntegro)** |
| **Setup & Automação** | Script de Migração Não Destrutiva | [`04_scripts_automacao/01_organizar_workspace.py`](../04_scripts_automacao/01_organizar_workspace.py) | `Script Python venv` | **EXECUTADO & VALIDADO** |
| **Rota 0 — Estratégia** | AI Canvas Corporativo (9 Blocos) | [`02_rota_0_estrategia/01_ai_canvas_taranis_black.md`](../02_rota_0_estrategia/01_ai_canvas_taranis_black.md) | `25.041 Bytes` | **HOMOLOGADO** |
| **Rota 0 — Estratégia** | Matriz Esforço × Impacto, OKRs e ADKAR | [`02_rota_0_estrategia/02_matriz_esforco_impacto_metricas_mudancas.md`](../02_rota_0_estrategia/02_matriz_esforco_impacto_metricas_mudancas.md) | `19.757 Bytes` | **HOMOLOGADO** |
| **Rota 0 — Estratégia** | Política Corporativa de IA & LGPD | [`02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md`](../02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md) | `15.345 Bytes` | **HOMOLOGADO** |
| **Rota 0 — Rastreabilidade** | Prompt AI Canvas (`PROMPT-R0-01`) | [`02_rota_0_estrategia/prompts/01_prompt_ai_canvas.md`](../02_rota_0_estrategia/prompts/01_prompt_ai_canvas.md) | `3.385 Bytes` | **GRAVADO & VERSIONADO** |
| **Rota 0 — Rastreabilidade** | Prompt Matriz Esforço (`PROMPT-R0-02`) | [`02_rota_0_estrategia/prompts/02_prompt_matriz_esforco_impacto.md`](../02_rota_0_estrategia/prompts/02_prompt_matriz_esforco_impacto.md) | `3.401 Bytes` | **GRAVADO & VERSIONADO** |
| **Rota 0 — Rastreabilidade** | Prompt Política IA (`PROMPT-R0-03`) | [`02_rota_0_estrategia/prompts/03_prompt_politica_ia_responsavel.md`](../02_rota_0_estrategia/prompts/03_prompt_politica_ia_responsavel.md) | `4.234 Bytes` | **GRAVADO & VERSIONADO** |
| **Rota 4 — Finanças/Op** | Mapeamento Lean de Processo (SIPOC) | [`03_rota_4_financas_operacoes/01_mapeamento_processo_sipoc.md`](../03_rota_4_financas_operacoes/01_mapeamento_processo_sipoc.md) | `16.480 Bytes` | **HOMOLOGADO** |
| **Rota 4 — Rastreabilidade** | Prompt Mapeamento SIPOC (`PROMPT-R4-01`) | [`03_rota_4_financas_operacoes/prompts/01_prompt_sipoc_mapeamento.md`](../03_rota_4_financas_operacoes/prompts/01_prompt_sipoc_mapeamento.md) | `3.650 Bytes` | **GRAVADO & VERSIONADO** |
| **Rota 4 — Finanças/Op** | Diagrama de Causa-Raiz Ishikawa (6M) | [`03_rota_4_financas_operacoes/02_diagrama_ishikawa_6m_causas_raiz.md`](../03_rota_4_financas_operacoes/02_diagrama_ishikawa_6m_causas_raiz.md) | `16.920 Bytes` | **HOMOLOGADO** |
| **Rota 4 — Rastreabilidade** | Prompt Diagrama Ishikawa (`PROMPT-R4-02`) | [`03_rota_4_financas_operacoes/prompts/02_prompt_ishikawa_causa_raiz.md`](../03_rota_4_financas_operacoes/prompts/02_prompt_ishikawa_causa_raiz.md) | `3.880 Bytes` | **GRAVADO & VERSIONADO** |
| **Rota 4 — Finanças/Op** | Diagnóstico DRE Orçado vs Realizado | [`03_rota_4_financas_operacoes/03_diagnostico_orcado_vs_realizado.md`](../03_rota_4_financas_operacoes/03_diagnostico_orcado_vs_realizado.md) | `18.520 Bytes` | **HOMOLOGADO (100% ROTA 4)** |
| **Rota 4 — Rastreabilidade** | Prompt DRE Orçado vs Realizado (`PROMPT-R4-03`) | [`03_rota_4_financas_operacoes/prompts/03_prompt_diagnostico_orcado_realizado.md`](../03_rota_4_financas_operacoes/prompts/03_prompt_diagnostico_orcado_realizado.md) | `4.110 Bytes` | **GRAVADO & VERSIONADO** |
| **Segurança & Compliance** | Sanitização de Caminhos & Privacidade | [`04_scripts_automacao/02_sanitizar_caminhos.py`](../04_scripts_automacao/02_sanitizar_caminhos.py) | `Script Python venv` | **CONCLUÍDO & AUDITADO** |
| **Comunicação & Estilo** | Calibração de Tom e Linguagem Clara | [`04_scripts_automacao/04_revisar_tom_linguagem.py`](../04_scripts_automacao/04_revisar_tom_linguagem.py) | `Script Python venv` | **CONCLUÍDO & REVISADO** |
| **Publicação & Git** | Preparação para GitHub & README Principal | [`README.md`](../README.md) | `Markdown executivo` | **CONCLUÍDO & HOMOLOGADO** |
| **Governança & Autoria** | Consolidação de Autoria e Titularidade | [`04_scripts_automacao/06_atualizar_autoria.py`](../04_scripts_automacao/06_atualizar_autoria.py) | `Script Python venv` | **CONCLUÍDO & HOMOLOGADO** |
| **Entrega Final (DOCX)** | Relatório Executivo Oficial Polido com Prompts por Página | [`03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx`](../03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx) | `61.145 Bytes` | **HOMOLOGADO (14 PÁGINAS, 6 PÁG DEDICADAS DE PROMPTS, ZERO EMOJIS)** |

---

## 2. Registro Histórico de Decisões Técnicas de Arquitetura (ADRs)

### Decisão 1: Preservação Intacta dos Arquivos Brutos (Preservação de dados)
* **Contexto:** Existiam 11 arquivos na pasta legada `Material de Apoio` e 3 na raiz sem segregação clara de camadas de dados.
* **Decisão:** Criar a pasta `01_dados_originais/` com subpastas `kit_de_dados/` e `briefings_desafio/`, efetuando a migração atestada por hash criptográfico SHA-256 antes e depois. O diretório antigo foi removido apenas após a validação bit a bit.
* **Consequência:** Integridade 100% comprovada dos dados de auditoria; rastreabilidade perante a banca examinadora do Challenge.

### Decisão 2: Arquitetura Periférica Não Invasiva (Veto à Troca de ERP)
* **Contexto:** O ERP legado da Taranis Black não possui APIs modernas e gera lentidão crônica de conciliação e aprovação.
* **Decisão:** Vetar categoricamente a substituição ou reescrita do ERP (classificada como armadilha de tempo / *Time Sink* de 12 a 18 meses). Em seu lugar, adotar uma **camada de inteligência periférica (*wrapper architecture*)** com automações em Python, OCR e IA generativa que consomem e alimentam os dados sem intervenção destrutiva no banco central.
* **Consequência:** Entregas rápidas em ondas (Onda 1 em 4 semanas), redução drástica de risco operacional e retorno financeiro acelerado.

### Decisão 3: Isolamento Obrigatório no Ambiente Virtual `.venv`
* **Contexto:** O sistema possui dependências de pacotes analíticos (`pandas`, `openpyxl`, `python-docx`, `numpy`).
* **Decisão:** Nenhuma rotina de automação, script ou teste pode ser executada fora do interpretador `.\.venv\Scripts\python.exe`. O `.venv` e eventuais metadados de versionamento `.git` devem ser rigorosamente preservados.
* **Consequência:** Reprodutibilidade absoluta em qualquer máquina ou pipeline de CI/CD.

### Decisão 4: Rastreabilidade Obrigatória de Prompts (Prompt Versioning)
* **Contexto:** No modelo tradicional de consultoria com IA, prompts são disparados de forma efêmera sem histórico, inviabilizando auditorias e reprodutibilidade de resultados.
* **Decisão:** Instituição da regra de que todo artefato gerado deve possuir um espelho de rastreabilidade na pasta `prompts/` contendo ID unívoco, data/hora, modelo utilizado, status de homologação e o texto exato da instrução original.
* **Consequência:** Governança e auditoria plena de cada linha de entrega do projeto.

### Decisão 5: Higienização de Caminhos Locais e Privacidade de Workspace (Security & Portability)
* **Contexto:** Artefatos e prompts continham referências a caminhos absolutos locais de sistema de arquivos e identificadores nominais de máquina (`[CAMINHO_ABSOLUTO_LOCAL]`).
* **Decisão:** Realizar varredura e higienização não destrutiva automatizada via Python (`04_scripts_automacao/02_sanitizar_caminhos.py`), substituindo todos os caminhos absolutos por notação relativa padronizada (`./`), preservando dados brutos e ambientes virtuais.
* **Consequência:** Eliminação de vazamento de metadados locais, total portabilidade do repositório para avaliação em qualquer sistema e conformidade estrita com a Regra 5 de Governança.

### Decisão 6: Calibração de Tom de Voz, Simplicidade e Foco Operacional B2B (Clarity & Usability)
* **Contexto:** Documentos utilizavam expressões retóricas inflamadas ("sangria", "blindagem", "cirúrgico"), títulos inflados ("Sênior", "Arquiteto") e termos médicos/bélicos desnecessários.
* **Decisão:** Realizar revisão automatizada em lote (`04_scripts_automacao/04_revisar_tom_linguagem.py`), adotando "Consultor de IA", substituindo jargões por termos objetivos de gestão de negócios ("perda de margem", "conformidade com a LGPD", "análise detalhada") e ajustando o foco para o canal corporativo B2B com vendas diretas pelo site tratadas como canal complementar.
* **Consequência:** Textos mais acessíveis, diretos e profissionais, facilitando a tomada de decisão pelos gestores da Taranis Black e alinhando perfeitamente a comunicação com a banca avaliadora.

### Decisão 7: Preparação para Repositório Público e Controle de Versão Seguro (Git Governance)
* **Contexto:** O projeto será publicado como repositório público no GitHub, exigindo exclusão garantida de arquivos voláteis (.venv, caches, temporários do Office) e documentação mestre executiva.
* **Decisão:** Criar `.gitignore` completo, implementar o script de auditoria de pré-commit (`04_scripts_automacao/05_auditar_privacidade_precommit.py`), validar a integridade de links e redigir o `README.md` principal na raiz sem badges desnecessários, com instruções claras de reprodutibilidade.
* **Consequência:** Repositório padronizado, seguro e pronto para publicação no GitHub e submissão na plataforma da Alura.

### Decisão 8: Atribuição Formal de Autoria e Titularidade do Projeto (Authorship & Accountability)
* **Contexto:** Os artefatos e prompts empregavam descritores genéricos de autoria ("Consultor de IA", "Pessoa Consultora de IA"), demandando identificação formal do titular do projeto perante a banca examinadora da Alura / ONE G11.
* **Decisão:** Executar script determinístico de atualização de metadados (`04_scripts_automacao/06_atualizar_autoria.py`), atribuindo formalmente a autoria a **Arley Ribeiro da Silva Xavier** no papel de **Consultor de IA** em todos os documentos Markdown, prompts, regras e logs, sem comprometer a notação de caminhos relativos ou a privacidade do ambiente local.
* **Consequência:** Total clareza de titularidade e responsabilização profissional dos artefatos, atendendo aos critérios de avaliação acadêmica e corporativa.

### Decisão 9: Preenchimento e Diagramação Corporativa do Relatório Executivo (Zero Emojis Policy)
* **Contexto:** O relatório executivo oficial em formato Microsoft Word (`.docx`) exigia o preenchimento de todas as seções das Rotas 0 e 4 com base nos requisitos do guia oficial, sob a restrição inegociável de estilo corporativo sóbrio (zero emojis).
* **Decisão:** Desenvolver e executar script em Python (`04_scripts_automacao/07_gerar_relatorio_word_executivo.py`) para preencher as 24 tabelas do template com os conteúdos homologados, aplicar formatação visual consistente (azul-marinho corporativo, fundo sóbrio, tipografia executiva Calibri) e expurgar preventivamente 100% de emojis ou pictogramas. Gerar cópia de segurança em `03_rota_4_financas_operacoes/relatorio_final_challenge_taranis_black.docx`.
* **Consequência:** Documento executivo oficial 100% preenchido, formatado em alto padrão profissional, pronto para upload no Google Drive e submissão na plataforma da Alura.

### Decisão 10: Reengenharia Visual, Tipográfica e de Contrastes do Documento Executivo (Accessible Corporate Design)
* **Contexto:** O documento Word preenchido apresentava sobreposição de tags de sombreamento legadas (`<w:shd w:fill="7d6008">`), gerando falhas severas de contraste visual (texto preto sobre fundo escuro residual), espaçamentos irregulares e quebras de linha artificiais originadas na importação do template.
* **Decisão:** Desenvolver e executar o script de reengenharia visual (`04_scripts_automacao/08_reestruturar_design_word.py`) para erradicar sombreamentos residuais, padronizar paleta corporativa e fontes.
* **Consequência:** Documento executivo oficial de altíssimo padrão corporativo e acessibilidade visual.

### Decisão 11: Reescrita e Diagramação Integral do Documento Word com Quebras Lógicas e Íntegra dos Prompts (Master Layout Architecture)
* **Contexto:** O documento requeria uma arquitetura editorial madura de nível C-Level, eliminando vácuos brancos no rodapé de páginas, padronizando entrelinhas 1.15x com espaçamento uniforme de 3pt após parágrafos, estruturando rigorosamente a narrativa em páginas temáticas completas (Capa, Resumo CEO, Rota 0 Parte 1, Rota 0 Parte 2, Rota 4 SIPOC/PCE, Rota 4 Ishikawa/5W2H, Rota 4 DRE/Margens) e incorporando a íntegra literal de todos os 6 prompts corporativos em caixas dedicadas em fonte Consolas.
* **Decisão:** Desenvolver e executar o gerador definitivo em Python (`04_scripts_automacao/09_gerar_relatorio_final_completo.py`) que constrói o documento OpenXML de forma nativa e pura, sem qualquer herança corrompida de templates anteriores, aplicando 7 quebras de página lógicas (`doc.add_page_break()`), 21 tabelas com `cantSplit` e `tblHeader`, e 6 caixas callout monoespaçadas contendo a íntegra dos prompts PROMPT-R0-01 a PROMPT-R4-03.
* **Consequência:** Documento executivo de 60.926 bytes, contendo 5.598 palavras, 37.356 caracteres, distribuídos em aproximadamente 10 páginas perfeitamente equilibradas, com zero emojis e conformidade total perante a banca examinadora da Alura / ONE G11.

### Decisão 12: Polimento Tipográfico Fino, Justificação Textual e Eliminação de E-Comerciais (Editorial Perfection)
* **Contexto:** A inspeção do documento demandou alinhamento justificado em blocos descritivos e tabelas, normalização estrita de espaços após dois pontos (`: `), substituição sistemática do caractere informal `&` pela conjunção formal "e", blindagem contra cabeçalhos órfãos em caixas de prompts via `keep_with_next` e alinhamento vertical balanceado na tabela de submissão.
* **Decisão:** Desenvolver e executar script em Python (`04_scripts_automacao/10_gerar_relatorio_final_polido.py`) aplicando `paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY` nas narrativas e células descritivas, `vertical_align = WD_ALIGN_VERTICAL.CENTER` nos marcadores de submissão, substituição determinística de 100% dos e-comerciais residuais e ativação de `keep_with_next = True` em todos os cabeçalhos de prompts do Anexo.
* **Consequência:** Documento final de 61.038 bytes com alinhamento visual uniforme, margem direita reta e limpa, zero e-comerciais, zero emojis e acabamento executivo impecável para apreciação da banca examinadora.

### Decisão 13: Reengenharia da Seção de Anexos com Página Dedicada por Prompt (Exclusive Prompt Layout)
* **Contexto:** Abertura do Anexo apresentava espaço ocioso e as caixas de prompts sofriam quebras entre folhas distintas devido à densidade de texto dos prompts mais extensos (mais de 3.000 caracteres).
* **Decisão:** Desenvolver e executar o script de diagramação avançada (`04_scripts_automacao/11_ajustar_prompts_por_pagina.py`) para:
  1. Consolidar na Página Inaugural do Anexo (Página 8) a Matriz de Artefatos Técnicos, a Tabela de Procedimento de Submissão Oficial na Alura e a introdução metodológica da esteira de prompts, preenchendo a folha integralmente sem vácuos brancos.
  2. Alocar cada um dos 6 prompts em uma folha exclusiva e independente (Páginas 9 a 14) antecedida por `doc.add_page_break()`.
  3. Calibrar a geometria das caixas com padding de 80 dxa vertical e 120 dxa lateral, fundo sutil cinza-gelo (`#F8FAFC`), borda lateral de 3pt azul-marinho (`#1A365D`), tipografia em `Consolas` 7.5pt com entrelinhas simples e `keep_with_next` no cabeçalho.
* **Consequência:** Documento executivo oficial consolidado em exatamente 14 páginas perfeitamente equilibradas, contendo 61.145 bytes, com zero emojis, zero quebras desordenadas e legibilidade superior para leitura e auditoria acadêmica.
