const PRODUCTION_APP_BASE_URL = 'https://example.com'

export function getAppBaseUrl() {
  const configuredBaseUrl = import.meta.env.VITE_APP_BASE_URL

  if (configuredBaseUrl) {
    return configuredBaseUrl
  }

  if (import.meta.env.DEV) {
    return window.location.origin
  }

  return PRODUCTION_APP_BASE_URL
}

