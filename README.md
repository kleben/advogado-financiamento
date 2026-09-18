## Produção Hostinger — branch main

**Qualquer commit na branch main publica no site real https://advogadofinanciamento.com.br/.**

A hospedagem serve a raiz do repositório. O `index.html` da raiz é a página completa e carrega CSS, JavaScript e imagens de `dist/assets/`. Não remover esse arquivo nem substituir por um redirecionamento para `/dist/`.

Após editar `dist/index.html` ou as configurações SEO, execute `python scripts/prepare_production.py` e inclua os arquivos gerados (`index.html`, `robots.txt`, `sitemap.xml`) no mesmo commit. A geração usa `config/seo-production.json`, remove o noindex de revisão e define a canonical do domínio real. `config/seo.json` e `dist/` continuam compatíveis com a revisão privada no Sites. Não há build automático necessário no servidor: os arquivos gerados são versionados.

Os dados estruturados locais continuam pendentes do endereço completo confirmado. Os arquivos de produção não incluem JSON-LD incompleto.

# Alcântara Advogados — Revisional de Veículos

Página estática responsiva inspirada na referência fornecida. HTML, CSS e JavaScript separados. Bootstrap 5.3.8 incluído localmente, sem dependência do CDN para renderizar a página. Fotos extraídas da referência do usuário.

## Arquivos
- `dist/index.html`: conteúdo, metadados e verificação do Search Console.
- `dist/assets/styles.css`: estilos e breakpoints.
- `dist/assets/config.js`: telefone, WhatsApp e IDs públicos de medição.
- `dist/assets/app.js`: contatos, ícones, diálogos e consentimento.

## Google
Preencha `google.tagManagerId` para usar GTM e configure suas tags GA4/Ads no contêiner. Alternativamente, deixe GTM vazio e preencha `analyticsId` e/ou `adsId` para integração direta. Não use ambas as formas para a mesma tag.

Após consentimento, cliques geram eventos separados `click_whatsapp` e `click_phone`, com `contact_channel` e `contact_location` (`header`, `hero`, `contact`, `footer` ou `mobile_bar`). No GTM são eventos no dataLayer; na integração direta são eventos GA4. Configure cada evento como uma conversão independente na plataforma escolhida; evite contar uma mesma ação simultaneamente por importação GA4 e tag Ads. O evento mede o clique, não confirma conversa ou ligação atendida. Para Google Ads, preencha o ID AW e os rótulos das conversões correspondentes. IDs vazios não carregam scripts de rastreamento. Consentimento padrão negado; nenhuma chamada Google é feita pelo código de métricas antes da aceitação. Preferências podem ser alteradas na política de privacidade. A revogação atualiza o consentimento, sem apagar retroativamente dados já enviados.

Para Search Console, configure `search_console_token` em `config/seo.json` e execute `python scripts/prepare_seo.py`, ou use verificação DNS no domínio definitivo. Nenhuma chave secreta deve ser inserida no frontend.

## Contato
O número (85) 8941-4720 e o e-mail foram transcritos exatamente da referência. Confira o formato atual do número e se está habilitado no WhatsApp antes de divulgação pública. A configuração de telefone é centralizada em config.js; ao alterá-la, atualize também o texto visível e os hrefs de fallback em index.html.

Política de privacidade e termos são textos iniciais e devem refletir a operação real do escritório antes da divulgação. Publicação inicial privada para revisão.

## Domínio do briefing
Domínio previsto: `advogadofinanciamento.com.br`. A publicação de revisão permanece no endereço Sites. O domínio próprio ainda precisa ser conectado e ter o DNS configurado; não foi alterado nesta revisão. Após conexão, configurar o endereço definitivo na campanha e verificar a propriedade no Search Console.

## Revisão do briefing
Incluída barra fixa mobile com área segura e espaço no rodapé, mensagem exata de WhatsApp também nos links de fallback, textos dos cards alinhados e primeira dobra mais compacta. Sem menu, sem destinos externos além dos canais de contato. Privacidade e termos abrem na própria página. Na barra, a regra global prevalece: “Falar no WhatsApp”, mesmo onde o briefing abrevia “WhatsApp”.

## SEO técnico
Configuração em `config/seo.json`; geração estática com `python scripts/prepare_seo.py`. A revisão atual permanece privada, sem canonical de domínio não conectado e sem dados locais incompletos. O modo público gera canonical/sitemap; JSON-LD é gerado somente com endereço confirmado. Consulte `docs/seo-implementation.md` para estado por atividade, evidências, pendências, ativação e reversão.

## Google Ads configurado
Aplicados os identificadores do PDF do escritório: tag `AW-979637512`, WhatsApp `oAtYCN61l_ocEIiqkNMD` e telefone `qXYMCOG1l_ocEIiqkNMD`. Consulte `docs/google-ads.md`. Consentimento continua obrigatório para disparo, sem bloquear links. Validação isolada com `node tests/test_ads.cjs`; recebimento real pelo Google ainda precisa de teste externo.
