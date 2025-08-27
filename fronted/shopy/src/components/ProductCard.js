// components/ProductCard.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const ProductCard = ({ product, onAddToCart }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    navigate(`/productitems/${product.id}`);
  };

  return (
    <div style={cardStyle} onClick={handleCardClick}>
      <img src={product.photo_url} alt={product.name} style={imageStyle} />
      <h3 style={{ margin: '0.5rem 0' }}>{product.name}</h3>
      <p style={{ color: '#555', fontSize: '0.9rem' }}>{product.description}</p>
      <div style={priceStyle}>${product.price.toFixed(2)}</div>
      <button
        style={buttonStyle}
        onClick={e => {
          e.stopPropagation();
          onAddToCart(product);
        }}
      >
        Add to Cart
      </button>
    </div>
  );
};
const cardStyle = {
  margin: 'auto',
  width: '200px',
  border: '1px solid #ddd',
  borderRadius: '8px',
  padding: '1rem',
  maxWidth: '250px',
  boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  backgroundColor: 'white',
};

const imageStyle = {
  width: '100%',
  height: '150px',
  objectFit: 'cover',
  borderRadius: '6px',
};

const priceStyle = {
  fontWeight: 'bold',
  fontSize: '1.2rem',
  margin: '0.5rem 0',
};

const buttonStyle = {
  padding: '0.5rem 1rem',
  backgroundColor: '#007bff',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer',
};


export default ProductCard;
