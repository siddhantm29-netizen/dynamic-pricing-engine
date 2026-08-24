import { useState, useEffect } from 'react';
import { getProducts, getCompetitorPrices, updateCompetitorPrices } from '../api/api';

export default function CompetitorPrices() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const prodsRes = await getProducts();
      
      const allData = [];
      for (const p of prodsRes.data.slice(0, 5)) { // limit for demo
        const compRes = await getCompetitorPrices(p.id);
        allData.push({
          product: p,
          competitors: compRes.data
        });
      }
      setData(allData);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setUpdating(true);
    try {
      await updateCompetitorPrices();
      await fetchData();
    } catch (e) {
      console.error(e);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <div className="loading">Loading competitor data...</div>;

  return (
    <div className="page competitors">
      <div className="page-header">
        <h1>Competitor Intelligence</h1>
        <button 
          className="btn btn-primary" 
          onClick={handleRefresh}
          disabled={updating}
        >
          {updating ? 'Scraping...' : 'Simulate Scraping Update'}
        </button>
      </div>

      {data.map((item) => (
        <div key={item.product.id} className="card comp-list-card">
          <h3>{item.product.name} (Our Price: ${item.product.current_price.toFixed(2)})</h3>
          <div className="comp-tags">
            {item.competitors.map(c => {
              const isCheaper = c.price < item.product.current_price;
              return (
                <div key={c.id} className={`comp-tag ${isCheaper ? 'danger' : 'safe'}`}>
                  <strong>{c.competitor_name}</strong>: ${c.price.toFixed(2)}
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
