import axios from 'axios'

// Create an axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/cooking/ver3',
  timeout: 10000,
})

// Request interceptor
api.interceptors.request.use(
  config => {
    // Add any request modifications here
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // Handle global error responses here
    if (error.response) {
      // Server responded with error status
      console.error(`API Error: ${error.response.status} - ${error.response.data.message}`)
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received from server')
    } else {
      // Something else happened
      console.error('Error in request setup:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api