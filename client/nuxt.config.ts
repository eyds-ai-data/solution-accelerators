// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  // Runtime config:
  //   Server-only → NUXT_BACKEND_API_URL (e.g. http://server:8000/api/v1 in Docker)
  //   Browser     → NUXT_PUBLIC_BACKEND_API_URL (e.g. http://localhost:8000/api/v1 in Docker)
  runtimeConfig: {
    backendApiUrl: '',
    public: {
      backendApiUrl: 'https://ai-investigation-server.azurewebsites.net/api/v1'
    }
  },

  modules: [
    '@nuxt/eslint',
    '@nuxt/ui',
    '@vueuse/nuxt'
  ],

  app: {
    head: {
      title: 'AI Investigation System'
    }
  },

  devtools: {
    enabled: false
  },

  css: [
    '~/assets/css/main.css',
    "v-network-graph/lib/style.css"
  ],

  routeRules: {
    '/api/**': {
      cors: true
    }
  },

  compatibilityDate: '2024-07-11',

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }
})
