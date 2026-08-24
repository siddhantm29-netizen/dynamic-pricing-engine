import axios from 'axios';

// In production (Vercel), VITE_API_URL is set to the Render backend URL.
// In development, Vite's proxy forwards /api to localhost:8000.
const BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({ baseURL: BASE_URL });

export const getProducts         = () => api.get('/products/');
export const getProduct          = (id) => api.get(`/products/${id}`);
export const getProductHistory   = (id) => api.get(`/products/${id}/price-history`);
export const getPricingRecommendation = (id) => api.get(`/pricing/${id}/recommend`);
export const applyPricing        = (id, data) => api.post(`/pricing/${id}/apply`, data);
export const getDashboardStats   = () => api.get('/pricing/dashboard/stats');
export const getCompetitorPrices = (id) => api.get(`/competitors/${id}`);
export const updateCompetitorPrices = () => api.post('/competitors/update');

export default api;
