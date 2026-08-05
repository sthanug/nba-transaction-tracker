# 🏀 NBA Transaction Tracker

A live site tracking NBA trades, signings, waivers, and roster moves — with on-demand AI breakdowns explaining what each move actually means for cap space, roster fit, or trade mechanics.

🔗 **Live site:** https://nba-transaction-tracker.streamlit.app/

---

## 💡 Why I Built This

As a Knicks (🧡) fan, trade season gave me genuine anxiety. I was tired of frantically refreshing social media and scouring five different news sites just to make sure we hadn't secretly shipped off our best players or made a head-scratching move. 

I wanted one clean, simple place to see every transaction as it happens, plus an easy way to understand the cap math and roster implications behind each move. So, I decided to build it myself. 

I built this project by "vibe-coding" parts of it using free AI tools alongside a Human-in-the-Loop (HITL) workflow—guiding the prompt directions, debugging the edge cases, refining the UI, and making sure the underlying logic stayed tight.

---

## ✨ Features

* **Live transaction feed:** Pulls the latest 100 NBA moves directly from ESPN's public API.
* **Search & filter:** Instantly filter by team or player name.
* **AI breakdowns:** Click **"Break it down"** on any move to get a short, conversational analysis powered by an LLM.
* **Auto-refreshing data:** The feed updates every 30 minutes automatically, or on demand via the Refresh button.

---

## 🛠️ How to Use

1. **Browse the feed:** Scroll through the latest NBA transactions. Each move is tagged with a date, team, and an icon indicating the move type:
    * Trade 🔄
    * Signing ✍️
    * Waiver 👋
    * Injury 🩹
    * Draft 🎓
2. **Search:** Type a team or player name into the search bar to filter the list in real time.
3. **Refresh:** Click the **🔄 Refresh** button to pull the newest data from ESPN.
4. **Get an AI take:** Click **"Break it down"** next to any move to generate a quick explanation of its significance. It stays visible until you refresh the page.


---

## 🤖 About the AI Breakdowns

AI analysis is powered by **Qwen2.5-7B-Instruct**, accessed via the Hugging Face Inference API.

---

## 📊 Data Source & Framework

* **Data Source:** Transaction data comes from ESPN's public NBA transactions feed and is refreshed roughly every 30 minutes.
* **Framework:** Built with [Streamlit](https://streamlit.io/).

---

## 📄 License

This project is licensed under the MIT License.
