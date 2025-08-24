import React, { useState } from 'react';
import { Link } from 'react-router-dom';




const Navbar = () => {


  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    // Implement search functionality or redirect
    alert(`Search for: ${searchTerm}`);
  };

  return (
    <nav style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      backgroundColor: '#282c34',
      padding: '10px 20px',
      color: 'white',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
    }}>
      {/* App Logo */}
      <div>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Shopy</Link>

      </div>

      {/* Navigation Links */}
      <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', gap: '2rem' }}>
      <li>
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
          <i className="bi bi-house me-1"></i>
          Home
        </Link>
      </li>
      <li>
        <Link to="/cart" style={{ color: 'white', textDecoration: 'none' }}>
          <i className="bi bi-cart me-1"></i>
          Cart
        </Link>
      </li>
      <li>
        <Link to="/order" style={{ color: 'white', textDecoration: 'none' }}>
          <i className="bi bi-box-seam me-1"></i>
          Order
        </Link>
      </li>
      <li>
        <Link to="/wishlist" style={{ color: 'white', textDecoration: 'none' }}>
          <i className="bi bi-heart me-1"></i>
          Wishlist
        </Link>
      </li>
    </ul>


      {/* Search Bar */}
      <form onSubmit={handleSearchSubmit}>
        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          onChange={handleSearchChange}
          style={{
            borderRadius: '4px 0 0 4px',
            border: 'none',
            padding: '5px 10px',
            outline: 'none',
            width: '200px',
          }}
        />
        <button type="submit" style={{
          borderRadius: '0 4px 4px 0',
          border: 'none',
          padding: '5px 10px',
          cursor: 'pointer',
          backgroundColor: '#61dafb',
          color: '#282c34',
          fontWeight: 'bold',
        }}>
          Search
        </button>
      </form>

      {/* Profile / Auth Buttons */}
      <div>
        <button style={{
          marginRight: '10px',
          backgroundColor: 'transparent',
          border: '1px solid white',
          color: 'white',
          borderRadius: '4px',
          padding: '5px 10px',
          cursor: 'pointer',
        }}>
          <Link to="/login/" style={{ color: 'white', textDecoration: 'none' }}>Login</Link>

        </button>
        <button style={{
          backgroundColor: '#61dafb',
          border: 'none',
          borderRadius: '4px',
          padding: '5px 10px',
          cursor: 'pointer',
          fontWeight: 'bold',
          color: '#282c34',
        }}>
          Sign Up
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
