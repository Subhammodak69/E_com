import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

const navLinkStyles = ({ isActive }) => ({
  color: isActive ? '#61dafb' : 'white',
  textDecoration: 'none',
  fontWeight: isActive ? 'bold' : 'normal',
  margin: '0 10px',
  padding: '5px 10px',
  borderRadius: '4px',
  backgroundColor: isActive ? 'rgba(97, 218, 251, 0.2)' : 'transparent',
});

const Navbar = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (e) => setSearchTerm(e.target.value);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    // Add search handler logic here, e.g., navigate or filter
    alert(`Searching for: ${searchTerm}`);
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
      {/* Logo */}
      <div>
        <NavLink to="/" style={{ color: 'white', fontSize: '24px', fontWeight: 'bold', textDecoration: 'none' }}>
          Shopy
        </NavLink>
      </div>

      {/* Navigation Links */}
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <NavLink to="/" style={navLinkStyles} end>Home</NavLink>
        <NavLink to="/cart" style={navLinkStyles}>Cart</NavLink>
        <NavLink to="/order" style={navLinkStyles}>Order</NavLink>
        <NavLink to="/wishlist" style={navLinkStyles}>Wishlist</NavLink>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearchSubmit} style={{ display: 'flex' }}>
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

      {/* Profile/Login Buttons */}
      <div style={{ marginLeft: '20px' }}>
        <button style={{
          marginRight: '10px',
          backgroundColor: 'transparent',
          border: '1px solid white',
          color: 'white',
          borderRadius: '4px',
          padding: '5px 10px',
          cursor: 'pointer',
        }}>
          Log In
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
