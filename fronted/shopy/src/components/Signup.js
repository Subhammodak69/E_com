import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSendOtp = async () => {
    try {
      const response = await axios.post('http://localhost:8000/users/send-otp?purpose=signup', formData)
      setTempId(response.data.temp_id);
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Could not send OTP. ' + (error.response?.data?.detail || 'Try again.'));
    }
  };

  const handleVerifyOtp = async () => {
    try {
      const response = await axios.post('http://localhost:8000/users/verify-otp', {
        temp_id: tempId,
        otp: otp,
      });

      setMessage(response.data.message);
      setOtpVerified(true);
    } catch (error) {
      setMessage('Invalid OTP. Please try again.');
    }
  };

  const handleResendOtp = async () => {
    handleSendOtp();
  };

  const handleSignUp = async () => {
    try {
      const response = await axios.post('http://localhost:8000/users/', {
        ...formData,
        temp_id: tempId,
        otp_input: otp,
      });
      setMessage('Signup complete!');
    } catch (error) {
      setMessage('Signup failed. ' + (error.response?.data?.detail || 'Try again.'));
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" >
      <div className="card shadow-lg p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <div className="text-center mb-3">
          <img src="/favicon.png" alt="logo" width="60" className="mb-2" />
          <h4 className="fw-bold mb-1">Create Your Account</h4>
          <small className="text-muted">Join Shopy with a few details</small>
        </div>
        {!tempId ? (
          <>
            {/* Show fields and send OTP button */}
            <div className="mb-2 d-flex " style={{ gap: "10px" }}>
              <input
                type="text"
                name="first_name"
                className="form-control"
                value={formData.first_name}
                onChange={handleChange}
                placeholder='First name'
                required
              />
              <input
                type="text"
                name="middle_name"
                className="form-control"
                value={formData.middle_name}
                onChange={handleChange}
                placeholder='Middle name'
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
              />
              <select
                className="form-select"
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
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
              />
            </div>
            <button className="btn btn-primary w-100 mb-2" onClick={handleSendOtp}>
              Send OTP
            </button>
          </>
        ) : !otpVerified ? (
          <>
            {/* Show OTP input, verify and resend buttons */}
            <div className="mb-3">
              <input
                type="text"
                className="form-control"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="Enter OTP"
              />
            </div>
            <button className="btn btn-success w-100 mb-2" onClick={handleVerifyOtp}>
              Verify OTP
            </button>
            <button className="btn btn-primary w-100 mb-2" onClick={handleResendOtp}>
              Resend OTP
            </button>
          </>
        ) : (
          <>
            {/* Show signup button only after OTP verification */}
            <button className="btn btn-primary w-100 mb-2" onClick={handleSignUp}>
              Sign Up
            </button>
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
