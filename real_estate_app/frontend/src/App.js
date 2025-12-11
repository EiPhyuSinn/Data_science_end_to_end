import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    property_type: 'Condo',
    township: 'Kamayut',
    bedrooms: 3,
    property_size: 2000
  });
  
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const townships = ['Golden Valley','Thanlyin', 'South Okkalapa','Yankin', 'Downtown','Hlaing', 'Hlaingthaya','Mingalar taung Nyunt', 'Ahlone','Yawmingyi','Mayangone', 'Kamayut', 'Bahan', 'Sanchaung', 'Tamwe', 'Thingangyun'];
  const propertyTypes = ['Condo', 'Penthouse', 'House', 'Apartment','Commercial','Serviced Apartment'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'bedrooms' || name === 'property_size' ? Number(value) : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPrediction(null);

    try {
      // Use proxy (no need for full URL)
      const response = await axios.post('/api/predict', formData);
      
      if (response.data.success) {
        setPrediction(response.data);
      } else {
        setError(response.data.error || 'Prediction failed');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Backend connection failed. Make sure Flask is running on port 5000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🏠 Yangon Real Estate Price Predictor</h1>
        <p>AI-powered property price estimation</p>
      </header>

      <div className="container">
        <div className="form-card">
          <h2>📋 Enter Property Details</h2>
          
          <form onSubmit={handleSubmit} className="prediction-form">
            <div className="form-group">
              <label>Property Type</label>
              <select 
                name="property_type"
                value={formData.property_type}
                onChange={handleChange}
                className="form-control"
              >
                {propertyTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Township</label>
              <select 
                name="township"
                value={formData.township}
                onChange={handleChange}
                className="form-control"
              >
                {townships.map(town => (
                  <option key={town} value={town}>{town}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Bedrooms</label>
              <input
                type="number"
                name="bedrooms"
                value={formData.bedrooms}
                onChange={handleChange}
                min="1"
                max="10"
                className="form-control"
              />
            </div>

            <div className="form-group">
              <label>Property Size (sqft)</label>
              <input
                type="number"
                name="property_size"
                value={formData.property_size}
                onChange={handleChange}
                min="500"
                max="10000"
                className="form-control"
              />
            </div>

            <button 
              type="submit" 
              className="submit-btn"
              disabled={loading}
            >
              {loading ? 'Predicting...' : '💰 Get Price Estimate'}
            </button>

            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}
          </form>

          {prediction && (
            <div className="result-card">
              <div className="result-header">
                <h3>✅ Price Estimate</h3>
                <span className="badge">AI Prediction</span>
              </div>
              
              <div className="price-display">
                <div className="currency">{prediction.currency}</div>
                <div className="price">${prediction.prediction.toLocaleString()}</div>
              </div>

              <div className="property-details">
                <h4>Property Details:</h4>
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="detail-label">Type:</span>
                    <span className="detail-value">{prediction.input_details.property_type}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Township:</span>
                    <span className="detail-value">{prediction.input_details.township}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Bedrooms:</span>
                    <span className="detail-value">{prediction.input_details.bedrooms}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Size:</span>
                    <span className="detail-value">{prediction.input_details.property_size}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;