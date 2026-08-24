import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getProducts, getPricingRecommendation, applyPricing } from '../api/api';

export default function ProductCatalog() {
  const [products, setProducts] = useState([]);
  const [recommendations, setRecommendations] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const res = await getProducts();
      setProducts(res.data);
      // Fetch recommendations for first few to show in grid
      res.data.slice(0, 10).forEach(p => fetchRec(p.id));
    } catch (error) {
      console.error('Failed to fetch products', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchRec = async (id) => {
    try {
      const res = await getPricingRecommendation(id);
      setRecommendations(prev => ({ ...prev, [id]: res.data }));
    } catch (e) {
      console.error(e);
    }
  };

  const handleApply = async (product, rec) => {
    try {
      await applyPricing(product.id, {
        recommended_price: rec.recommended_price,
        reason: 'Applied from catalog grid'
      });
      fetchProducts(); // Refresh list
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) return <div className="loading">Loading products...</div>;

  return (
    <div className="page product-catalog">
      <h1>Product Catalog</h1>
      
      <div className="product-grid">
        {products.map(product => {
          const rec = recommendations[product.id];
          let diff = 0;
          let diffClass = '';
          if (rec) {
            diff = rec.recommended_price - product.current_price;
            diffClass = diff > 0 ? 'text-success' : diff < 0 ? 'text-danger' : '';
          }

          return (
            <div key={product.id} className="product-card">
              <h3><Link to={`/products/${product.id}`}>{product.name}</Link></h3>
              <p className="category">{product.category}</p>
              
              <div className="price-info">
                <div className="current-price">
                  <span>Current: </span>
                  <strong>${product.current_price.toFixed(2)}</strong>
                </div>
                
                {rec && (
                  <div className="rec-price">
                    <span>Recommended: </span>
                    <strong className={diffClass}>${rec.recommended_price.toFixed(2)}</strong>
                    {diff !== 0 && (
                      <span className={`diff ${diffClass}`}>
                        ({diff > 0 ? '+' : ''}{diff.toFixed(2)})
                      </span>
                    )}
                  </div>
                )}
              </div>

              <div className="actions">
                {rec && diff !== 0 ? (
                  <button className="btn btn-primary" onClick={() => handleApply(product, rec)}>
                    Apply New Price
                  </button>
                ) : (
                  <button className="btn" disabled>Optimal</button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
