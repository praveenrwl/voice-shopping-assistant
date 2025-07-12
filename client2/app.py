
import streamlit as st
import requests
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

# ————————————————————————————————
# Page Setup & Session State Initialization
# ————————————————————————————————
st.set_page_config(page_title="🛍️ AI Shopping Assistant", layout="centered")
# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = {}

# ————————————————————————————————
# Title & Reset Chat
# ————————————————————————————————
st.title("🛍️ Voice Shopping Assistant")
st.markdown("Ask me about products, deals, or get smart recommendations!")
if st.button("🔄 Reset Chat"):
    st.session_state["chat_history"].clear()
    st.session_state["favorites"].clear()
    st.experimental_rerun()

# ————————————————————————————————
# Product Catalog
# ————————————————————————————————
product_catalog = [
    {"name": "Astronaut Puzzle", "description": "A fun 100-piece jigsaw puzzle featuring an astronaut in space.", "price": 499, "tags": ["space", "puzzle", "fun"], "age_range": [6,12], "image": "https://cdn.pixabay.com/photo/2016/11/29/10/07/jigsaw-puzzle-1861710_1280.jpg"},
    {"name": "Glow-in-the-Dark Solar System Kit", "description": "Craft your own glowing planets and learn about the solar system.", "price": 799, "tags": ["space", "science", "DIY"], "age_range": [7,12], "image": "https://cdn.pixabay.com/photo/2022/01/19/22/25/solar-system-6949917_1280.jpg"},
    {"name": "Beginner Telescope", "description": "Explore the night sky with this compact telescope.", "price": 1999, "tags": ["space", "exploration", "science"], "age_range": [8,14], "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Telescope_01.jpg/320px-Telescope_01.jpg"},
    {"name": "Creative Art Box", "description": "A collection of paints, brushes, and art sheets for young artists.", "price": 649, "tags": ["art", "creativity", "fun"], "age_range": [5,12], "image": "https://cdn.pixabay.com/photo/2015/10/30/20/13/watercolor-1016951_1280.jpg"},
    {"name": "Magnet Science Kit", "description": "Learn physics with 10 magnetic experiments and activities.", "price": 899, "tags": ["science", "physics", "DIY"], "age_range": [8,14], "image": "https://cdn.pixabay.com/photo/2017/02/17/09/28/magnet-2076846_1280.jpg"},
    {"name": "Dinosaur Dig Excavation Kit", "description": "Dig for fossils and assemble your own dino skeleton!", "price": 549, "tags": ["dinosaur", "science", "paleontology"], "age_range": [6,11], "image": "https://cdn.pixabay.com/photo/2015/12/01/20/28/dinosaur-1072832_1280.jpg"},
    {"name": "LEGO City Rocket Launch Center", "description": "Build your own rocket launch pad with this space-themed LEGO kit.", "price": 2999, "tags": ["lego", "space", "creativity"], "age_range": [7,13], "image": "https://cdn.pixabay.com/photo/2017/03/06/20/02/lego-2127013_1280.jpg"},
    {"name": "Periodic Table Poster", "description": "Colorful and fun poster for chemistry lovers.", "price": 299, "tags": ["science", "chemistry", "learning"], "age_range": [10,16], "image": "https://cdn.pixabay.com/photo/2018/10/01/20/12/periodic-table-3714386_1280.jpg"},
    {"name": "Smart Robot Coding Toy", "description": "Program a robot using a simple drag-and-drop app.", "price": 2499, "tags": ["coding", "robotics", "STEM"], "age_range": [9,14], "image": "https://cdn.pixabay.com/photo/2019/03/18/19/54/robot-4062674_1280.jpg"},
    {"name": "Paint-by-Numbers Space Set", "description": "Paint a galaxy scene with this guided paint kit.", "price": 459, "tags": ["art", "space", "painting"], "age_range": [6,12], "image": "https://cdn.pixabay.com/photo/2020/05/04/00/21/galaxy-5128560_1280.jpg"}
]

# ————————————————————————————————
# Sidebar - User Preferences
# ————————————————————————————————
with st.sidebar:
    st.header("🎯 User Preferences")
    name = st.text_input("Your Name", value="Alex")
    age = st.slider("Age", 5, 18, 10)
    interests = st.multiselect("Select Interests", ["space","robots","math","puzzle","science","drawing"], default=["space","puzzle"])
    if st.button("Save Preferences"):
        st.session_state["user_profile"] = {"name": name, "age": age, "interests": interests}
        st.success("✅ Preferences saved!")

# ————————————————————————————————
# Voice Input & TTS
# ————————————————————————————————
def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=3, phrase_time_limit=5)
    try:
        return r.recognize_google(audio)
    except:
        return ""

def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts.save(fp.name)
        os.system(f"start {fp.name}" if os.name=='nt' else f"afplay {fp.name}")

# ————————————————————————————————
# Helper: Filter Products
# ————————————————————————————————
def filter_products(user):
    age = user.get('age',0)
    tags = set(user.get('interests',[]))
    return [p for p in product_catalog if age>=p['age_range'][0] and age<=p['age_range'][1] and tags.intersection(p['tags'])]

# ————————————————————————————————
# Helper: Get LLM Reply
# ————————————————————————————————
def get_reply(msg):
    user = st.session_state.user_profile
    options = filter_products(user)
    catalog = '\n'.join([f"- {o['name']}: ₹{o['price']}" for o in options])
    prompt = f"Suggest one product from the list below for '{msg}':\n{catalog}\nReply with product name, benefit, and price only."
    res = requests.post('http://localhost:8000/api/chat', json={'message':prompt})
    return res.json().get('reply','Error') if res.status_code==200 else 'Error'

# ————————————————————————————————
# Chat Input & Stream
# ————————————————————————————————
col1, col2 = st.columns([3,1])
with col1:
    text = st.text_input('Type a message:')
with col2:
    if st.button('🎙️ Voice'):
        spoken = record_voice()
        st.session_state['chat_history'].append(('user',spoken))
        reply = get_reply(spoken)
        st.session_state['chat_history'].append(('bot',reply))
        speak(reply)
if text:
    st.session_state['chat_history'].append(('user',text))
    reply = get_reply(text)
    st.session_state['chat_history'].append(('bot',reply))
    speak(reply)

# ————————————————————————————————
# Display Suggestion & Save Button
# ————————————————————————————————
if st.session_state['chat_history']:
    role,msg = st.session_state['chat_history'][-1]
    if role=='bot':
        st.markdown('### 🧩 Suggested Product')
        for p in filter_products(st.session_state['user_profile']):
            if p['name'].lower() in msg.lower():
                c1,c2 = st.columns([1,2])
                with c1:
                    st.image(p['image'],width=180)
                with c2:
                    st.markdown(f"**{p['name']}** – ₹{p['price']}")
                    st.markdown(p['description'])
                    if st.button('💾 Save',key=p['name']):
                        st.session_state['favorites'].append(p)
                        st.success(f"Saved {p['name']}")

# ————————————————————————————————
# Conversation & Favorites
# ————————————————————————————————
st.markdown('---')
st.markdown('### 💬 Conversation')
for r,m in st.session_state['chat_history']:
    emoji = '🧑‍💻' if r=='user' else '🤖'
    st.markdown(f"{emoji}: {m}")
st.markdown('### ❤️ Your Saved Items')
if st.session_state['favorites']:
    for f in st.session_state['favorites']:
        st.image(f['image'],width=120)
        st.markdown(f"**{f['name']}** – ₹{f['price']}")
        st.caption(f['description'])
else:
    st.info('No saved items yet.')
