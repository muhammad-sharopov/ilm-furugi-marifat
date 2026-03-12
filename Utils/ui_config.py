import streamlit as st
import os, time
from Utils.AI_helper import reset_ai_memory

def setup_page():
    st.set_page_config(layout="wide")

def show_splash():
    if "app_loaded" not in st.session_state:
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');
            html, body {margin:0; padding:0; width:100%; height:100%; font-family:'Outfit', sans-serif; overflow:hidden;}
            .splash {position:fixed; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center;
                     background: radial-gradient(circle at center, #1e293b, #0f172a 90%); color:#f8fafc; z-index:9999;
                     transition:opacity 0.8s ease, transform 0.8s ease;}
            .splash.fade-out {opacity:0; transform:scale(1.05); pointer-events:none;}
            canvas {position:fixed; inset:0; z-index:1; opacity: 0.6;}
            .splash > * {position:relative; z-index:2;}
            
            .logo-icon {font-size:4rem; margin-bottom:10px; background: linear-gradient(135deg, #6366f1, #a855f7); 
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                        filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5));
                        animation: float 3s ease-in-out infinite;}
            
            .title {font-size:3.5rem; font-weight:800; letter-spacing:-0.03em; margin-bottom:8px; opacity:0;
                    background: linear-gradient(to right, #fff, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    animation: fadeUp 0.8s ease forwards; animation-delay:0.3s;}
            
            .subtitle {font-size:1.2rem; color:#94a3b8; font-weight:400; opacity:0; letter-spacing: 0.02em; text-align: center; max-width: 800px;
                       animation: fadeUp 0.8s ease forwards; animation-delay:0.6s;}
            
            .ministry {font-size:0.9rem; color:#64748b; margin-top: 15px; opacity:0;
                       animation: fadeUp 0.8s ease forwards; animation-delay:0.9s;}

            .loader-line {margin-top:40px; width:200px; height:4px; background:rgba(255,255,255,0.1); border-radius:4px; overflow:hidden;
                          opacity:0; animation: fadeUp 0.8s ease forwards; animation-delay:1.2s;}
            .loader-fill {height:100%; width:0%; background: #6366f1; box-shadow: 0 0 10px #6366f1; transition:width 0.2s linear;}
            
            @keyframes fadeUp {from{opacity:0; transform:translateY(20px);} to{opacity:1; transform:translateY(0);}}
            @keyframes float {0%, 100%{transform:translateY(0);} 50%{transform:translateY(-10px);}}
        </style>

        <canvas id="bits"></canvas>
        <div class="splash" id="splash">
            <div class="logo-icon">❖</div>
            <div class="title">EduStat AI</div>
            <div class="subtitle">Интеллектуальная система анализа и прогнозирования образовательных данных</div>
            <div class="ministry">Разработано для Министерства образования и науки РТ</div>
            <div class="loader-line"><div class="loader-fill" id="fill"></div></div>
        </div>

        <script>
            const canvas = document.getElementById("bits"), ctx = canvas.getContext("2d");
            let w, h, particles = [];
            
            function resize() { w = canvas.width = innerWidth; h = canvas.height = innerHeight; }
            window.addEventListener('resize', resize); resize();

            // Создаем частицы "Нейросеть"
            for(let i=0; i<60; i++) {
                particles.push({
                    x: Math.random()*w, y: Math.random()*h,
                    vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5,
                    size: Math.random()*2 + 1
                });
            }

            function animate() {
                ctx.clearRect(0,0,w,h);
                ctx.fillStyle = "#6366f1";
                ctx.strokeStyle = "rgba(99, 102, 241, 0.15)";
                
                for(let i=0; i<particles.length; i++) {
                    let p = particles[i];
                    p.x += p.vx; p.y += p.vy;
                    
                    if(p.x < 0 || p.x > w) p.vx *= -1;
                    if(p.y < 0 || p.y > h) p.vy *= -1;
                    
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
                    ctx.fill();
                    
                    // Соединяем линии
                    for(let j=i+1; j<particles.length; j++) {
                        let p2 = particles[j];
                        let dist = Math.hypot(p.x-p2.x, p.y-p2.y);
                        if(dist < 150) {
                            ctx.lineWidth = 1 - dist/150;
                            ctx.beginPath();
                            ctx.moveTo(p.x, p.y);
                            ctx.lineTo(p2.x, p2.y);
                            ctx.stroke();
                        }
                    }
                }
                requestAnimationFrame(animate);
            }
            animate();

            // Прогресс бар
            let progress = 0;
            const bar = document.getElementById("fill");
            const timer = setInterval(() => {
                progress += Math.random() * 8;
                if(progress > 100) progress = 100;
                bar.style.width = progress + "%";
                if(progress === 100) {
                    clearInterval(timer);
                    setTimeout(() => {
                        document.getElementById("splash").classList.add("fade-out");
                    }, 600);
                }
            }, 200);
        </script>
        """, unsafe_allow_html=True)

        import time
        time.sleep(4)
        st.session_state.app_loaded = True
        st.rerun()


def init_api_key():
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

def init_session():
    if "_ai_session_inited" not in st.session_state:
        reset_ai_memory()
        st.session_state["_ai_session_inited"] = True

def init_page_state():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Загрузка данных'

def setup_sidebar(set_page):
    st.sidebar.header("🔧 Навигация")
    pages = {
        "Загрузка данных": "📥",
        "Автообработка данных": "🛡️",
        "Обработка пропусков": "⚙️",
        "Обработка выбросов": "🚩",
        "Визуальный анализ": "📊",
        "Сводные таблицы": "📟",
        "Сравнение групп": "⚖️",
        "Логистическая регрессия": "📈",
        "CatBoost моделирование": "🐈‍⬛",
        "Разъяснение результатов (с ИИ)": "💬",
            }

    st.markdown("""
        <style>
            div.stButton > button {
                background-color: #f0f2f6;
                color: black;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            div.stButton > button:hover {
                background-color: #e0f0ff;
                color: #007BFF;
                border: 1px solid #007BFF;
                border-radius: 6px;
            }
        </style>
    """, unsafe_allow_html=True)

    for name, icon in pages.items():
        st.sidebar.button(f"{icon} {name}", on_click=set_page, args=(name,))

    if st.sidebar.button("🔄 Очистить всё"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ─── Floating chat button (inject once in Home.py) ───────────────────────────
def render_float_chat_btn():
    """Инжектирует фиксированную кнопку чата в правом нижнем углу без использования JS."""
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = False

    st.markdown("""
    <style>
    /* 
       БЕЗОПАСНОЕ ПОЗИЦИОНИРОВАНИЕ (Вложенный блок):
       Используем двойной stVerticalBlock, чтобы гарантированно 
       ИЗБЕЖАТЬ попадания в корневой вертикальный блок всей страницы.
    */
    [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"]:has(> div.element-container .float-chat-marker) {
        position: fixed !important;
        bottom: 28px !important;
        right: 28px !important;
        z-index: 999999 !important;
        width: auto !important;
        animation: slideUp 0.3s ease-out !important;
        background: transparent !important;
        gap: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Скрываем ТОЛЬКО контейнер с самим маркером */
    div.element-container:has(.float-chat-marker) {
        display: none !important;
    }

    /* Стилизация самой кнопки Streamlit внутри контейнера */
    [data-testid="stVerticalBlock"]:has(> div.element-container .float-chat-marker) > div[data-testid="element-container"] button {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        color: #fff !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        box-shadow: 0 6px 24px rgba(99,102,241,0.45) !important;
        border: none !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
    }

    [data-testid="stVerticalBlock"]:has(> div.element-container .float-chat-marker) > div[data-testid="element-container"] button:hover {
        transform: translateY(-3px) scale(1.04) !important;
        box-shadow: 0 10px 30px rgba(99,102,241,0.6) !important;
    }

    /* Пульсация (добавляем декоративно через псевдоэлемент или просто CSS) */
    @keyframes chatpulse {
        0%,100% { opacity:1; transform:scale(1); }
        50%      { opacity:0.5; transform:scale(1.4); }
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="float-chat-marker" style="display:none;"></div>', unsafe_allow_html=True)
        if st.button("💬 Чат с ИИ", key="global_chat_btn_toggle", help="Открыть/закрыть чат с ИИ"):
            st.session_state.show_chat = not st.session_state.show_chat
            st.rerun()


def render_ai_chat_overlay():
    """Рендерит оверлей чата, если st.session_state.show_chat == True."""
    if not st.session_state.get("show_chat"):
        return

    from Utils.chat import continue_chat, reset_chat_history

    # Колбек для отправки сообщения по Enter и очистки поля
    def _submit_overlay_chat():
        q = st.session_state.overlay_chat_input_val
        if q:
            # Сразу добавляем в историю для визуального отображения юзер-баббла
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"role": "user", "content": q})
            
            # Ставим флаг для обработки
            st.session_state.pending_ai_processing = q
            st.session_state.overlay_chat_input_val = ""

    st.markdown("""
    <style>
    /* 
       ЧИСТЫЙ CSS ПОДХОД:
       Чтобы не сломать весь сайт (не захватить root-контейнер), 
       мы используем строгий селектор, который ищет только тот stVerticalBlock,
       который НАПРЯМУЮ содержит stMarkdown с нашим маркером.
    */
    /* Стилизация блока чата. Аналогично ограничиваем вложенностью */
    [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"]:has(> div.element-container .chat-overlay-marker) {
        position: fixed !important;
        bottom: 90px !important;
        right: 28px !important;
        width: 420px !important;
        height: 580px !important;
        background: #fff !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15) !important;
        z-index: 999998 !important;
        display: flex !important;
        flex-direction: column !important;
        border: 1px solid #e5e7eb !important;
        font-family: 'Outfit', sans-serif !important;
        animation: slideUp 0.3s ease-out !important;
        overflow: hidden !important;
        padding: 0 !important;
        gap: 0 !important;
        margin: 0 !important;
    }
    
    /* Скрываем технические маркеры безопасно */
    div.element-container:has(.chat-overlay-marker),
    div.element-container:has(.float-chat-marker) {
        display: none !important;
    }
    
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

    /* Стилизация контейнера заголовка (синяя полоса) */
    [data-testid="stVerticalBlock"]:has(.chat-overlay-marker) [data-testid="stHorizontalBlock"]:has(.chat-overlay-title) {
        background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
        border-radius: 16px 16px 0 0 !important;
        padding: 4px 12px !important;
        margin: 0 !important;
        min-height: 45px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    .chat-overlay-title { 
        margin: 0 !important; 
        font-size: 1rem !important; 
        font-weight: 600 !important; 
        color: #fff !important;
        border: none !important;
    }

    /* Стили для кнопок в шапке (белый X) */
    [data-testid="stVerticalBlock"]:has(.chat-overlay-marker) [data-testid="stHorizontalBlock"]:has(.chat-overlay-title) [data-testid="stButton"] button {
        background: transparent !important;
        border: none !important;
        color: rgba(255,255,255,0.8) !important;
        padding: 0 !important;
        font-size: 1.2rem !important;
    }
    [data-testid="stVerticalBlock"]:has(.chat-overlay-marker) [data-testid="stHorizontalBlock"]:has(.chat-overlay-title) [data-testid="stButton"] button:hover {
        color: #fff !important;
    }

    .chat-overlay-content { 
        height: 440px !important; 
        max-height: 440px !important;
        overflow-y: auto !important; 
        padding: 12px; 
        background: #f9fafb; 
        display: block !important;
    }
    
    /* Пузыри внутри HTML-истории */
    .overlay-row { display: flex; margin-bottom: 8px; width: 100%; }
    .overlay-row.user { justify-content: flex-end; }
    .overlay-row.ai { justify-content: flex-start; }
    .overlay-bubble {
        padding: 8px 12px; border-radius: 12px; font-size: 0.85rem; max-width: 85%;
        line-height: 1.4; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .overlay-row.user .overlay-bubble { background: #6366f1; color: #fff; border-bottom-right-radius: 2px; }
    .overlay-row.ai .overlay-bubble { background: #fff; color: #1e293b; border: 1px solid #e2e8f0; border-bottom-left-radius: 2px; }
    .overlay-bubble-thinking { color: #888; border: 1px dashed #cbd5e1; background: #fff; }

    /* Компактная нижняя панель */
    .chat-inputs-wrapper {
        padding: 8px 12px;
        background: #fff;
        border-top: 1px solid #e2e8f0;
        flex-shrink: 0;
    }
    .chat-inputs-wrapper [data-testid="stButton"] button {
        background: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        color: #6366f1 !important;
        font-size: 1.1rem !important;
        padding: 0 !important;
        width: 32px !important;
        height: 32px !important;
        min-height: 32px !important;
        max-height: 32px !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }
    .chat-inputs-wrapper [data-testid="stButton"] button:hover {
        background: #eef2ff !important;
        border-color: #6366f1 !important;
        color: #4f46e5 !important;
        transform: translateY(-1px) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container():
        # Секретный маркер для строгого CSS :has()
        st.markdown('<div class="chat-overlay-marker" style="display:none;"></div>', unsafe_allow_html=True)
        
        # Заголовок с кнопкой Х
        h_col1, h_col2 = st.columns([8, 1])
        with h_col1:
            st.markdown('<h3 class="chat-overlay-title">💬 AI Помощник</h3>', unsafe_allow_html=True)
        with h_col2:
            if st.button("✖", key="overlay_close_btn_top", help="Закрыть"):
                st.session_state.show_chat = False
                st.rerun()

        # Флаг ожидания ИИ
        pending_q = st.session_state.get("pending_ai_processing")

        # Выводим историю через HTML
        history_html = '<div class="chat-overlay-content" id="overlay-chat-history">'
        chat_history = st.session_state.get("chat_history", [])
        for msg in chat_history:
            if msg.get("role") == "system" or msg.get("hidden"):
                continue
            role_class = "user" if msg["role"] == "user" else "ai"
            content = msg.get("content") or msg.get("text", "")
            history_html += f'<div class="overlay-row {role_class}"><div class="overlay-bubble">{content}</div></div>'
        
        # Размещаем индикатор загрузки "ИИ думает...", если есть отложенный запрос
        if pending_q:
            history_html += f'<div class="overlay-row ai"><div class="overlay-bubble overlay-bubble-thinking">⏳ <i>ИИ думает...</i></div></div>'
            
        history_html += '</div>'
        
        st.markdown(history_html, unsafe_allow_html=True)

        # Streamlit инпуты
        st.markdown('<div class="chat-inputs-wrapper">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.text_input("Ваш вопрос...", key="overlay_chat_input_val", on_change=_submit_overlay_chat, label_visibility="collapsed", disabled=bool(pending_q))
        with col2:
            if st.button("➤", key="overlay_send_btn", help="Отправить", disabled=bool(pending_q)):
                _submit_overlay_chat()
        with col3:
            if st.button("🗑", key="overlay_clear_btn_compact", help="Очистить чат", disabled=bool(pending_q)):
                reset_chat_history()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Блок выполнения тяжелого LLM запроса (запускается ПОСЛЕ рендера окна с индикатором ⏳)
    if pending_q:
        # Убираем флаг, чтобы не зациклить
        st.session_state.pending_ai_processing = None
        # Убираем дубликат вопроса из истории, т.к. continue_chat вставит его сам
        if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
            st.session_state.chat_history.pop()
        
        # Делаем тяжелый запрос к ИИ
        continue_chat(pending_q)
        
        # Перерисовываем с готовым ответом
        st.rerun()



# ─── Sidebar context checklist ───────────────────────────────────────────────
def _ctx_sent_sidebar(keyword: str, hidden_only: bool = True) -> bool:
    """Проверяет был ли отправлен контекст (для сайдбара)."""
    for msg in st.session_state.get("chat_history", []):
        if msg.get("role") == "system":
            continue
        if hidden_only and not msg.get("hidden"):
            continue
        if keyword.lower() in str(msg.get("content", "")).lower():
            return True
    return False


_SIDEBAR_CONTEXTS = [
    ("📊 Данные (датасет)",             "датасет",              True),
    ("🔗 Корреляционный анализ",         "корреляционный анализ", False),
    ("📟 Сводная таблица",              "сводную таблицу",       True),
    ("🤖 Результаты модели (Logistic)", "логистическ",           True),
    ("🐈 Результаты модели (CatBoost)", "catboost",              True),
]


def render_sidebar_context():
    """Отображает чеклист контекстов в самом конце сайдбара."""
    with st.sidebar:
        sent_n = sum(1 for _, kw, ho in _SIDEBAR_CONTEXTS if _ctx_sent_sidebar(kw, ho))
        total_n = len(_SIDEBAR_CONTEXTS)
        
        with st.expander(f"📋 Контекст ИИ ({sent_n}/{total_n})", expanded=False):
            for label, kw, ho in _SIDEBAR_CONTEXTS:
                sent = _ctx_sent_sidebar(kw, ho)
                icon = "✅" if sent else "☐"
                color = "#2ecc71" if sent else "#aaa"
                st.markdown(
                    f"<div style='font-size:0.8rem;color:{color};padding:2px 0;'>{icon} {label}</div>",
                    unsafe_allow_html=True,
                )
