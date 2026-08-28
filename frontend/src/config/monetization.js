/**
 * Monetization Configuration
 * Gerencia anúncios, planos de preço e limites de conversão
 */

export const ADSENSE_CONFIG = {
  // ID da conta AdSense já carregada no index.html.
  clientId: 'ca-pub-9678636402491491',
  adSlots: {
    // Preencha com os IDs criados no painel do AdSense para publicar anúncios pagos.
    headerBanner: '',
    sidebarRect: '',
    footerBanner: '',
    mobileBanner: ''
  },
  // Reativar somente em páginas com conteúdo editorial substancial.
  enabled: false
}

export const PRICING_PLANS = {
  free: {
    name: 'Grátis',
    price: 0,
    conversionsPerMonth: 5,
    maxFileSize: 10, // MB
    formats: ['DOCX'],
    showAds: true,
    features: [
      '5 conversões/mês',
      'Máximo 10MB',
      '1 formato por vez',
      'Com anúncios'
    ]
  },
  pro: {
    name: 'Pro',
    price: 4.99,
    conversionsPerMonth: 100,
    maxFileSize: 50, // MB
    formats: ['DOCX', 'PNG', 'JPG', 'TXT', 'XLSX', 'PPTX'],
    showAds: false,
    features: [
      '100 conversões/mês',
      'Máximo 50MB',
      'Todos os formatos',
      'Sem anúncios',
      'Suporte por email'
    ]
  },
  enterprise: {
    name: 'Enterprise',
    price: 19.99,
    conversionsPerMonth: 1000,
    maxFileSize: 100, // MB
    formats: ['DOCX', 'PNG', 'JPG', 'TXT', 'XLSX', 'PPTX'],
    showAds: false,
    features: [
      '1000 conversões/mês',
      'Máximo 100MB',
      'Todos os formatos',
      'Sem anúncios',
      'Suporte prioritário',
      'API access'
    ]
  }
}

export const AD_PLACEMENTS = {
  // Localidades onde os anúncios aparecem
  headerTop: {
    enabled: true,
    format: 'leaderboard', // 728x90
    position: 'after-hero'
  },
  sidebarBottom: {
    enabled: true,
    format: 'medium-rectangle', // 300x250
    position: 'after-converter'
  },
  footerBefore: {
    enabled: true,
    format: 'leaderboard', // 728x90
    position: 'before-footer'
  }
}

/**
 * Verificar se deve mostrar anúncios
 * @param {Object} user - Objeto do usuário
 * @returns {Boolean}
 */
export function shouldShowAds(user = null) {
  if (!ADSENSE_CONFIG.enabled) return false
  if (!user) return true  // Mostrar para usuários não autenticados
  if (user.plan === 'free') return true
  return false
}

/**
 * Obter limite de conversões do usuário
 * @param {String} plan - Plano do usuário (free, pro, enterprise)
 * @returns {Number}
 */
export function getConversionLimit(plan = 'free') {
  return PRICING_PLANS[plan]?.conversionsPerMonth || 5
}

/**
 * Obter tamanho máximo de arquivo
 * @param {String} plan - Plano do usuário
 * @returns {Number} Tamanho em MB
 */
export function getMaxFileSize(plan = 'free') {
  return PRICING_PLANS[plan]?.maxFileSize || 10
}

export default {
  ADSENSE_CONFIG,
  PRICING_PLANS,
  AD_PLACEMENTS,
  shouldShowAds,
  getConversionLimit,
  getMaxFileSize
}
