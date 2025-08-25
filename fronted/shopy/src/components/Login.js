import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [message, setMessage] = useState('');

  const handleSendOtp = () => {
    // Dummy logic
    setOtpSent(true);
    setMessage('OTP sent to your email.');
  };

  const handleVerifyOtp = () => {
    // Dummy logic
    if (otp === '1234') {
      setMessage('OTP verified successfully!');
    } else {
      setMessage('Invalid OTP. Try again.');
    }
  };

  const handleResendOtp = () => {
    setOtp('');
    setMessage('OTP resent to your email.');
  };

  return (
    <div className="container d-flex justify-content-center align-items-center ">
      <div className="card shadow-lg p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <div className="text-center mb-4">
          <img src="/favicon.png" alt="favicon" width="60" className="mb-2" />
          <h4 className="fw-bold mb-1">Login to Shopy</h4>
          <small className="text-muted">Secure OTP-based login</small>
        </div>
        {!otpSent && (
        <div className="mb-3">
          <label htmlFor="email" className="form-label">Email address</label>
          <input
            type="email"
            className="form-control"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={otpSent}
            required
          />
        </div>
        )
        }

        {!otpSent && (
          <button className="btn btn-primary w-100 mb-3" onClick={handleSendOtp}>
            Send OTP
          </button>
        )}

        {otpSent && (
          <>
            <div className="mb-3">
              <label htmlFor="otp" className="form-label">Enter OTP</label>
              <input
                type="text"
                className="form-control"
                id="otp"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength={6}
              />
            </div>

            <button className="btn btn-success w-100 mb-2" onClick={handleVerifyOtp}>
              Verify OTP
            </button>

            <button className="btn btn-outline-secondary w-100 mb-3" onClick={handleResendOtp}>
              Resend OTP
            </button>
          </>
        )}

        {message && (
          <div className="alert alert-info text-center py-2 mb-0">
            {message}
          </div>
        )}
        <p>Create Account ? 
        <Link to="/Signup/" style={{ marginLeft: "5px" ,textDecoration: 'none' }}>Sign Up</Link>

        </p>
      </div>
    </div>
  );
};

export default Login;
