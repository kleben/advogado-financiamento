# Google Ads — configuração do PDF do escritório

Tag: `AW-979637512`.

| Canal | send_to |
|---|---|
| WhatsApp | `AW-979637512/oAtYCN61l_ocEIiqkNMD` |
| Telefone | `AW-979637512/qXYMCOG1l_ocEIiqkNMD` |

Configuração em `dist/assets/config.js`; listeners em `dist/assets/app.js`. Usa integração direta gtag, com GTM e GA4 vazios. Não instalar outra cópia da tag. Todos os CTAs existentes e o telefone do rodapé usam data-contact, com um listener por link. Cada clique autorizado envia somente a conversão do canal; os nomes click_whatsapp/click_phone continuam presentes para uso futuro de GA4/GTM. Não há as funções duplicadas gtag_report_conversion do exemplo do PDF.

A tag é inserida uma única vez no head após aceite de consentimento (inclusive em retorno com aceite salvo). Sem aceite, não carrega Google nem envia conversões. Nenhuma conversão ocorre no carregamento ou ao aceitar cookies. A recusa não bloqueia os contatos.

Os links mantêm a navegação nativa, sem preventDefault, callback de redirecionamento ou espera pela rede. A conversão solicita transporte beacon; a entrega pode ser impedida por bloqueadores/rede e precisa de confirmação no Tag Assistant/Google Ads. Um clique não comprova conversa iniciada ou ligação atendida.

## Validação concluída

`node tests/test_ads.cjs` executa os arquivos reais em um adaptador DOM isolado, sem chamadas publicitárias reais. Verifica os nove links, os IDs exatos, somente uma tag/config, zero conversões no carregamento, aceite/recusa/reaceite, canais separados e ausência de bloqueio de navegação. Sintaxe JavaScript também validada.

## Validação externa pendente

Após o lançamento público no domínio definitivo, validar com Tag Assistant e Google Ads: aceitar consentimento, clicar nos CTAs das diferentes seções, conferir os dois destinos, ausência de duplicação e abertura real de WhatsApp/discador em aparelho. Repetir com consentimento recusado (contato funciona; conversão não enviada). A publicação atual continua privada e o domínio ainda não está conectado. Não há confirmação de recebimento pelo Google.
