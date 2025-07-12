# 🛍️ Voice Shopping Assistant

An AI‑powered, voice‑enabled shopping assistant tailored for kids and parents. Users can ask natural language queries—typed or spoken—and receive personalized product recommendations (with images, descriptions, prices, and save‑for‑later functionality) powered by a local LLaMA‑2 (13B) model via Ollama, FastAPI backend, and Streamlit frontend.  


## 🔍 Problem  
Parents and children often struggle to find age‑appropriate, educational or fun products online. Traditional search boxes require precise keywords and overwhelm users with thousands of results. Our solution enables hands‑free, conversational shopping with AI‑driven recommendations.

---

## 💡 Solution  
- **Voice & Text Input:** Speak or type queries like “Suggest something space‑themed for a 10‑year‑old.”  
- **Personalized Sidebar:** Capture user name, age, and interests.  
- **LLM Recommendations:** Local LLaMA‑2 (13B) model via Ollama generates concise product suggestions.  
- **Product Cards:** Display image, description, tags, and price.  
- **Save for Later:** Users can bookmark favorites, reviewed in a “❤️ Your Saved Items” section.  

---

## 🛠️ Tech Stack  
| Layer                    | Technology                                    |
|--------------------------|-----------------------------------------------|
| **Frontend/UI**          | [Streamlit](https://streamlit.io)             |
| **Voice I/O**            | `speech_recognition` + Google Web Speech API (input), `gTTS` (output) |
| **Backend**              | [FastAPI](https://fastapi.tiangolo.com)       |
| **LLM Engine**           | [Ollama](https://ollama.ai) + LLaMA‑2 (13B)    |
| **Data Storage**         | Static JSON product catalog                   |
| **Deployment (Demo)**    | Localhost (Streamlit + Uvicorn)               |

---

## 📥 Installation

1. **Clone the repo**  

   * git clone https://github.com/YOUR_USERNAME/voice-shopping-assistant.git
   * cd voice-shopping-assistant


2. **Backend Setup**

  
   * cd server
   * python3 -m venv venv
   * source venv/bin/activate            # Windows: venv\Scripts\activate
   * pip install -r requirements.txt


3. **Frontend Setup (Streamlit)**

   * cd ../client2
   * python3 -m venv venv
   * source venv/bin/activate
   * pip install -r requirements.txt


4. **Ollama & LLaMA‑2**

   * Install Ollama: `brew install ollama` (macOS) or follow [docs](https://ollama.ai).
   * Download LLaMA‑2 13B: `ollama pull llama2`
   * Start local server:

   
     ollama run llama2
 

---

## ▶️ Running Locally

1. **Start Backend**

   cd server
   uvicorn app.main:app --reload


2. **Start Frontend**


   cd client2
   streamlit run app.py
  

3. **Open Browser**
   Visit `http://localhost:8501` to interact with your Voice Shopping Assistant.

---

## 🧑‍💻 Usage

* **Set Preferences:** Use the sidebar to enter name, age, and interests.
* **Type or Speak:** Click 🎙️ or type a query in the text box.
* **Get Recommendations:** View AI’s response, product card, and price.
* **Save Items:** Click 💾 to bookmark products in “❤️ Your Saved Items.”

---

## 🤝 Contributing

Contributions, ideas, and pull requests are welcome! Please open an issue or submit a PR.

---

## 📄 License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

```
```
