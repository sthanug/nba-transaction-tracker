import requests
import streamlit as st
from datetime import datetime
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
            border-radius: 8px;
            font-weight: 500;
            border: 1px solid rgba(49, 51, 63, 0.2);
        }
        .move-card {
            padding: 0.9rem 1.1rem;
            border-radius: 10px;
            border: 1px solid rgba(49, 51, 63, 0.12);
            background-color: rgba(240, 242, 246, 0.4);
            margin-bottom: 0.6rem;
        }
        .move-meta {
            color: #6b7280;
            font-size: 0.85rem;
            margin-bottom: 0.15rem;
        }
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #6b7280;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HELPERS ---
def format_date(raw_date):
    """Turn '2026-08-03' into something a person would actually say."""
    try:
        return datetime.strptime(raw_date, "%Y-%m-%d").strftime("%b %-d, %Y")
    except Exception:
        return raw_date or "Date unknown"


def move_emoji(desc):
    """Pick a small icon based on what kind of move this is."""
    text = desc.lower()
    if "trade" in text:
        return "🔄"
    if "sign" in text:
        return "✍️"
    if "waive" in text or "release" in text:
        return "👋"
    if "injur" in text or "il" in text.split():
        return "🩹"
    if "draft" in text:
        return "🎓"
    return "🏀"


# --- DATA ---
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
        moves.append({"date": date, "team": team_name, "desc": desc})
    return moves


# --- AI ---
def analyze_move(move_text):
    try:
        token = st.secrets.get("HF_TOKEN", "")
        if not token:
            return "I can't reach the analysis model right now — looks like the API key isn't set up."

        client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=token)

        system_prompt = (
            "You're a sharp, personable NBA analyst chatting with a fan. In 2 natural sentences, "
            "break down what this move means — think salary cap impact, roster fit, or trade "
            "mechanics, whichever is most relevant. Keep it conversational, not robotic."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"What's the story here? {move_text}"}
        ]
        res = client.chat_completion(messages=messages, max_tokens=100, temperature=0.3)
        return res.choices[0].message.content
    except Exception as e:
        return f"Couldn't pull up an analysis just now ({str(e)}). Try again in a bit."


# --- HEADER ---
st.title("🏀 NBA Transaction Tracker")
st.caption("A running feed of trades, signings, and roster moves around the league — with AI breakdowns on demand.")

col_search, col_refresh = st.columns([5, 1])
with col_search:
    query = st.text_input(
        "Filter moves",
        "",
        placeholder="Search by team or player, e.g. 'Lakers' or 'James'...",
        label_visibility="collapsed"
    ).strip().lower()
with col_refresh:
    if st.button("🔄 Refresh", use_container_width=True):
        fetch_transactions.clear()
        st.rerun()

st.divider()

# --- MAIN ---
with st.spinner("Pulling the latest moves..."):
    moves = fetch_transactions()

if not moves:
    st.markdown(
        """
        <div class="empty-state">
            <h3>🤷 Nothing to show right now</h3>
            <p>Either it's a quiet day around the league, or the feed hiccuped. Try refreshing in a bit.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    filtered = [
        (i, m) for i, m in enumerate(moves)
        if not query or query in m["team"].lower() or query in m["desc"].lower()
    ]

    if not filtered:
        st.markdown(
            f"""
            <div class="empty-state">
                <h3>🔍 No matches for "{query}"</h3>
                <p>Try a different team name or player, or clear the search to see everything.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if query:
            st.caption(f"Showing {len(filtered)} of {len(moves)} moves")

        for i, move in filtered:
            date = format_date(move["date"])
            team = move["team"]
            desc = move["desc"]
            icon = move_emoji(desc)

            col_text, col_action = st.columns([4, 1])
            with col_text:
                st.markdown(f'<div class="move-meta">{icon} {date} • {team}</div>', unsafe_allow_html=True)
                st.write(desc)
            with col_action:
                if st.button("Break it down", key=f"btn_{i}", use_container_width=True):
                    with st.spinner("Thinking it through..."):
                        st.session_state[f"ai_{i}"] = analyze_move(desc)

            if f"ai_{i}" in st.session_state:
                st.info(f"🧠 {st.session_state[f'ai_{i}']}")
