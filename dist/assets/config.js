/* Configuração pública: IDs do Google não são senhas. Nunca coloque chaves privadas aqui. */
window.SITE_CONFIG = {
  whatsapp: '558589414720',
  phone: '+558589414720',
  whatsappMessage: 'Olá! Encontrei vocês pelo site e gostaria de tirar uma dúvida sobre o financiamento do meu veículo.',
  google: {
    // Use GTM OU a integração direta GA4/Ads para evitar eventos duplicados.
    tagManagerId: '', // GTM-XXXXXXX; quando preenchido, configure GA4/Ads dentro do GTM.
    analyticsId: '', // G-XXXXXXXXXX
    adsId: 'AW-979637512', // Google Ads — instruções do escritório
    whatsappConversionLabel: 'oAtYCN61l_ocEIiqkNMD', // Rótulo da conversão do Google Ads
    phoneConversionLabel: 'qXYMCOG1l_ocEIiqkNMD'
  }
};
