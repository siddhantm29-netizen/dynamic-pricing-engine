import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import ProductCatalog from './pages/ProductCatalog';
import ProductDetail from './pages/ProductDetail';
import CompetitorPrices from './pages/CompetitorPrices';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<ProductCatalog />} />
            <Route path="/products/:id" element={<ProductDetail />} />
            <Route path="/competitors" element={<CompetitorPrices />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
