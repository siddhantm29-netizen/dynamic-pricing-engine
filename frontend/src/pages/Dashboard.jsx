import { useState, useEffect } from 'react';
import { getDashboardStats } from '../api/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await getDashboardStats();
      setStats(res.data);
    } catch (error) {
      console.error('Failed to fetch stats', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading dashboard...</div>;

  // Mock data for chart
  const mockCategoryData = [
    { name: 'Electronics', impact: 4.2 },
    { name: 'Clothing', impact: 2.1 },
    { name: 'Books', impact: 0.8 },
    { name: 'Appliances', impact: 3.5 },
  ];

  return (
    <div className="page dashboard">
      <h1>Pricing Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Products</h3>
          <div className="value">{stats?.total_products || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Avg Price Change</h3>
          <div className={`value ${stats?.avg_price_change_pct > 0 ? 'text-success' : 'text-danger'}`}>
            {stats?.avg_price_change_pct > 0 ? '+' : ''}{stats?.avg_price_change_pct || 0}%
          </div>
        </div>
        <div className="stat-card">
          <h3>Revenue Impact</h3>
          <div className={`value ${stats?.revenue_impact_pct > 0 ? 'text-success' : 'text-danger'}`}>
            {stats?.revenue_impact_pct > 0 ? '+' : ''}{stats?.revenue_impact_pct || 0}%
          </div>
        </div>
        <div className="stat-card alert">
          <h3>Needs Review</h3>
          <div className="value">{stats?.products_needing_review || 0}</div>
        </div>
      </div>

      <div className="chart-section">
        <h2>Revenue Impact by Category</h2>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={mockCategoryData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="impact" fill="#1b5e20" name="Impact (%)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
