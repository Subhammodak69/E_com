import React from 'react';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Login from './components/Login';
import SignUp from './components/Signup';

const Layout = () => (
  <div className="App" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
    <Navbar />
    <main style={{ flex: 1, padding: '20px', minHeight: '90vh' }}>
      <Outlet />
    </main>
    <Footer />
  </div>
);

const Home = () => (
  <>
    <h1>Welcome to Your Site</h1>
    <p>This is the middle content area.</p>
  </>
);

function App() {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Layout />,
      children: [
        { path: '', element: <Home /> },           // Use empty path for index route
        { path: 'login', element: <Login /> },     // No leading slash
        { path: 'signup', element: <SignUp /> },   // No leading slash
      ],
    },
  ]);

  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
