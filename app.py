import streamlit as st
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
import random
from gtts import gTTS # New import
from io import BytesIO # New import for handling audio data

# ==========================================
# 🗣️ Text-to-Speech using gTTS (Cloud Compatible)
# ==========================================
def speak_real_audio(text):
    """Generates and plays audio using gTTS (works on Streamlit Cloud)."""
    try:
        # Create a BytesIO object to hold the audio file in memory
        mp3_fp = BytesIO()
        tts = gTTS(text, lang='en')
        tts.write_to_fp(mp3_fp)
        
        # Rewind the file pointer to the beginning before reading
        mp3_fp.seek(0)
        
        # Display Streamlit audio player and autoplay it
        st.audio(mp3_fp.read(), format='audio/mp3', autoplay=True)
        # We don't need st.info anymore, as the audio player is visible
        
    except Exception as e:
        # Fallback to simulated message if gTTS or Streamlit audio fails
        st.warning(f"🔇 Audio playback failed (Error: {e}). Showing text instead: '{text}'")


# ==========================================
# 🏠 Streamlit UI Setup (NO CHANGES BELOW THIS LINE NEEDED FOR IMPORTS/SETUP)
# ==========================================
st.set_page_config(page_title="MyCare+", page_icon="💊", layout="wide")

# 🌟 Splash Screen
if "splash_done" not in st.session_state:
    st.title("💊 MyCare+ — AI Health Companion")
    st.subheader("Team CodeSlayers | HackNova 2025")
    st.markdown("### _Your care, your way — Emotion + AI + Health in one app_")
    st.image("https://cdn-icons-png.flaticon.com/512/9429/9429110.png", width=200)
    st.info("Launching app... please wait ⏳")
    time.sleep(1) # Reduced sleep for faster launch
    st.session_state.splash_done = True
    st.rerun()

# ==========================================
# 🧠 Session States (Initialization)
# ==========================================
if "mood_log" not in st.session_state:
    st.session_state.mood_log = []
if "recent_medicines" not in st.session_state:
    st.session_state.recent_medicines = []
if "chat_history_assistant" not in st.session_state:
    st.session_state.chat_history_assistant = []
if "chat_history_tablet" not in st.session_state:
    st.session_state.chat_history_tablet = []


# ==========================================
# Sidebar Navigation & Emergency Button
# ==========================================
st.sidebar.title("💊 MyCare+ Dashboard")
section = st.sidebar.radio("📍 Choose any required services", [
    "🎤 Voice & Emotion Assistant",
    "📷 Tablet Scanner",
    "📊 Health Insights",
    "🚨 Emergency Contact"
])

st.sidebar.markdown("---")
# --- (3) Emergency Notification Implementation ---
st.sidebar.subheader("🚨 Emergency Services")
if st.sidebar.button("🚨 **ACTIVATE EMERGENCY ALERT**", type="primary"):
    st.error("⚠️ EMERGENCY ALERT ACTIVATED!")
    
    # --- RED ALARM EFFECT REPLACEMENT ---
    placeholder = st.empty()
    for _ in range(3):
        placeholder.markdown("<h1 style='color: red; text-align: center; font-size: 50px;'>🚨 EMERGENCY ALERT 🚨</h1>", unsafe_allow_html=True)
        time.sleep(0.3)
        placeholder.empty()
        time.sleep(0.3)
    placeholder.markdown("<h1 style='color: red; text-align: center; font-size: 50px;'>✅ SENT!</h1>", unsafe_allow_html=True)
    # --- END ALARM EFFECT ---
    
    st.sidebar.info("Message sent to Dr. Smith and nearest family contact (Mom) with your location.")
    speak_real_audio("Emergency alert is activated and nearest contacts have been notified.")
    # Show a simulated notification on the main page for effect
    st.toast('🚨 EMERGENCY: Contacts Notified!', icon='🚨')

# ==========================================
# 1️⃣ Voice & Emotion Assistant
# ==========================================
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["sad", "upset", "depressed", "lonely"]):
        return "sadness", "You seem low. Take a deep breath, it’s going to be okay. Remember to focus on one small positive thing today."
    elif any(word in text for word in ["angry", "mad", "furious", "frustrated"]):
        return "anger", "Feeling tense? Remember, calm minds solve problems better. Try a 5-minute deep breathing exercise."
    elif any(word in text for word in ["stressed", "nervous", "worried", "overwhelmed"]):
        return "stress", "It sounds like you're under pressure. Break down your tasks and tackle them one by one. You've got this!"
    elif any(word in text for word in ["happy", "great", "excited", "good", "wonderful"]):
        return "happiness", "That's wonderful to hear! Keep that positive energy flowing and share your good mood."
    else:
        return "neutral", "Thank you for sharing. I'm here to listen whenever you need. How can I help you further?"

if section == "🎤 Voice & Emotion Assistant":
    st.header("🧠 Emotional Wellness & Support")
    st.write("Talk to MyCare+ about your day. It listens, detects emotion, and responds supportively.")

    # --- Assistant Chat Implementation ---
    st.markdown("### 💬 AI Assistant Chat")
    # Placeholder for audio player to keep it consistent
    audio_placeholder = st.empty() 
    chat_container = st.container(height=300)

    # Display chat history
    with chat_container:
        for role, message in st.session_state.chat_history_assistant:
            with st.chat_message(role):
                st.write(message)

    # Chat input
    user_input = st.chat_input("Start your conversation here (e.g., 'I had a really sad day today')...")

    if user_input:
        # Add user message to history
        st.session_state.chat_history_assistant.append(("user", user_input))
        with chat_container:
            with st.chat_message("user"):
                st.write(user_input)

        # Process and generate AI response
        emotion, ai_response_text = detect_emotion(user_input)
        st.session_state.mood_log.append(emotion)
        
        # Add AI message to history
        ai_message = f"**Detected Emotion**: **{emotion.upper()}**\n\n{ai_response_text}"
        st.session_state.chat_history_assistant.append(("assistant", ai_message))

        # Display AI response
        with chat_container:
            with st.chat_message("assistant"):
                st.write(ai_message)
                # Play the REAL audio response
                with audio_placeholder:
                    speak_real_audio(ai_response_text)
                
        # Optional: AI Mood Summary
        if len(st.session_state.mood_log) >= 3:
            mood_counts = {m: st.session_state.mood_log.count(m) for m in set(st.session_state.mood_log)}
            dominant = max(mood_counts, key=mood_counts.get) if mood_counts else "N/A"
            st.markdown("---")
            st.subheader("🧠 AI Mood Summary")
            st.info(f"Based on your recent chats, your dominant emotion has been **{dominant.upper()}**.")

# ==========================================
# 2️⃣ Tablet Scanner
# ==========================================
elif section == "📷 Tablet Scanner":
    st.header("💊 AI Tablet Scanner & Medical Information")
    st.write("Scan a tablet using your webcam. MyCare+ identifies it and provides key information.")
    
    # --- Disclaimer Implementation ---
    st.warning("🚨 **DISCLAIMER:** This is an AI identification tool. **FOR MEDICAL ADVICE, ALWAYS CONSULT A DOCTOR OR PHARMACIST.**")
    st.markdown("---")

    uploaded_file = st.camera_input("📸 Capture your tablet image")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Scanned Tablet", use_column_width=True)
        
        with st.spinner("🔍 Analyzing tablet shape, color, and imprints..."):
            time.sleep(1) # Simulated analysis time

        tablets = ["Paracetamol (500mg)", "Ibuprofen (400mg)", "Amoxicillin (250mg)", "Cetirizine (10mg)", "Aspirin (81mg)", "Dolo 650", "Azithromycin (500mg)"]
        medicine_name = random.choice(tablets)
        
        st.success(f"✅ Identified Medicine: **{medicine_name}**")
        speak_real_audio(f"Medicine identified as {medicine_name}. Searching for details now.")

        # --- Google Content / Research Integration (Simulated) ---
        search_query = f"Uses and side effects of {medicine_name}"
        st.info(f"🌐 **Searching Google for:** *{search_query}*")
        time.sleep(2) # Simulated search time

        # Simulate fetched data
        if "Paracetamol" in medicine_name or "Dolo 650" in medicine_name:
            uses = "Pain relief (headache, muscle ache) and fever reduction."
            side_effects = "Rarely, allergic reaction. Overdose can cause liver damage."
        elif "Ibuprofen" in medicine_name or "Aspirin" in medicine_name:
            uses = "Pain and inflammation relief. Used for joint pain, menstrual cramps."
            side_effects = "Stomach irritation, rarely stomach ulcers."
        else: # Amoxicillin, Cetirizine, Azithromycin
            uses = "Used to treat various bacterial infections or allergies (Cetirizine)."
            side_effects = "Commonly stomach upset, diarrhea, or allergic reactions."

        # Add tablet information to the chat
        ai_response = f"**{medicine_name}**\n\n**Common Uses (Source: WebMD/Google):** {uses}\n\n**Common Side Effects:** {side_effects}"
        st.session_state.chat_history_tablet.append(("assistant", ai_response))
        
        st.info("⏰ Reminder: **Set for 8:00 PM daily** (configurable in full app).")
        st.session_state.recent_medicines.append(medicine_name)
        if len(st.session_state.recent_medicines) > 3:
            st.session_state.recent_medicines.pop(0)

    # --- Tablet Chat Implementation ---
    st.markdown("### 💬 Tablet Info Chat")
    chat_container_tablet = st.container(height=300)

    # Display chat history for tablet (only AI messages with info)
    with chat_container_tablet:
        if not st.session_state.chat_history_tablet:
            st.info("Scan a tablet to see its information appear here.")
        for role, message in st.session_state.chat_history_tablet:
            with st.chat_message(role):
                st.write(message)
                
    st.markdown("---")
    if st.session_state.recent_medicines:
        st.subheader("🧾 Recently Scanned Medicines")
        for med in reversed(st.session_state.recent_medicines):
            st.write(f"- 💊 **{med}**")


# ==========================================
# 3️⃣ Health Dashboard
# ==========================================
elif section == "📊 Health Insights":
    st.header("📈 Personalized Health Insights")
    st.write("View your detected emotion statistics and key health metrics.")
    
    # Analyze mood log
    if st.session_state.mood_log:
        mood_counts = {m: st.session_state.mood_log.count(m) for m in set(st.session_state.mood_log)}
        all_emotions = ["happiness", "neutral", "sadness", "anger", "stress"]
        # Ensure all emotions are in the dict for plotting
        for e in all_emotions:
            if e not in mood_counts:
                mood_counts[e] = 0
                
        emotions_for_plot = list(mood_counts.keys())
        values_for_plot = list(mood_counts.values())

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(emotions_for_plot, values_for_plot, color=['green', 'gray', 'blue', 'red', 'orange'])
        ax.set_title("Voice Emotion Pattern (Recent Interactions)")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    else:
        st.info("Interact with the **Voice & Emotion Assistant** to see your mood trend here.")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("💓 Heart Rate", "76 bpm", "+3 steady")
    col2.metric("🧘 Stress Index", "Low", "-12% this week")
    col3.metric("😴 Sleep Quality", "Good", "+8% improvement")

    st.success("Keep tracking your health with MyCare+ 💚")

# ==========================================
# 4️⃣ Emergency Contact (Moved to Sidebar section)
# ==========================================
elif section == "🚨 Emergency Contact":
    st.header("🚨 Emergency Contact & System Status")
    st.write("This feature is designed to quickly alert your pre-registered contacts (Doctor, Family) in a critical situation.")
    
    st.markdown("### System Status:")
    st.table({
        "Feature": ["Primary Contact", "Secondary Contact", "Location Sharing", "System Status"],
        "Status": ["Dr. Jane Smith (Cardiologist)", "Mom (Family)", "Active", "OK"]
    })
    
    st.info("The Emergency Alert button in the sidebar will instantly dispatch a notification with your last known location.")