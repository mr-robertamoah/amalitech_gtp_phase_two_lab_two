import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to Product Catalog</h1>
      <p>Browse products or create your own!</p>
      <div style={{ marginTop: '30px' }}>
        <Link to="/products" className="btn btn-primary" style={{ marginRight: '10px' }}>
          Browse Products
        </Link>
        <Link to="/register" className="btn btn-primary">
          Get Started
        </Link>
      </div>
    </div>
  );
};

export default Home;