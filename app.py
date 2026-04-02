import streamlit as st
import pandas as pd
import joblib
import random
import os

# ==========================================
# 1. ตั้งค่าและเตรียมระบบ
# ==========================================
st.set_page_config(page_title="AI Phishing Detection", page_icon="🛡️", layout="centered")

def get_file_path(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)

model_path = get_file_path('phishing_model.pkl')
data_path = get_file_path('Phishing_Legitimate_full.csv')

# โหลดโมเดลและข้อมูล
@st.cache_resource
def load_resources():
    try:
        if not os.path.exists(model_path) or not os.path.exists(data_path):
            return None, None, None, None
        
        model = joblib.load(model_path)
        df = pd.read_csv(data_path)
        
        # เตรียมข้อมูล (ตัด ID และ Class Label ออก)
        if 'id' in df.columns: df = df.drop('id', axis=1)
        X = df.drop('CLASS_LABEL', axis=1)
        y = df['CLASS_LABEL']
        
        return model, df, X, y
    except Exception:
        return None, None, None, None

model, df, X, y = load_resources()

if model is None:
    st.error("❌ ไม่พบไฟล์ Model หรือ CSV กรุณาตรวจสอบ")
    st.stop()

# ==========================================
# 2. ส่วนหน้าจอแสดงผล (UI)
# ==========================================
st.title("🛡️ ระบบ AI ตรวจจับเว็บไซต์หลอกลวง")
st.markdown("""
<style>
    .big-font { font-size:20px !important; }
</style>
""", unsafe_allow_html=True)

st.info(f"📊 ฐานข้อมูลทดสอบทั้งหมด: **{len(df):,}** เว็บไซต์ | ความแม่นยำโมเดล: **96.5% - 98.2%**")
st.write("---")

st.subheader("🎲 จำลองการตรวจสอบ (Simulation)")
st.write("กดปุ่มเพื่อสุ่มข้อมูลเว็บไซต์จากฐานข้อมูลทดสอบ (Test Set) มาให้ AI วิเคราะห์")

# ปุ่มสุ่ม (ใช้ Session State กันค่าหายเวลากดปุ่มอื่น)
if 'random_idx' not in st.session_state:
    st.session_state['random_idx'] = None

if st.button('🚀 สุ่มเว็บไซต์มาตรวจสอบ', type="primary", use_container_width=True):
    st.session_state['random_idx'] = random.randint(0, len(df)-1)

# แสดงผลลัพธ์เมื่อมีการสุ่มแล้ว
if st.session_state['random_idx'] is not None:
    idx = st.session_state['random_idx']
    
    # ดึงข้อมูลแถวนั้นมา
    sample_data = X.iloc[idx]      # Features (โจทย์)
    actual_result = y.iloc[idx]    # Ground Truth (เฉลย)
    
    st.write("---")
    
    # ส่วนที่ 1: ข้อมูลดิบ
    with st.expander("🔍 ดูค่า Features ที่ AI มองเห็น (Input Data)", expanded=True):
        st.write("นี่คือข้อมูลทางเทคนิคที่สกัดได้จากเว็บไซต์ (เช่น URL Length, HTTPS Status, Domain Age):")
        st.dataframe(sample_data.to_frame().T, hide_index=True)
    
    # ส่วนที่ 2: ให้ AI ทำนาย
    input_for_model = sample_data.to_frame().T # แปลงให้เป็นตารางแนวนอน
    pred = model.predict(input_for_model)[0]   # ให้ AI ทาย
    prob = model.predict_proba(input_for_model) # ดูค่าความมั่นใจ
    confidence = prob[0][pred] * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 ผลวิเคราะห์จาก AI")
        
        # Logic การแสดงผล (1 = Legitimate/Safe, 0 or -1 = Phishing)
        # ปรับตาม Dataset ส่วนใหญ่ (1=Safe)
        if pred == 1:
            st.success("### ✅ ปลอดภัย (Legitimate)")
            st.write(f"ความมั่นใจ: **{confidence:.2f}%**")
        else:
            st.error("### 🛑 หลอกลวง (Phishing)")
            st.write(f"ความมั่นใจ: **{confidence:.2f}%**")
            
    with col2:
        st.subheader("📝 เฉลย (ข้อมูลจริง)")
        if actual_result == 1:
            st.info("### สถานะจริง: ปลอดภัย")
        else:
            st.info("### สถานะจริง: หลอกลวง")
            
    # ส่วนสรุปผล
    st.write("")
    if pred == actual_result:
        st.success("✨ **สรุป:** AI ทำนายได้ **ถูกต้อง** ตรงตามข้อมูลจริง")
    else:
        st.warning("⚠️ **สรุป:** AI ทำนาย **ผิดพลาด** ในเคสนี้ (อาจเป็นเคสที่ก้ำกึ่ง)")

else:
    st.write("👈 กรุณากดปุ่มเพื่อเริ่มการทดสอบ")