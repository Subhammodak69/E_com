import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useProductDetails } from '../contexts/ProductDetailsContext';

const ProductDetails = () => {
  const { id } = useParams();
  const { productDetail, loadingDetail, errorDetail, fetchProductDetailById } = useProductDetails();

  useEffect(() => {
    fetchProductDetailById(id);
  }, [id]);

  if (loadingDetail) return <div>Loading...</div>;
  if (errorDetail) return <div>{errorDetail}</div>;
  if (!productDetail) return <div>No product found.</div>;

  return (
    <div style={{ maxWidth: 600, margin: '50px auto', background: '#fff', padding: 24, borderRadius: 8 }}>
      <img src={productDetail.photo_url} alt={productDetail.name} style={{ width: '100%', height: 340, objectFit: 'contain' }} />
      <h1>{productDetail.name}</h1>
      <p style={{ color: '#666', fontSize: 18 }}>{productDetail.description}</p>
      <div style={{ fontWeight: 'bold', fontSize: 22, marginTop: 18 }}>
        ${productDetail.price.toFixed(2)}
      </div>
    </div>
  );
};

export default ProductDetails;
