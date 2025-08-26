import React, { useContext } from 'react';
import ProductCard from './ProductCard';  // Adjust path as needed
import { ProductsContext } from '../contexts/ProductsContext';  // Adjust path

const Home = () => {
  const { products, loadingProducts, error } = useContext(ProductsContext);

  const handleAddToCart = (product) => {
    alert(`Added ${product.name} to cart!`);
    // Your cart logic here
  };

  if (loadingProducts) {
    return <div>Loading products...</div>;
  }

  if (error) {
    return <div>Error loading products: {error}</div>;
  }

  if (products.length === 0) {
    return <div>Products not found yet.</div>;
  }

  return (
    <>
      <h2>Shows All Products</h2>
      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', background:'white' , margin: 'auto', maxwidth: '1100px', padding: '20px',overflow:'auto' }}>
        {products.map((product) => (
          <ProductCard 
            key={product.id}
            product={product}
            onAddToCart={handleAddToCart}
          />
        ))}
      </div>
    </>
  );
};

export default Home;
