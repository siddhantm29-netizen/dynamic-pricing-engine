import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProduct, getProductHistory, getPricingRecommendation, getCompetitorPrices, applyPricing } from '../api/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function ProductDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState({
    product: null,
    history: [],
    recommendation: null,
    competitors: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [prodRes, histRes, recRes, compRes] = await Promise.all([
        getProduct(id),
        getProductHistory(id),
        getPricingRecommendation(id),
        getCompetitorPrices(id)
      ]);
      
      const formattedHistory = histRes.data.map(h => ({
        ...h,
        date: new Date(h.timestamp).toLocaleDateString()
      }));

      setData({
        product: prodRes.data,
        history: formattedHistory,
        recommendation: recRes.data,
        competitors: compRes.data
      });
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async () => {
    try {
      await applyPricing(id, {
        recommended_price: data.recommendation.recommended_price,
        reason: 'Applied from detail page'
      });
      fetchData(); // refresh
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) return <div className="loading">Loading details...</div>;
  if (!data.product) return <div>Product not found.</div>;

  const { product, recommendation, history, competitors } = data;

  return (
    <div className="page product-detail">
      <button className="btn btn-secondary back-btn" onClick={() => navigate('/products')}>&larr; Back</button>
      
      <div className="header-section">
        <h1>{product.name}</h1>
        <div className="badges">
          <span className="badge">{product.category}</span>
          <span className="badge stock">Stock: {product.stock_level}</span>
        </div>
      </div>

      <div className="content-grid">
        <div className="left-col">
          <div className="card chart-card">
            <h2>Price History</h2>
            <div className="chart-container" style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={history}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={['auto', 'auto']} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#1b5e20" strokeWidth={2} name="Price ($)" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="card comp-card">
            <h2>Competitor Prices</h2>
            <table className="table">
              <thead>
                <tr>
                  <th>Competitor</th>
                  <th>Price</th>
                </tr>
              </thead>
              <tbody>
                {competitors.map(c => (
                  <tr key={c.id}>
                    <td>{c.competitor_name}</td>
                    <td>${c.price.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="right-col">
          <div className="card recommendation-card">
            <h2>Pricing Recommendation</h2>
            
            <div className="price-comparison">
              <div className="price-box">
                <span className="label">Current Price</span>
                <span className="value">${product.current_price.toFixed(2)}</span>
              </div>
              <div className="arrow">&rarr;</div>
              <div className="price-box highlighted">
                <span className="label">Recommended Price</span>
                <span className="value">${recommendation.recommended_price.toFixed(2)}</span>
              </div>
            </div>

            <div className="metrics">
              <div className="metric">
                <span className="label">Competitor Avg:</span>
                <span>${recommendation.competitor_avg.toFixed(2)}</span>
              </div>
              <div className="metric">
                <span className="label">Demand Score:</span>
                <span>{recommendation.demand_score.toFixed(2)}x</span>
              </div>
            </div>

            <div className="explanation-box">
              <h3>AI Reasoning:</h3>
              <p>{recommendation.explanation}</p>
            </div>

            <button 
              className="btn btn-primary full-width" 
              onClick={handleApply}
              disabled={product.current_price === recommendation.recommended_price}
            >
              {product.current_price === recommendation.recommended_price ? 'Price is Optimal' : 'Apply Recommendation'}
            </button>
          </div>
          
          <div className="card details-card">
            <h2>Product Constraints</h2>
            <ul className="constraint-list">
              <li><strong>Cost Price:</strong> ${product.cost_price.toFixed(2)}</li>
              <li><strong>Base Price:</strong> ${product.base_price.toFixed(2)}</li>
              <li><strong>MSRP:</strong> ${product.msrp.toFixed(2)}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
