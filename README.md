# 🛡️ AI-Powered Phishing Website Detection System
**Developed by:** [Nutt Worrawalunup] | Computer Science Student (GPAX 4.00)

## 📌 Project Overview
ระบบคัดแยกเว็บไซต์หลอกลวง (Phishing) โดยใช้ Machine Learning เพื่อเพิ่มความปลอดภัยในการใช้งานอินเทอร์เน็ต ระบบสามารถวิเคราะห์ปัจจัยทางเทคนิคของ URL และตัดสินใจความเสี่ยงได้โดยอัตโนมัติ

## ⚙️ System Architecture (SA Perspective)
ระบบถูกออกแบบมาในรูปแบบ **End-to-End Application**:
1. **Data Layer**: ใช้ฐานข้อมูลจาก Kaggle (5,000+ records) มีฟีเจอร์วิเคราะห์ 48 ปัจจัย
2. **Logic Layer**: ประมวลผลด้วยอัลกอริทึม **Random Forest Classifier** (Accuracy > 90%)
3. **Presentation Layer**: พัฒนา User Interface ด้วย **Streamlit** เพื่อให้ผู้ใช้ทั่วไปใช้งานได้ง่าย

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Library:** Pandas, Scikit-learn, Joblib
- **Framework:** Streamlit (Frontend & Deployment)
- **Model:** Random Forest (Ensemble Learning)

## 📊 Key Indicators Analyzed
ระบบวิเคราะห์ปัจจัยสำคัญ เช่น:
- URL Length & Depth
- HTTPS Status (NoHttps)
- Domain Presence in Subdomains
- Presence of Sensitive Words

## 🚀 How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `streamlit run app.py`
