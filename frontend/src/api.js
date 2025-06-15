const API_URL = process.env.REACT_APP_API_URL || '';

export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        message: 'An unknown error occurred',
      }));
      throw new Error(error.message || 'Request failed');
    }

    return response.json();
  } catch (error) {
    console.error(`API request failed for ${url}:`, error);
    throw error;
  }
};

const api = {
  // Auth endpoints
  register: (userData) => apiRequest('/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  
  login: (credentials) => apiRequest('/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  }),
  
  logout: (token) => apiRequest('/logout', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  }),
  
  // Product endpoints
  getAllProducts: () => apiRequest('/products'),
  
  getUserProducts: (token) => apiRequest('/products/user', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  }),
  
  getProduct: (id) => apiRequest(`/products/${id}`),
  
  createProduct: (productData, token) => apiRequest('/products', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(productData),
  }),
  
  updateProduct: (id, productData, token) => apiRequest(`/products/${id}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(productData),
  }),
  
  deleteProduct: (id, token) => apiRequest(`/products/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  }),
};

export default api;