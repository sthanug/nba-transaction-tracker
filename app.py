import requests
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="NBA Transaction Tracker",
    page_icon="🏀",
    layout="wide"
)

# --- STYLING ---
st.markdown(
    """
    <style>
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
        }
        .stButton>button {
            border-radius: 6px;
            font-weight: 500;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --- DATA FETCHING ---
@st.cache_data(ttl=1800)
def fetch_transactions():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/transactions?limit=100"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
    except Exception:
        return []

    moves = []
    for item in data.get("transactions", []):
        date = item.get("date", "")[:10]
        desc = item.get("description", "No details provided.")
        team_info = item.get("team", {})

        team_name = "NBA"
        if isinstance(team_info, dict):
            team_name = team_info.get("displayName", "NBA")

        moves.append({
            "date": date,
            "team": team_name,
            "desc": desc
        })
    return moves


# --- AI ANALYSIS ---
def analyze_move(move_text):
    try:
        token = st.secrets.get("HF_TOKEN", "")
        if not token:
            return "Missing API key."

        client = InferenceClient(token=token)
        
        prompt = (
            "You are an NBA analyst. Provide a brief, 2-sentence breakdown of the salary cap, "
            "roster fit, or trade mechanics for this transaction. Keep it direct and natural."
        )

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Analyze: {move_text}"}
        ]

        res = client.chat_completion(messages=messages, max_tokens=100, temperature=0.3)
        return res.choices[0].message.content
    except Exception as e:
        return f"Unable to analyze right now: {str(e)}"


# --- APP INTERFACE ---
st.title("NBA Transaction Tracker")

query = st.text_input("Filter moves", "", placeholder="Search team or player...").strip().lower()
st.divider()

moves = fetch_transactions()

if not moves:
    st.info("No recent transactions found.")
else:
    for i, move in enumerate(moves):
        date = move["date"]
        team = move["team"]
        desc = move["desc"]

        if not query or query in team.lower() or query in desc.lower():
            col_text, col_action = st.columns([4, 1])

            with col_text:
                st.caption(f"{date} • {team}")
                st.write(desc)

            with col_action:
                if st.button("Analyze", key=f"btn_{i}"):
                    st.session_state[f"ai_{i}"] = analyze_move(desc)

            if f"ai_{i}" in st.session_state:
                st.info(st.session_state[f"ai_{i}"])

            st.divider()
