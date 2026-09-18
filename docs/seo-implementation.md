# Implementação da spec SEO — 17/09/2026

## Estado por atividade

| Atividade | Implementado | Pendente |
|---|---|---|
| SEO-01 | Modo de revisão preservado; inspeção confirma nenhum domínio conectado; proteção de geração pública | Domínio/DNS/HTTPS, autorização de público, redirecionamentos e verificação HTTP real |
| SEO-02 | Título/description preservados; token vazio removido; gerador de canonical limpa e token real | Ativar canonical após domínio operacional |
| SEO-03 | Gerador JSON-LD LegalService com endereço visível consistente e validação de dados obrigatórios | Endereço completo e confirmação dos dados; Schema.org e Rich Results Test externos |
| SEO-04 | Robots de revisão; gerador de sitemap e robots público; limpeza automática ao voltar para revisão | Publicação/validação dos arquivos no domínio definitivo |
| SEO-05 | Ícones presentes no HTML; dimensões reais nas imagens; decode assíncrono; preservados WebP, preload e defer; baseline de bytes | LCP/CLS/INP, 3 medições por perfil, cache/compressão reais, impacto de tags de marketing |
| SEO-06 | Fontes em rem; cards em duas colunas até 991px; quebra de controles; texto das notas mantido no mobile; compensação da altura real da barra | Validação visual nas 11 larguras, orientação horizontal e zoom 200% |
| SEO-07 | Canais de contato e nomes de eventos preservados; token de verificação configurável | Search Console, IDs Google, inspeção, sitemap e dados reais |

## Como ativar quando as dependências estiverem resolvidas

1. Confirmar domínio HTTPS operacional e lançamento público autorizado. O script NÃO conecta domínio, muda audiência nem verifica DNS por conta própria.
2. Editar `config/seo.json`: `mode: production`, `domain_verified: true` e `public_release_authorized: true` somente após verificações reais.
3. Para JSON-LD, preencher `business.address` com `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry` e marcar `business.confirmed: true` após confirmação pelo escritório. O endereço será inserido no rodapé e no JSON-LD. Dados opcionais ausentes são omitidos. Dados de teste não entram no site.
4. Se o endereço estiver pendente, manter `business.confirmed: false`. O site público pode receber canonical e sitemap, porém não será declarado completo para SEO local.
5. Para verificação HTML do Search Console, preencher `search_console_token`; para DNS, manter null.
6. Executar `python scripts/prepare_seo.py` e `python -m unittest discover -s tests -v`. Revisar o diff, validar interfaces e publicar o estado exato usando Sites.
7. Validar HTTP 200, variantes com redirecionamentos sem perda de UTMs/gclid, ausência de noindex na produção e acesso ao robots/sitemap efetivamente servidos.
8. Executar os validadores externos e Search Console. Não classificar geração local como validação do Google.

O script é idempotente e edita blocos marcados em `dist/index.html`. Executá-lo novamente depois de alterações de configuração. Os arquivos de configuração ficam fora de dist e não são publicados como assets.

## Revisão privada

O modo atual é `review`. Gera noindex sem canonical/JSON-LD/sitemap e robots permitindo leitura da diretiva noindex. A autenticação Sites é a proteção de privacidade real; robots não protege dados. O modo production remove o noindex. O endereço de revisão não entra em sitemap.

## Evidências disponíveis

- Oito testes offline passaram: links/arquivos/ícones no HTML, revisão sem metadados públicos, guardas de lançamento, idempotência, canonical limpa, XML do sitemap, dados obrigatórios, escaping de endereço/JSON e retorno ao modo privado.
- JavaScript verificado por `node --check` nos dois arquivos.
- Ícones renderizados estaticamente; JavaScript não injeta ícones após o carregamento.
- Nove links de contato mantêm os destinos do briefing sem JavaScript.
- Eventos `click_whatsapp` e `click_phone` e lógica de consentimento preservados. Não se afirma entrega real ao Google sem IDs configurados.
- Medidas de bytes em `seo-baseline.json` e `seo-after.json`; gzip calculado offline, não é evidência de compressão HTTP.

| Arquivo | Antes (bytes) | Depois (bytes) | Gzip estimado antes/depois |
|---|---:|---:|---:|
| index.html | 9.955 | 17.663 | 3.121 / 3.985 |
| app.js | 7.314 | 5.891 | 3.107 / 2.374 |
| styles.css | 13.459 | 15.434 | 3.660 / 4.113 |

A transferência de ícones para HTML aumenta seu tamanho e reduz JS necessário para a primeira renderização; não representa redução total de bytes nem prova de melhora de LCP/CLS. Bootstrap permanece integral (232.111 bytes sem compressão), pois não houve medição de cobertura que justificasse removê-lo parcialmente.

## Limitação de QA

A infraestrutura Sites disponível não fornece servidor de prévia compatível para este projeto estático, conforme a referência de prévia managed-linux. Não foi iniciado um servidor alternativo fora desse fluxo. Portanto não houve navegação de teste, medição Lighthouse ou validação visual simulada. Nenhuma das larguras ou metas de campo está marcada como aprovada. As alterações CSS foram revisadas estaticamente; o gate visual continua pendente. Também não houve validação de cache/headers da produção privada.

## Reversão

Reverter pelo Git a alteração de SEO ou restaurar/publicar a versão Sites anterior (versão 2, revisão a009b89720ce9f6191975a4a64ab8be146005cc4). Não usar reset destrutivo. Para retirar metadados públicos de uma futura revisão privada, restaurar `mode: review` e executar o gerador antes de publicar. Mudanças de DNS e audiência exigem procedimento próprio; o gerador não as desfaz.
