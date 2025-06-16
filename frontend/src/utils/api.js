import axios from 'axios'

// Allow overriding the API base URL so that production builds can
// communicate with the Django backend even when served from a different
// domain or port. During local development the Vite proxy handles API
// requests, so we keep the base URL empty in that case.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || ''
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
