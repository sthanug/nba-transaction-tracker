import requests
import streamlit as st

st.set_page_config(
    page_title="NBA Transaction Tracker",
    page_icon="🏀",
    layout="wide"
)

# --- CUSTOM CSS ---
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
        .ai-box-orange {
            background-color: rgba(255, 85, 0, 0.1) !important;
            border: 1px solid #ff5500 !important;
            color: #ffffff !important;
            padding: 12px 16px;
            border-radius: 8px;
            margin-top: 8px;
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.5;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --- HELPER: EMOJI TAGGER ---
def add_transaction_emoji(text):
    text_lower = text.lower()
    if "waive" in text_lower or "cut" in text_lower or "release" in text_lower:
        return f"👋🏾 {text}"
    elif "sign" in text_lower or "contract" in text_lower:
        return f"📄 {text}"
    elif "trade" in text_lower or "acquir" in text_lower or "deal" in text_lower:
        return f"🔄 {text}"
    elif "extend" in text_lower or "extension" in text_lower:
        return f"✍️ {text}"
    elif "injur" in text_lower or "illness" in text_lower or "out" in text_lower:
        return f"🚑 {text}"
    return f"📌 {text}"


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
    token = st.secrets.get("HF_TOKEN", "")
    if not token:
        return "Missing API key in secrets."

    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        "You are an NBA analyst. Provide a brief, 2-sentence breakdown of the salary cap, "
        "roster fit, or trade mechanics for this transaction. Keep it direct and natural."
    )

    payload = {
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Analyze: {move_text}"}
        ],
        "max_tokens": 100,
        "temperature": 0.3
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error ({response.status_code}): {response.text[:100]}"
    except Exception as e:
        return f"Unable to analyze right now: {str(e)}"


# --- MAIN INTERFACE ---
st.title("🏀 NBA Transaction Tracker")

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
                st.write(add_transaction_emoji(desc))

            with col_action:
                if st.button("Analyze", key=f"btn_{i}"):
                    st.session_state[f"ai_{i}"] = analyze_move(desc)

            if f"ai_{i}" in st.session_state:
                st.markdown(
                    f'<div class="ai-box-orange"><b>AI Breakdown:</b> {st.session_state[f"ai_{i}"]}</div>',
                    unsafe_allow_html=True
                )

            st.divider()
