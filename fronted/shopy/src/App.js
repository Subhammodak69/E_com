import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
  return (
    <div className="App" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />

      <main style={{ flex: '1', padding: '20px' }}>
        {/* Your middle content goes here */}
        <h1>Welcome to Your Site</h1>
        <p>This is the middle content area.</p>
      </main>

      <Footer />
    </div>
  );
}

export default App;
