import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';

const SignUp = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    middle_name: '',
    last_name: '',
    email: '',
    phone: '',
    gender: '',
  });
  const [otp, setOtp] = useState('');
  const [tempId, setTempId] = useState(null);
  const [otpVerified, setOtpVerified] = useState(false);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const resetForm = () => {
    setTempId(null);
    setOtp('');
    setOtpVerified(false);
    setMessage('');
    setFormData({
      first_name: '',
      middle_name: '',
      last_name: '',
      email: '',
      phone: '',
      gender: '',
    });
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendOtp = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/users/send-otp', formData);
      setTempId(response.data.temp_id);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Could not send OTP. ' + (error.response?.data?.detail || 'Try again.'));
    } finally {
      setLoading(false);
    }
  };

  // New function to perform signup after OTP verification success
  const performSignUp = async () => {
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/users/', {
        ...formData,
        otp_verified: true,  // Signal that OTP was verified
      });
      setMessage('Signup complete!');
      setTimeout(() => {
        setLoading(false);
        navigate('/login');
      }, 1000);
    } catch (error) {
      setLoading(false);
      setMessage('Signup failed. ' + (error.response?.data?.detail || 'Try again.'));
    }
  };




  const handleVerifyOtp = async () => {
    setLoading(true);
    console.log(tempId, "tempId");
    console.log(otp, "otp");
    try {
      const response = await axios.post(
        'http://localhost:8000/users/verify-otp?purpose=signup',
        {
          temp_id: tempId,
          otp: otp,
        }
      );

      setMessage(response.data.message);
      setOtpVerified(true);

      // After successful OTP verification, automatically call signup
      await performSignUp();

      setLoading(false);  // Stop loading after signup completes
    } catch (error) {
      setMessage('Invalid OTP. Please try again.');
      setTimeout(() => {
        setLoading(false);
        resetForm();
      }, 1000);
    }
  };


  const handleResendOtp = () => {
    handleSendOtp();
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '100vh', position: 'relative' }}>
      {loading && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          backgroundColor: 'rgba(53, 153, 215, 0.28)',
          zIndex: 1050,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          <div className="spinner-border text-primary" role="status" aria-hidden="true"></div>
        </div>
      )}

      <div className="card shadow-lg p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <div className="text-center mb-3">
          <img src="/favicon.png" alt="logo" width="60" className="mb-2" />
          <h4 className="fw-bold mb-1">Create Your Account</h4>
          <small className="text-muted">Join Shopy with a few details</small>
        </div>
        {!tempId ? (
          <>
            <div className="mb-2 d-flex" style={{ gap: "10px" }}>
              <input
                type="text"
                name="first_name"
                className="form-control"
                value={formData.first_name}
                onChange={handleChange}
                placeholder='First name'
                required
                disabled={loading}
              />
              <input
                type="text"
                name="middle_name"
                className="form-control"
                value={formData.middle_name}
                onChange={handleChange}
                placeholder='Middle name'
                disabled={loading}
              />
            </div>
            <div className="mb-2 d-flex" style={{ gap: "10px" }}>
              <input
                type="text"
                name="last_name"
                className="form-control"
                value={formData.last_name}
                onChange={handleChange}
                required
                placeholder='Last name'
                disabled={loading}
              />
              <select
                className="form-select"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
                disabled={loading}
              >
                <option value="">Select Gender</option>
                <option value="1">Male</option>
                <option value="2">Female</option>
                <option value="3">Others</option>
              </select>
            </div>
            <div className="mb-2">
              <input
                type="email"
                name="email"
                className="form-control"
                value={formData.email}
                onChange={handleChange}
                required
                placeholder='Enter your Email'
                disabled={loading}
              />
            </div>
            <div className="mb-2">
              <input
                type="tel"
                name="phone"
                className="form-control"
                value={formData.phone}
                onChange={handleChange}
                placeholder='Enter your phone no'
                disabled={loading}
              />
            </div>
            <button className="btn btn-primary w-100 mb-2" onClick={handleSendOtp} disabled={loading}>
              Send OTP
            </button>
          </>
        ) : !otpVerified ? (
          <>
            <div className="mb-3">
              <input
                type="text"
                className="form-control"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="Enter OTP"
                disabled={loading}
              />
            </div>
            <button className="btn btn-success w-100 mb-2" onClick={handleVerifyOtp} disabled={loading}>
              Verify OTP
            </button>
            <button className="btn btn-primary w-100 mb-2" onClick={handleResendOtp} disabled={loading}>
              Resend OTP
            </button>
          </>
        ) : (
          // Remove manual Sign Up button since signup is automatic after OTP verification
          <>
            <div className="alert alert-success text-center py-2 mb-0">Signing up...</div>
          </>
        )}
        {message && (
          <div className="alert alert-info text-center py-2 mt-2 mb-0">
            {message}
          </div>
        )}
        <div className="text-center mt-3">
          Already have an account?
          <Link to="/login" className="ms-1" style={{ textDecoration: 'none' }}>
            Login
          </Link>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
