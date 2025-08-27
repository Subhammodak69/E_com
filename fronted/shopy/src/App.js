// App.js
import React from 'react';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProductsProvider } from './contexts/ProductsContext';
import { ProductDetailsProvider } from './contexts/ProductDetailsContext';  // Import ProductDetailsProvider
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './components/Home';
import Login from './components/Login';
import SignUp from './components/Signup';
import ProductDetails from './components/ProductDetails';

const Layout = () => (
  <div className="App" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
    <Navbar />
    <main style={{ flex: 1, padding: '20px', minHeight: '90vh' }}>
      <Outlet />
    </main>
    <Footer />
  </div>
);

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'login', element: <Login /> },
      { path: 'signup', element: <SignUp /> },
      { path: 'productitems/:id', element: <ProductDetails /> },
    ],
  },
]);

function App() {
  return (
    <AuthProvider>
      <ProductsProvider>
        <ProductDetailsProvider>   {/* Wrap with ProductDetailsProvider */}
          <RouterProvider router={router} />
        </ProductDetailsProvider>
      </ProductsProvider>
    </AuthProvider>
  );
}

export default App;
