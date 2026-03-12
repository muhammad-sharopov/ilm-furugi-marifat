import streamlit as st
from Utils.chat import continue_chat, reset_chat_history

# ─────────────────────────────────────────────
#  Popup-style chat page
# ─────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap');

/* Сужаем и центрируем страницу, имитируем popup */
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stMainBlockContainer"]       { max-width: 720px; margin: 0 auto; padding: 0 16px 120px; }

/* Заголовок окна чата */
.chat-header {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: #fff;
    border-radius: 16px 16px 0 0;
    padding: 18px 24px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35);
    font-family: 'Outfit', sans-serif;
    margin-top: 16px;
    position: relative;
    overflow: hidden;
}
.chat-header::before {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: translateX(-100%); animation: shine 3s infinite;
}
@keyframes shine { 100% { transform: translateX(100%); } }

.header-left { display: flex; align-items: center; gap: 14px; }
.chat-header h2 { margin: 0; font-size: 1.3rem; font-weight: 700; }
.chat-header p  { margin: 2px 0 0; font-size: 0.85rem; opacity: 0.85; }

/* Кнопка закрытия */
.close-btn {
    background: rgba(255, 255, 255, 0.15);
    color: white !important;
    text-decoration: none !important;
    padding: 6px 12px;
    border-radius: 10px;
    font-size: 0.8rem;
    font-weight: 600;
    transition: background 0.2s;
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255,255,255,0.2);
}
.close-btn:hover { background: rgba(255, 255, 255, 0.25); }

.chat-header .pulse {
    width: 10px; height: 10px; background: #34d399; border-radius: 50%;
    animation: pulse 1.6s infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.4; transform:scale(1.5); }
}

/* Тело чата */
.chat-body {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-top: none;
    padding: 24px;
    min-height: 400px;
    max-height: 600px;
    overflow-y: auto;
    box-shadow: 0 10px 40px rgba(0,0,0,0.05);
}

/* Пузыри */
.chat-row { display:flex; margin-bottom:14px; width:100%; }
.chat-row.user  { justify-content:flex-end; }
.chat-row.ai    { justify-content:flex-start; }
.chat-row.user .bubble {
    background: linear-gradient(135deg,#6366f1,#4f46e5);
    color:#fff; border-radius:18px 18px 4px 18px;
    padding:10px 16px; max-width:75%;
    box-shadow:0 2px 10px rgba(99,102,241,.25);
    font-size:.93rem; line-height:1.5;
}
.chat-row.ai .bubble {
    background:#fff; color:#1a1a2e;
    border-radius:18px 18px 18px 4px;
    padding:10px 16px; max-width:80%;
    border:1px solid #e5e7eb;
    font-size:.93rem; line-height:1.5;
}
.avatar { font-size:1.4rem; margin:0 6px; display:flex; align-items:flex-start; }

/* Быстрые вопросы */
.qq-header {
    font-size:0.82rem; color:#6366f1; font-weight:600;
    margin:10px 0 6px;
    font-family:'Outfit',sans-serif;
}
.stButton > button {
    font-size: 0.8rem !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    border: 1px solid #6366f1 !important;
    color: #6366f1 !important;
    background: #fff !important;
    transition: all .15s !important;
}
.stButton > button:hover {
    background: #6366f1 !important;
    color: #fff !important;
}

/* Футер */
.chat-footer {
    background:#fff;
    border: 1px solid #e5e7eb;
    border-top: none;
    border-radius: 0 0 16px 16px;
    padding: 6px 12px 14px;
}
</style>
""", unsafe_allow_html=True)


# ─── Вспомогательная функция ───────────────────────────────────────────────
def _ctx_sent(keyword: str, hidden_only: bool = True) -> bool:
    for msg in st.session_state.get("chat_history", []):
        if msg.get("role") == "system":
            continue
        if hidden_only and not msg.get("hidden"):
            continue
        if keyword.lower() in str(msg.get("content", "")).lower():
            return True
    return False


_CONTEXTS = [
    ("датасет",              True),
    ("корреляционный анализ", False),
    ("сводную таблицу",       True),
    ("логистическ",           True),
    ("catboost",              True),
]

_QUICK_QUESTIONS = {
    "датасет": [
        "Какие колонки в моих данных?",
        "Есть ли пропуски в данных?",
        "Какой тип данных у каждого столбца?",
    ],
    "корреляционный анализ": [
        "Объясни найденные корреляции простым языком",
        "Какие связи самые сильные?",
        "На что обратить внимание в результатах корреляции?",
    ],
    "сводную таблицу": [
        "Прокомментируй результаты сводной таблицы",
        "Какие выводы можно сделать из сводной таблицы?",
        "Какие группы показывают лучшие результаты?",
    ],
    "логистическ": [
        "Объясни метрики логистической регрессии",
        "Насколько хороша модель?",
        "Какие признаки наиболее важны?",
    ],
    "catboost": [
        "Объясни метрики модели CatBoost",
        "Как улучшить результаты CatBoost?",
        "Какие признаки наиболее важны по CatBoost?",
    ],
}


# ─── Заголовок окна ────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <div class="header-left">
        <div class="pulse"></div>
        <div>
            <h2>💬 EduStat AI — Ассистент</h2>
            <p>Интеллектуальный помощник всегда на связи</p>
        </div>
    </div>
    <a href="/" target="_self" class="close-btn">Закрыть ×</a>
</div>
""", unsafe_allow_html=True)

# ─── Тело чата ─────────────────────────────────────────────────────────────
st.markdown('<div class="chat-body">', unsafe_allow_html=True)


def _render_msg(content, role):
    if role == "user":
        st.markdown(f'''
        <div class="chat-row user">
            <div class="bubble">{content}</div>
            <div class="avatar">👤</div>
        </div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-row ai">
            <div class="avatar">🤖</div>
            <div class="bubble">{content}</div>
        </div>''', unsafe_allow_html=True)


# Обработка быстрого вопроса (нажатие кнопки)
if "_quick_question" in st.session_state and st.session_state["_quick_question"]:
    _qq = st.session_state.pop("_quick_question")
    with st.spinner("⏳ ИИ думает..."):
        continue_chat(_qq)
    st.rerun()

# Рендерим историю
st.session_state.setdefault("chat_history", [])
for msg in st.session_state.chat_history:
    if msg.get("role") == "system" or msg.get("hidden"):
        continue
    _render_msg(msg.get("content") or msg.get("text", ""), msg.get("role"))

st.markdown('</div>', unsafe_allow_html=True)

# ─── Быстрые вопросы ───────────────────────────────────────────────────────
sent_keys = [kw for kw, ho in _CONTEXTS if _ctx_sent(kw, ho)]

if sent_keys:
    st.markdown('<div class="chat-footer">', unsafe_allow_html=True)
    st.markdown('<div class="qq-header">💡 Быстрые вопросы</div>', unsafe_allow_html=True)

    for kw in sent_keys:
        questions = _QUICK_QUESTIONS.get(kw, [])
        cols = st.columns(len(questions)) if questions else []
        for i, q in enumerate(questions):
            with cols[i]:
                if st.button(q, key=f"qq_{kw}_{i}"):
                    st.session_state["_quick_question"] = q
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Кнопка очистки + ввод ────────────────────────────────────────────────
col_clear, _ = st.columns([1, 5])
with col_clear:
    if st.button("🗑 Очистить", use_container_width=True):
        reset_chat_history()
        st.rerun()

if question := st.chat_input("Напишите свой вопрос…"):
    _render_msg(question, "user")
    with st.spinner("⏳ ИИ думает..."):
        answer = continue_chat(question)
    _render_msg(answer, "assistant")
