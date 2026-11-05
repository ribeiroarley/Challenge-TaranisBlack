# PROMPT-R0-03 - POLÍTICA CORPORATIVA DE IA RESPONSÁVEL & DIRETRIZES DE CONFORMIDADE LGPD
- **Data/Hora de Execução:** 2026-11-05 16:54:30-03:00
- **Modelo LLM:** Antigravity (Gemini 3.8 Flash Medium)
- **Rota:** Rota 0 — Estratégia Corporativa de IA
- **Artefato Gerado:** [`02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md`](../03_politica_corporativa_ia_lgpd.md)
- **Status da Validação:** Homologado / Concluído

---

## Conteúdo Integral do Prompt

```markdown
Atue como Consultor de IA e Governança.

SEU OBJETIVO:
Desenvolver a Política Corporativa de IA Responsável & Diretrizes de Conformidade com a LGPD para a Taranis Black, estabelecendo regras formais para os 280 colaboradores sobre o uso seguro de ferramentas de IA Generativa (ChatGPT, Claude, Gemini, Copilot e LLMs locais).

ARTEFATOS A SEREM GERADOS:
1. Documento Executivo de Política:
   `02_rota_0_estrategia/03_politica_corporativa_ia_lgpd.md`
2. Arquivo de Rastreabilidade do Prompt:
   `02_rota_0_estrategia/prompts/03_prompt_politica_ia_responsavel.md` (seguindo rigorosamente o padrão com Prompt ID: PROMPT-R0-03, Metadados, Status e Conteúdo Integral deste prompt).

INSTRUÇÕES DE CONTEÚDO PARA A POLÍTICA (03_politica_corporativa_ia_lgpd.md):

1. OBJETIVO, ESCOPO E APLICABILIDADE:
   - Definição do propósito da política (proteger ativos, clientes e colaboradores enquanto fomenta a inovação).
   - Abrangência sobre todos os 280 colaboradores, terceiros e prestadores de serviço em todas as áreas (Vendas, Marketing, RH, Finanças e Operações).

2. CLASSIFICAÇÃO DA INFORMAÇÃO E DIRETRIZES DE USO DE DADOS:
   - Defina 4 níveis de sensibilidade de dados no contexto de IA:
     * Público (dados de catálogo, posts de blog abertos);
     * Interno (processos operacionais gerais, manuais);
     * Confidencial (DRE, faturamento, margem de produtos, tabelas de frete, estratégias comerciais B2B);
     * Restrito/Sensível (LGPD: dados pessoais, CPFs, salários de colaboradores, dados de saúde ergonômica).
   - Estabeleça regras claras: o que PODE e o que NÃO PODE ser inserido em ferramentas de IA públicas vs. corporativas pagas/fechadas.

3. CASOS DE USO PERMITIDOS VS. USOS EXPRESSAMENTE VETADOS:
   - Permitidos (com guardrails): sumarização de atas sem dados de clientes, redação de rascunhos de e-mails, validação sintática de fórmulas no Excel/Power Query, estruturação de briefings, geração de ideias criativas.
   - Proibidos categoricamente: upload de folhas de pagamento com nomes/salários reais (como os da base de People Analytics), upload de extratos bancários brutos ou relatórios DRE com segredo industrial em ferramentas abertas, tomada de decisão 100% autônoma sobre demissões ou crédito sem supervisão humana (Human-in-the-Loop).

4. PROTOCOLOS DE ANONIMIZAÇÃO E SANITIZAÇÃO PRÉVIA:
   - Passo a passo prático para analistas antes de submeter textos ou tabelas: substituição de nomes por identificadores genéricos ([Colaborador_A], [Cliente_X]), mascaramento de CPFs/CNPJs e remoção de valores monetários absolutos quando desnecessários.

5. MITIGAÇÃO DE ALUCINAÇÕES E RESPONSABILIDADE DO USUÁRIO:
   - Princípio da "Responsabilidade do Autor": a IA é copiloto; o colaborador que assina ou utiliza a resposta é o único responsável pela precisão factual, matemática e fiscal.
   - Obrigatoriedade de checagem cruzada em fontes primárias (especialmente em tributação de fretes, alíquotas de ICMS e cálculos contábeis).

6. GOVERNANÇA, COMITÊ DE IA E PENALIDADES:
   - Papéis do Comitê de Governança de IA (formado por Jurídico/DPO, TI/Segurança da Informação e Liderança de Operações).
   - Canal formal para homologação de novas ferramentas de IA.
   - Consequências disciplinares por descumprimento (advertência, suspensão e responsabilização cível/trabalhista).

PERSISTÊNCIA E VALIDAÇÃO:
Gere ambos os arquivos nos caminhos indicados e exiba no log do terminal o resumo executivo dos 6 pontos da política e a validação de gravação do prompt de rastreabilidade.
```
