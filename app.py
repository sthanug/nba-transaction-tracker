import requests
import streamlit as st

st.set_page_config(
    page_title="NBA Transaction Tracker",
    page_icon="🏀",
    layout="wide"
)

#css
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

#emojis
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


#data fetching
@st.cache_data(ttl=1800)
def fetch_transactions():
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/transactions?limit=100"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        st.error(f"ESPN API Connection Error: {e}")
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
    
#aianalyze
def analyze_move(date, team, move_text):
    token = st.secrets.get("GROQ_API_KEY", "")
    if not token:
        return "Missing API key."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    prompt = (
        "You are a sharp NBA analyst providing a concise 2-sentence breakdown of an NBA transaction. "
        "CRITICAL RULES: "
        "1. Focus on the practical basketball and roster impact (e.g., depth management, roster flexibility, luxury tax relief, or rotation fit) based on the current point in the season. "
        "2. Do not blindly overuse buzzwords like 'training camp' or 'Exhibit 10' unless they naturally fit the transaction and date. "
        "3. DO NOT guess or fabricate specific player skillsets or veteran histories if you aren't certain. Refer to fringe players simply by position or general depth role. "
        "4. DO NOT name other players on the team's roster."
    )

    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Date: {date}\nTeam: {team}\nTransaction: {move_text}\nAnalyze the move:"}
        ],
        "max_completion_tokens": 1024,
        "temperature": 0.3,
        "reasoning_format": "hidden"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=12)
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"].get("content", "")
            return content if content else "Received empty response from model."
        else:
            return f"API Error ({response.status_code}): {response.text[:100]}"
    except Exception as e:
        return f"Unable to analyze right now: {str(e)}"
