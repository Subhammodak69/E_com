import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const ProductsContext = createContext();

export const ProductsProvider = ({ children }) => {
  const [products, setProducts] = useState([]);
  const [loadingProducts, setLoadingProducts] = useState(true);
  const [error, setError] = useState(null);

  const fetchProducts = async () => {
    setLoadingProducts(true);
    try {
      const response = await axios.get('http://localhost:8000/productitems'); // Adjust URL to your backend
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load products');
      setProducts([]);
    } finally {
      setLoadingProducts(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <ProductsContext.Provider value={{ products, loadingProducts, error }}>
      {children}
    </ProductsContext.Provider>
  );
};
