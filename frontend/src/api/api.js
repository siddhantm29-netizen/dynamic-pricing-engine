import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

export const getProducts = () => api.get('/products/');
export const getProduct = (id) => api.get(`/products/${id}`);
export const getProductHistory = (id) => api.get(`/products/${id}/price-history`);
export const getPricingRecommendation = (id) => api.get(`/pricing/${id}/recommend`);
export const applyPricing = (id, data) => api.post(`/pricing/${id}/apply`, data);
export const getDashboardStats = () => api.get('/pricing/dashboard/stats');
export const getCompetitorPrices = (id) => api.get(`/competitors/${id}`);
export const updateCompetitorPrices = () => api.post('/competitors/update');

export default api;
