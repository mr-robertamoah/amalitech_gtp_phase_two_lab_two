import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const ProductCard = ({ product, onDelete }) => {
  const { user } = useContext(AuthContext);
  const isOwner = user && user.id === product.user_id;

  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
      
      {isOwner && (
        <div style={{ marginTop: '10px' }}>
          <Link to={`/edit-product/${product.id}`} className="btn btn-primary" style={{ marginRight: '10px' }}>
            Edit
          </Link>
          <button onClick={() => onDelete(product.id)} className="btn btn-danger">
            Delete
          </button>
        </div>
      )}
    </div>
  );
};

export default ProductCard;