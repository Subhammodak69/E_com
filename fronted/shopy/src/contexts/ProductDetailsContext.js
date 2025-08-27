// src/contexts/ProductDetailsContext.js
import React, { createContext, useContext, useState } from 'react';

const ProductDetailsContext = createContext();

export const ProductDetailsProvider = ({ children }) => {
  const [productDetail, setProductDetail] = useState(null);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [errorDetail, setErrorDetail] = useState(null);

  const fetchProductDetailById = async (id) => {
    setLoadingDetail(true);
    setErrorDetail(null);
    try {
      const res = await fetch(`http://127.0.0.1:8000/productitems/${id}`);
      if (!res.ok) throw new Error('Failed to fetch product detail');
      const data = await res.json();
      setProductDetail(data);
      setLoadingDetail(false);
      return data;
    } catch (error) {
      setErrorDetail(error.message);
      setLoadingDetail(false);
      setProductDetail(null);
      return null;
    }
  };

  return (
    <ProductDetailsContext.Provider
      value={{ productDetail, loadingDetail, errorDetail, fetchProductDetailById }}
    >
      {children}
    </ProductDetailsContext.Provider>
  );
};

export const useProductDetails = () => useContext(ProductDetailsContext);
