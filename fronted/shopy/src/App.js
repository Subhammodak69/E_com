import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Login from './components/Login';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import SignUp from './components/Signup';

const Layout = () => {
  // This layout wraps Navbar, Footer, and outlet for nested routes inside main
  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <main style={{display:"flex", flex:1, padding: '20px', minHeight:"90vh", transition:"ease-in" }}>
        <Outlet /> {/* renders the matched child route element here */}
      </main>
      <Footer />
    </div>
  );
};

const Home = () => (
  <>
    <h1>Welcome to Your Site</h1>
    <p>This is the middle content area.</p>
  </>
);

function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Layout />, // Wrap Navbar/Footer/Layout here
      children: [
        {
          path: "/",
          element: <Home />,
        },
        {
          path: "/login/",
          element: <Login />,
        },
        {
          path: "/signup/",
          element: <SignUp />,
        },
        // Add more routes here if needed
      ],
    },
  ]);

  return <RouterProvider router={router} />;
}

export default App;
