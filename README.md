# 🏀 NBA Transaction Tracker

A web app I built for the Congressional App Challenge that pulls live NBA transactions and uses AI to explain them in plain English for casual fans.

## What It Does
* **Live ESPN Feed:** Fetches the 100 most recent league transactions and adds emoji tags (like signings, waivers, and trades) so it's easy to scan.
* **AI Breakdowns:** Clicking **Analyze** on any move uses the Groq API (`gpt-oss-20b`) to explain what the move actually means for the team's roster—with strict prompt rules so the AI doesn't make up fake stats or cap numbers.
* **Search & Filter:** Type in any team or player name to filter the feed instantly.
* **Mobile Friendly:** Built with a dark-mode layout that works on both desktop and phones.

## Built With
* **Python** & **Streamlit** (Frontend & Backend)
* **Groq API** (`gpt-oss-20b` for transaction breakdowns)
* **ESPN API** (Live NBA transaction data)
* **Streamlit Community Cloud** (Hosting)

## Privacy
This app doesn't use accounts, passwords, or tracking. It only reads public NBA data and runs quick AI summaries without saving any user info.
