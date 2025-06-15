import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import ProductCard from '../components/ProductCard';
import api from '../api';

const MyProducts = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { token } = useContext(AuthContext);

  useEffect(() => {
    const fetchUserProducts = async () => {
      try {
        const data = await api.getUserProducts(token);
        setProducts(data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchUserProducts();
  }, [token]);

  const handleDelete = async (productId) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await api.deleteProduct(productId, token);
        setProducts(products.filter(product => product.id !== productId));
      } catch (err) {
        setError(err.message);
      }
    }
  };

  if (loading) return <div>Loading your products...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div>
      <h2>My Products</h2>
      {products.length === 0 ? (
        <p>You haven't added any products yet.</p>
      ) : (
        <div className="product-grid">
          {products.map(product => (
            <ProductCard 
              key={product.id} 
              product={product} 
              onDelete={handleDelete} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default MyProducts;