import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Package, TrendingUp, Users } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: <LayoutDashboard size={20} /> },
    { path: '/products', label: 'Catalog', icon: <Package size={20} /> },
    { path: '/competitors', label: 'Competitors', icon: <Users size={20} /> },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <TrendingUp className="brand-icon" />
          <span>Dynamic Pricing Engine</span>
        </div>
        <div className="navbar-menu">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
            >
              {item.icon}
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
