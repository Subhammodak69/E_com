import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loadingUser, setLoadingUser] = useState(true);

  const fetchCurrentUser = async () => {
    const token = localStorage.getItem('token');
    console.log("DEBUG: Retrieved token from localStorage:", token);

    if (!token) {
      console.log("DEBUG: No token found, user set to null");
      setUser(null);
      setLoadingUser(false);
      return;
    }

    try {
      console.log("DEBUG: Making API call to /users/me with token");
      const response = await axios.get('http://localhost:8000/auth/me', {
        headers: { Authorization: `Bearer ${token}` },
      });
      console.log("DEBUG: API response received:", response.data);
      setUser(response.data);
    } catch (error) {
      console.error("DEBUG: Error fetching /users/me:", error);

      // Log detailed error response if available
      if (error.response) {
        console.error("DEBUG: API error status:", error.response.status);
        console.error("DEBUG: API error data:", error.response.data);
      }
      
      localStorage.removeItem('token');
      setUser(null);
    }
    setLoadingUser(false);
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, loadingUser }}>
      {children}
    </AuthContext.Provider>
  );
};
