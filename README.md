# Yangon Rental Price Analysis & Prediction 

An end-to-end data science and machine learning project that scrapes rental property data in **Yangon, Myanmar**, performs **exploratory data analysis (EDA)**, trains multiple **regression models**, and deploys a **full-stack web application** using **Docker** and **AWS Elastic Beanstalk**.
<img width="1470" height="956" alt="Screenshot 2025-12-15 at 9 45 08 PM" src="https://github.com/user-attachments/assets/4dbd466b-e3df-4eb1-bffc-28013fc21dc7" />



## Project Overview

This project focuses on understanding rental prices across different townships in Yangon and building a machine learning model to predict rental prices based on property characteristics.

**Key stages:**
1. Web Scraping (Playwright)
2. Data Cleaning & EDA
3. Machine Learning Model Training
4. Full-stack Deployment (React + Flask)
5. Docker & AWS Elastic Beanstalk Deployment
---

## Project Documentation
- For a more detailed explanation of the project workflow, data processing steps, model training, and deployment, **please check the [project documentation](docs/Project_Documentation.pdf) included in this repository.**
---

## 1. Web Scraping (Playwright)

- **Source**: `https://www.propertiesinyangon.com/rent`
- **Tool Used**: Playwright  
- **Why Playwright?**
  - Handles dynamic JavaScript-rendered pages
  - Supports automatic scrolling
  - Reliable for large-scale scraping
    

### Scraping Process
- Navigated to the **Rent** listings page
- Automatically scrolled to load all listings
- Extracted:
  - Property ID
  - Property type
  - Township
  - Bedrooms
  - Property size
  - Rental price
- Total scraping time: **~1 hour**
- Output saved as a **JSON file**

---

## 2. Exploratory Data Analysis (EDA)

### 2.1 Data Loading & Cleaning
- Loaded scraped JSON data
- Selected relevant columns:
  - `property_type`
  - `township`
  - `bedrooms`
  - `property_size`
  - `price`
- Handling missing values:
  - Dropped rows without property size
  - Filled missing bedroom values with `0`

---

### 2.2 Data Transformation

#### Property Size
- Removed `ft²`
- Converted ranges (e.g. `400 to 710 ft²`) → **average value**

#### Price
- Removed rows with:
  - `"Contact for price"`
  - `"for sale"`
- Cleaned text (`$`, `,`, `/Month`)
- Converted price ranges (e.g. `$2,000 - $3,700`) → **average value**

#### Property Type
- Standardized categories  
  - Example: `"Condo, Penthouse"` → `"Penthouse"`
- Removed rare categories (< 10 samples)

#### Township
- Removed rare townships (< 10 samples) to reduce class imbalance

---

### 2.3 Data Exploration

#### Numerical Features
- `property_size`
- `bedrooms`
- `price`

Visualizations:
- KDE plots to observe distributions and outliers

#### Categorical Features
- `township`
- `property_type`

Visualizations:
- Count plots to analyze frequency and imbalance

---

### 2.4 Relationship Analysis

- **Boxplots**
  - `property_type` vs `price`
  - `township` vs `price`
- **Scatterplots**
  - `property_size` vs `price`
  - `bedrooms` vs `price`
- **Correlation Analysis**
  - Between `price`, `property_size`, and `bedrooms`

---

## 3. Machine Learning Model Training

### Data Preparation
- Loaded processed CSV
- Removed price outliers (top & bottom **5%**)
- Target variable: `y = price`
- Features: property details
- Applied **log transformation** to price

---

### Feature Engineering
- Numerical features → `StandardScaler`
- Categorical features → `OneHotEncoder`
- Combined using `ColumnTransformer`
- Train-test split: **80% / 20%**

---

### Models Trained
- Linear Regression
- Ridge Regression
- Lasso Regression
- Decision Tree
- Random Forest
- AdaBoost
- K-Nearest Neighbors (KNN)
- Support Vector Regression (SVR)

---

### Evaluation Metrics
- **R²**
- **MAE**
- **Median Absolute Error**
- **RMSE**

### Best Model
**Random Forest Regressor**
- **R²**: 0.57  
- **MAE**: 0.28  
- **RMSE**: 0.35  

---

## 4. Full-Stack Application

### Backend
- **Flask API**
- Served using **Gunicorn**
- Exposes prediction endpoint

### Frontend
- **React**
- Built and served using **Nginx**
- Communicates with backend via `/api`

---

## 5. Docker Setup

This project uses **Docker Compose** to run frontend and backend together.

### Build and Run

1. **Clone the repository**
```bash
git clone <https://github.com/EiPhyuSinn/Data_science_end_to_end/>
cd <real_estate_app>
```
2. **Start containers**
```bash
docker-compose up
```
3. **Access the app**
```bash
Frontend: http://localhost:80
Backend API: http://localhost:5000/api
```

3. **Stop containers**
```bash
docker-compose down
```

## 6. Cloud Deployment

- Deployed using AWS Elastic Beanstalk

- Dockerized multi-container setup

- Nginx serves frontend

- Flask API handles predictions

## Tech Stack

- Scraping: Playwright

- EDA & ML: Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn

- Backend: Flask, Gunicorn

- Frontend: React, Nginx

- Containerization: Docker, Docker Compose

- Cloud: AWS Elastic Beanstalk

## Future Improvements

- Add more recent rental data

- Improve model performance with XGBoost / LightGBM

- Add map-based visualization

- Implement user authentication

- Add CI/CD pipeline
