// src/components/Navbar.js

import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

const Navbar = () => {
  const { user, loadingUser } = useContext(AuthContext);

  const getUserAvatarText = () => {
    if (!user || !user.first_name) return '';
    return user.first_name[0].toUpperCase();
  };

  if (loadingUser) {
    return (
      <nav style={navStyle}>
        <div style={{ color: 'white' }}>Loading user info...</div>
      </nav>
    );
  }

  return (
    <nav style={navStyle}>
      <div>
        <Link to="/" style={linkStyle}>
          Shopy
        </Link>
      </div>

      <ul style={navListStyle}>
        <li><Link to="/" style={linkStyle}>Home</Link></li>
        <li><Link to="/cart" style={linkStyle}>Cart</Link></li>
        <li><Link to="/order" style={linkStyle}>Order</Link></li>
        <li><Link to="/wishlist" style={linkStyle}>Wishlist</Link></li>
      </ul>

      <form
        onSubmit={e => {
          e.preventDefault();
          alert(`Search for: ${e.target.search.value}`);
        }}
      >
        <input
          type="text"
          name="search"
          placeholder="Search products..."
          style={searchInputStyle}
        />
        <button type="submit" style={searchButtonStyle}>Search</button>
      </form>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {!user ? (
          <>
            <button style={loginButtonStyle}>
              <Link to="/login" style={linkStyle}>Login</Link>
            </button>
            <button style={signupButtonStyle}>
              <Link to="/signup" style={{ ...linkStyle, color: '#282c34' }}>SignUp</Link>
            </button>
          </>
        ) : (
          <>
            {user.profile_photo_url ? (
              <img
                src={user.profile_photo_url}
                alt="User Avatar"
                style={avatarImageStyle}
              />
            ) : (
              <div style={avatarFallbackStyle}>{getUserAvatarText()}</div>
            )}
            <span style={{ fontWeight: 'bold', color: 'white' }}>{user.first_name}</span>
          </>
        )}
      </div>
    </nav>
  );
};

// Styles (same as in your original)
const navStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  backgroundColor: '#282c34',
  padding: '10px 20px',
  color: 'white',
  position: 'sticky',
  top: 0,
  zIndex: 1000,
};

const navListStyle = {
  listStyle: 'none',
  padding: 0,
  margin: 0,
  display: 'flex',
  gap: '2rem',
};

const linkStyle = {
  color: 'white',
  textDecoration: 'none',
};

const searchInputStyle = {
  borderRadius: '4px 0 0 4px',
  border: 'none',
  padding: '5px 10px',
  outline: 'none',
  width: '200px',
};

const searchButtonStyle = {
  borderRadius: '0 4px 4px 0',
  border: 'none',
  padding: '5px 10px',
  cursor: 'pointer',
  backgroundColor: '#61dafb',
  color: '#282c34',
  fontWeight: 'bold',
};

const loginButtonStyle = {
  marginRight: '10px',
  backgroundColor: 'transparent',
  border: '1px solid white',
  color: 'white',
  borderRadius: '4px',
  padding: '5px 10px',
  cursor: 'pointer',
};

const signupButtonStyle = {
  backgroundColor: '#61dafb',
  border: 'none',
  borderRadius: '4px',
  padding: '5px 10px',
  cursor: 'pointer',
  fontWeight: 'bold',
  color: '#282c34',
};

const avatarImageStyle = {
  width: '40px',
  height: '40px',
  borderRadius: '50%',
};

const avatarFallbackStyle = {
  width: '40px',
  height: '40px',
  borderRadius: '50%',
  backgroundColor: '#61dafb',
  color: '#282c34',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  fontWeight: 'bold',
  fontSize: '1.25rem',
  userSelect: 'none',
};

export default Navbar;
