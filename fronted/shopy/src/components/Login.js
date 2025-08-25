import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [tempId, setTempId] = useState(null);
  const [otpSent, setOtpSent] = useState(false);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSendOtp = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`http://localhost:8000/auth/login/send-otp?purpose=login`, { email });
      setTempId(response.data.temp_id);
      setOtpSent(true);
      setMessage(response.data.message);
    } catch (error) {
      let errorMsg = 'Try again';
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          errorMsg = error.response.data.detail.map(d => d.msg || JSON.stringify(d)).join(', ');
        } else if (typeof error.response.data.detail === 'string') {
          errorMsg = error.response.data.detail;
        } else {
          errorMsg = JSON.stringify(error.response.data.detail);
        }
      }
      setMessage('Failed to send OTP: ' + errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    setLoading(true);
    try {
      // Verify OTP first
      await axios.post('http://localhost:8000/auth/login/verify-otp', {
        temp_id: tempId,
        otp,
      });

      // Assuming backend returns token on verification or a next API call after verify
      // Example: backend returns { access_token: '...' } after OTP verify
      const tokenResponse = await axios.post('http://localhost:8000/auth/login-with-temp-id', {
        temp_id: tempId,
        flag: "is_otp_verified"  // Must match exactly
      });

      const token = tokenResponse.data.access_token;
      localStorage.setItem('token', token);  // <== Save token here

      setMessage('Login successful!');
      setTimeout(() => {
        setLoading(false);
        navigate('/');
      }, 1000);
    } catch (error) {
      setLoading(false);
      setMessage('Invalid OTP. Please try again.');
    }
  };


  const handleResendOtp = () => {
    setOtp('');
    setMessage('');
    handleSendOtp();
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '100vh', position: 'relative' }}>
      {loading && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(255,255,255,0.7)',
          zIndex: 1050,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          <div className="spinner-border text-primary" role="status" aria-hidden="true"></div>
        </div>
      )}

      <div className="card shadow-lg p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <div className="text-center mb-4">
          <img src="/favicon.png" alt="favicon" width="60" className="mb-2" />
          <h4 className="fw-bold mb-1">Login to Shopy</h4>
          <small className="text-muted">Secure OTP-based login</small>
        </div>

        {!otpSent ? (
          <>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">Email address</label>
              <input
                type="email"
                className="form-control"
                id="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                disabled={loading}
              />
            </div>
            <button className="btn btn-primary w-100 mb-3" onClick={handleSendOtp} disabled={loading}>Send OTP</button>
          </>
        ) : (
          <>
            <div className="mb-3">
              <label htmlFor="otp" className="form-label">Enter OTP</label>
              <input
                type="text"
                className="form-control"
                id="otp"
                value={otp}
                onChange={e => setOtp(e.target.value)}
                maxLength={6}
                disabled={loading}
              />
            </div>
            <button className="btn btn-success w-100 mb-2" onClick={handleVerifyOtp} disabled={loading}>Verify OTP</button>
            <button className="btn btn-outline-secondary w-100 mb-3" onClick={handleResendOtp} disabled={loading}>Resend OTP</button>
          </>
        )}

        {message && (
          <div className="alert alert-info text-center py-2 mb-0">{message}</div>
        )}

        <p>
          Create Account?
          <Link to="/signup" style={{ marginLeft: "5px", textDecoration: 'none' }}>Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
