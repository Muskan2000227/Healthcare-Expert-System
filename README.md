# 🏥 HealthCare Expert System

A web-based **Django** application integrating **Machine Learning models** for **symptom-based diagnosis**, **disease risk prediction**, **personalized health recommendations**, and **interactive chatbot** support. This system offers multiple health-related tools, including calculators, health predictions, and tests for common disorders like anxiety and depression.

---

## 📌 Key Features

### 🧠 Health Tools & Predictions:
- **Interactive Human Body Diagram**: Click on any organ to get a list of symptoms, possible diseases, and treatment options.
- **Health Calculators**:
  - BMI (Body Mass Index)
  - BMR (Basal Metabolic Rate)
  - Diabetes Risk Calculator
  - Hydration Calculator
- **Health Predictions**:
  - Disease Prediction based on symptoms and historical data.
  - Disorder Prediction (e.g., mental health issues like anxiety and depression).
  - Health Expenses Prediction based on user health conditions.

### 💊 Vitamins, Supplements, and Drugs Search:
- **Search by Alphabet or Field**: Find vitamins, supplements, or drugs by their name or by entering specific health conditions.
  
### 🩺 Health Tests:
- **Anxiety Test**
- **Depression Test**

### 🔄 User Profile:
- **Login Options**: Use Google login or manual login.
- **Profile Management**: Edit profile details, including health-related information.

### 🧑‍💼 Machine Learning Models:
- Convolutional Neural Network (CNN) for lung cancer detection.
- Decision Tree for disease classification and health risk prediction.
- SARIMAX for time-series forecasting of health trends.

---

## 🚀 Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, JQuery
- **Database**: MySQL
- **Machine Learning**: scikit-learn, TensorFlow/Keras, statsmodels
- **Authentication**: Google OAuth 2.0 for Google login
- **Others**: Bootstrap (UI), jQuery (interactivity)

---

## ⚙️ Getting Started

Run the following commands to set up and start the project locally:

```bash
# Clone the repository
git clone https://github.com/yourusername/Healthcare.git
cd Healthcare

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
