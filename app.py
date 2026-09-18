import streamlit as st
import ollama
import base64
import ast


# ==========================================
# BACKGROUND IMAGE FUNCTION
# ==========================================

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# ==========================================
# CODE ANALYSIS FUNCTION
# ==========================================

def analyze_python_code(code):

    try:
        tree = ast.parse(code)

        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            )
        ]

        classes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

        imports = [
            node
            for node in ast.walk(tree)
            if isinstance(
                node,
                (ast.Import, ast.ImportFrom)
            )
        ]

        return {
            "functions": len(functions),
            "classes": len(classes),
            "imports": len(imports)
        }

    except SyntaxError:

        return {
            "functions": 0,
            "classes": 0,
            "imports": 0
        }


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Code Explanation Tutor",
    page_icon="💻",
    layout="wide"
)


# ==========================================
# ROBOT BACKGROUND + UI STYLING
# ==========================================

try:

    background_image = get_base64_image(
        "assets/robot-bg.png"
    )

    st.markdown(
        f"""
        <style>

        /* ==========================================
           MAIN APPLICATION
           ========================================== */

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(5, 10, 25, 0.25),
                    rgba(5, 10, 25, 0.25)
                ),
                url("data:image/png;base64,{background_image}");

            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}


        /* ==========================================
           MAIN CONTENT
           ========================================== */

        .block-container {{
            max-width: 1050px;
            margin-left: 32%;
            margin-right: 5%;

            padding-top: 3rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 3rem;
        }}


        /* ==========================================
           MAIN TEXT
           ========================================== */

        .block-container h1,
        .block-container h2,
        .block-container h3,
        .block-container h4,
        .block-container h5,
        .block-container h6,
        .block-container p,
        .block-container label,
        .block-container li,
        .block-container ol,
        .block-container ul,
        .block-container strong,
        .block-container em {{
            color: #ffffff !important;
        }}


        /* ==========================================
           HERO
           ========================================== */

        .hero-section {{
            padding: 20px 0 10px 0;
        }}

        .hero-badge {{
            display: inline-block;

            padding: 6px 14px;
            margin-bottom: 12px;

            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 20px;

            background: rgba(0, 0, 0, 0.45);

            color: #ffffff;

            font-size: 12px;
            font-weight: 700;

            letter-spacing: 1px;
        }}

        .hero-section h1 {{
            font-size: 48px !important;
            font-weight: 800 !important;

            margin: 0 !important;

            color: #ffffff !important;
        }}

        .hero-section p {{
            font-size: 18px !important;

            margin-top: 10px !important;

            color: rgba(255, 255, 255, 0.85) !important;
        }}


        /* ==========================================
           UPLOAD CARD
           ========================================== */

        .upload-card {{
            padding: 28px;

            margin-top: 10px;
            margin-bottom: 12px;

            text-align: center;

            background: rgba(0, 0, 0, 0.50);

            border: 1px solid rgba(255, 255, 255, 0.20);

            border-radius: 18px;

            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);

            transition: all 0.25s ease;
        }}

        .upload-card:hover {{
            background: rgba(0, 0, 0, 0.62);

            border-color: rgba(255, 255, 255, 0.35);

            transform: translateY(-2px);
        }}

        .upload-icon {{
            font-size: 42px;
            margin-bottom: 8px;
        }}

        .upload-title {{
            font-size: 24px;
            font-weight: 700;

            color: #ffffff;

            margin-bottom: 8px;
        }}

        .upload-description {{
            font-size: 15px;

            color: rgba(255, 255, 255, 0.82);

            margin-bottom: 8px;
        }}

        .upload-hint {{
            font-size: 12px;

            color: rgba(255, 255, 255, 0.55);
        }}


        /* ==========================================
           FILE HEADER
           ========================================== */

        .file-header {{
            display: flex;
            align-items: center;

            padding: 18px 20px;

            margin-top: 15px;
            margin-bottom: 15px;

            background: rgba(0, 0, 0, 0.52);

            border: 1px solid rgba(255, 255, 255, 0.18);

            border-radius: 15px;

            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }}

        .file-icon {{
            font-size: 34px;
            margin-right: 15px;
        }}

        .file-name {{
            font-size: 19px;
            font-weight: 700;

            color: #ffffff;

            margin-bottom: 3px;
        }}

        .file-status {{
            font-size: 12px;

            color: rgba(255, 255, 255, 0.60);
        }}


        /* ==========================================
           STATISTICS
           ========================================== */

        .stat-card {{
            padding: 18px;

            text-align: center;

            background: rgba(0, 0, 0, 0.50);

            border: 1px solid rgba(255, 255, 255, 0.15);

            border-radius: 14px;

            backdrop-filter: blur(7px);
            -webkit-backdrop-filter: blur(7px);
        }}

        .stat-icon {{
            font-size: 24px;
            margin-bottom: 5px;
        }}

        .stat-value {{
            font-size: 25px;
            font-weight: 800;

            color: #ffffff;
        }}

        .stat-label {{
            font-size: 12px;

            color: rgba(255, 255, 255, 0.60);

            margin-top: 3px;
        }}


        /* ==========================================
           TUTOR HEADER
           ========================================== */

        .tutor-header {{
            padding: 20px;

            margin-bottom: 18px;

            background: rgba(0, 0, 0, 0.52);

            border: 1px solid rgba(255, 255, 255, 0.17);

            border-radius: 16px;

            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }}

        .tutor-title {{
            font-size: 23px;
            font-weight: 750;

            color: #ffffff;

            margin-bottom: 5px;
        }}

        .tutor-description {{
            font-size: 13px;

            color: rgba(255, 255, 255, 0.65);
        }}


        /* ==========================================
           CHAT INFORMATION
           ========================================== */

        .chat-info {{
            padding: 14px 18px;

            margin-bottom: 15px;

            background: rgba(0, 0, 0, 0.42);

            border: 1px solid rgba(255, 255, 255, 0.12);

            border-radius: 12px;

            color: rgba(255, 255, 255, 0.75);

            font-size: 13px;
        }}


        /* ==========================================
           CHAT MESSAGES
           ========================================== */

        [data-testid="stChatMessage"] {{
            background: rgba(0, 0, 0, 0.45);

            border: 1px solid rgba(255, 255, 255, 0.12);

            border-radius: 14px;

            padding: 10px;
        }}

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] ol,
        [data-testid="stChatMessage"] ul,
        [data-testid="stChatMessage"] strong {{
            color: #ffffff !important;
        }}


        /* ==========================================
           DOWNLOAD BUTTON
           ========================================== */

        .stDownloadButton > button {{
            background: rgba(20, 25, 40, 0.90) !important;

            color: #ffffff !important;

            border: 1px solid rgba(255, 255, 255, 0.20) !important;

            border-radius: 10px !important;

            font-weight: 600 !important;

            min-height: 42px !important;

            transition: all 0.2s ease !important;
        }}

        .stDownloadButton > button span {{
            color: #ffffff !important;
        }}

        .stDownloadButton > button:hover {{
            background: rgba(35, 45, 65, 0.98) !important;

            color: #ffffff !important;

            border-color: rgba(255, 255, 255, 0.40) !important;
        }}

        .stDownloadButton > button:hover span {{
            color: #ffffff !important;
        }}


        /* ==========================================
           CLEAR CHAT BUTTON
           ========================================== */

        .clear-chat-button .stButton > button {{
            background: rgba(20, 25, 40, 0.90) !important;

            color: #ffffff !important;

            border: 1px solid rgba(255, 255, 255, 0.20) !important;

            border-radius: 10px !important;

            font-weight: 600 !important;

            min-height: 42px !important;

            transition: all 0.2s ease !important;
        }}

        .clear-chat-button .stButton > button span {{
            color: #ffffff !important;
        }}

        .clear-chat-button .stButton > button:hover {{
            background: rgba(35, 45, 65, 0.98) !important;

            color: #ffffff !important;

            border-color: rgba(255, 255, 255, 0.40) !important;
        }}

        .clear-chat-button .stButton > button:hover span {{
            color: #ffffff !important;
        }}


        /* ==========================================
           NORMAL BUTTONS
           ========================================== */

        .stButton > button {{
            border-radius: 10px;

            font-weight: 600;
        }}


        /* ==========================================
           EMPTY STATE
           ========================================== */

        .empty-state {{
            padding: 20px;

            background: rgba(0, 0, 0, 0.45);

            border: 1px solid rgba(255, 255, 255, 0.15);

            border-radius: 15px;

            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);

            margin-top: 15px;
        }}

        .empty-state-title {{
            font-size: 18px;
            font-weight: 700;

            color: #ffffff;

            margin-bottom: 6px;
        }}

        .empty-state-text {{
            font-size: 14px;

            color: rgba(255, 255, 255, 0.72);
        }}


        /* ==========================================
           QUESTION SECTION
           ========================================== */

        .question-section {{
            margin-top: 25px;
            margin-bottom: 15px;
        }}

        .question-section-title {{
            font-size: 25px;
            font-weight: 700;

            color: #ffffff;

            margin-bottom: 5px;
        }}

        .question-section-subtitle {{
            font-size: 14px;

            color: rgba(255, 255, 255, 0.70);
        }}


        /* ==========================================
           QUESTION CARDS
           ========================================== */

        .question-card {{
            min-height: 115px;

            padding: 18px;

            background: rgba(0, 0, 0, 0.48);

            border: 1px solid rgba(255, 255, 255, 0.16);

            border-radius: 14px;

            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);

            margin-bottom: 12px;

            transition: all 0.2s ease;
        }}

        .question-card:hover {{
            background: rgba(0, 0, 0, 0.65);

            border-color: rgba(255, 255, 255, 0.30);

            transform: translateY(-2px);
        }}

        .question-card-icon {{
            font-size: 25px;
            margin-bottom: 8px;
        }}

        .question-card-title {{
            font-size: 15px;
            font-weight: 700;

            color: #ffffff;

            margin-bottom: 5px;
        }}

        .question-card-description {{
            font-size: 12px;

            color: rgba(255, 255, 255, 0.65);

            line-height: 1.5;
        }}


        /* ==========================================
           SIDEBAR
           ========================================== */

        section[data-testid="stSidebar"] {{
            background: rgba(245, 247, 250, 0.96);

            border-right: 1px solid rgba(0, 0, 0, 0.12);
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stText,
        section[data-testid="stSidebar"] .stCaption {{
            color: #111827 !important;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color: rgba(0, 0, 0, 0.15);
        }}


        /* ==========================================
           FILE UPLOADER
           ========================================== */

        div[data-testid="stFileUploaderDropzone"] {{
            background: rgba(0, 0, 0, 0.70) !important;

            border: 1px solid rgba(255, 255, 255, 0.25) !important;

            border-radius: 14px !important;
        }}

        div[data-testid="stFileUploaderDropzone"] span,
        div[data-testid="stFileUploaderDropzone"] small,
        div[data-testid="stFileUploaderDropzone"] p {{
            color: #ffffff !important;
        }}

        div[data-testid="stFileUploaderDropzone"] button {{
            background-color: #111827 !important;

            color: #ffffff !important;

            border: 1px solid rgba(255, 255, 255, 0.35) !important;

            border-radius: 8px !important;
        }}

        div[data-testid="stFileUploaderDropzone"] button span {{
            color: #ffffff !important;
        }}

        div[data-testid="stFileUploaderDropzone"] button:hover {{
            background-color: #000000 !important;

            border-color: #ffffff !important;
        }}


        /* ==========================================
           SELECT BOX
           ========================================== */

        div[data-baseweb="select"] {{
            background-color: rgba(255, 255, 255, 0.95);

            border-radius: 8px;
        }}

        div[data-baseweb="select"] * {{
            color: #111827 !important;
        }}


        /* ==========================================
           TEXT INPUT
           ========================================== */

        div[data-baseweb="input"] {{
            background-color: rgba(255, 255, 255, 0.95);

            border-radius: 8px;
        }}

        div[data-baseweb="input"] input {{
            color: #111827 !important;
        }}


        /* ==========================================
           CODE BLOCK
           ========================================== */

        pre {{
            border-radius: 12px;
        }}


        /* ==========================================
           ALERTS
           ========================================== */

        div[data-testid="stAlert"] {{
            border-radius: 10px;
        }}


        /* ==========================================
           DIVIDERS
           ========================================== */

        hr {{
            border-color: rgba(255, 255, 255, 0.25);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


except FileNotFoundError:

    st.warning(
        "Robot background image not found. "
        "Make sure assets/robot-bg.png exists."
    )


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("💻 Code Tutor")

    st.write(
        "An AI-powered tutor that helps beginners "
        "understand Python programs."
    )

    st.divider()

    st.subheader("How it works")

    st.write("1. Upload a Python file")
    st.write("2. Review your code")
    st.write("3. Choose or type a question")
    st.write("4. Ask the AI")
    st.write("5. Continue the conversation")
    st.write("6. Download explanations")

    st.divider()

    st.caption(
        "Powered by Streamlit + Ollama + Llama 3.2"
    )


# ==========================================
# HERO SECTION
# ==========================================

st.markdown(
    """
<div class="hero-section">
<div class="hero-badge">🤖 AI-POWERED PYTHON TUTOR</div>
<h1>Code Explanation Tutor</h1>
<p>
Understand your Python code with clear,
beginner-friendly AI explanations.
</p>
</div>
""",
    unsafe_allow_html=True
)

st.divider()


# ==========================================
# UPLOAD SECTION
# ==========================================

st.markdown(
    """
<div class="upload-card">
<div class="upload-icon">📂</div>
<div class="upload-title">Upload your Python code</div>
<div class="upload-description">
Upload a <b>.py</b> file and let your AI tutor
analyze and explain it.
</div>
<div class="upload-hint">
Supported format: Python (.py)
</div>
</div>
""",
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Choose a Python (.py) file",
    type=["py"],
    label_visibility="collapsed"
)


# ==========================================
# PROCESS UPLOADED FILE
# ==========================================

if uploaded_file is not None:

    # ==========================================
    # READ FILE
    # ==========================================

    try:

        code = uploaded_file.read().decode("utf-8")

    except UnicodeDecodeError:

        st.error(
            "❌ Unable to read this file. "
            "Please upload a valid UTF-8 Python file."
        )

        st.stop()


    # ==========================================
    # EMPTY FILE CHECK
    # ==========================================

    if not code.strip():

        st.warning(
            "⚠️ The uploaded Python file is empty."
        )

        st.stop()


    # ==========================================
    # SESSION STATE
    # ==========================================

    current_file = uploaded_file.name

    if (
        "current_file" not in st.session_state
        or st.session_state.current_file != current_file
    ):

        st.session_state.current_file = current_file

        st.session_state.messages = []

        st.session_state.last_explanation = ""

        st.session_state.last_question = ""


    if "messages" not in st.session_state:

        st.session_state.messages = []


    if "last_explanation" not in st.session_state:

        st.session_state.last_explanation = ""


    if "last_question" not in st.session_state:

        st.session_state.last_question = ""


    # ==========================================
    # ANALYZE CODE
    # ==========================================

    analysis = analyze_python_code(code)

    function_count = analysis["functions"]

    class_count = analysis["classes"]

    import_count = analysis["imports"]


    # ==========================================
    # FILE HEADER
    # ==========================================

    st.markdown(
        f"""
<div class="file-header">
<div class="file-icon">🐍</div>
<div>
<div class="file-name">{uploaded_file.name}</div>
<div class="file-status">
Python source file • Ready for analysis
</div>
</div>
</div>
""",
        unsafe_allow_html=True
    )


    # ==========================================
    # SUCCESS MESSAGE
    # ==========================================

    st.success(
        f"Successfully uploaded: {uploaded_file.name}"
    )


    # ==========================================
    # CODE STATISTICS
    # ==========================================

    lines = code.splitlines()

    total_lines = len(lines)

    code_lines = len(
        [
            line
            for line in lines
            if line.strip()
        ]
    )

    character_count = len(code)


    # ==========================================
    # STATISTICS ROW 1
    # ==========================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
<div class="stat-card">
<div class="stat-icon">📄</div>
<div class="stat-value">{total_lines}</div>
<div class="stat-label">Total Lines</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
<div class="stat-card">
<div class="stat-icon">💻</div>
<div class="stat-value">{code_lines}</div>
<div class="stat-label">Code Lines</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
<div class="stat-card">
<div class="stat-icon">🔤</div>
<div class="stat-value">{character_count}</div>
<div class="stat-label">Characters</div>
</div>
""",
            unsafe_allow_html=True
        )


    st.write("")


    # ==========================================
    # STATISTICS ROW 2
    # ==========================================

    col4, col5, col6 = st.columns(3)


    with col4:

        st.markdown(
            f"""
<div class="stat-card">
<div class="stat-icon">⚙️</div>
<div class="stat-value">{function_count}</div>
<div class="stat-label">Functions</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col5:

        st.markdown(
            f"""
<div class="stat-card">
<div class="stat-icon">🧩</div>
<div class="stat-value">{class_count}</div>
<div class="stat-label">Classes</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col6:

        st.markdown(
            f"""
<div class="stat-card">
<div class="stat-icon">📦</div>
<div class="stat-value">{import_count}</div>
<div class="stat-label">Imports</div>
</div>
""",
            unsafe_allow_html=True
        )


    st.divider()


    # ==========================================
    # TABS
    # ==========================================

    code_tab, tutor_tab = st.tabs(
        [
            "📝 View Code",
            "🤖 AI Tutor"
        ]
    )


    # ==========================================
    # CODE TAB
    # ==========================================

    with code_tab:

        st.subheader(
            f"📝 {uploaded_file.name}"
        )

        st.caption(
            "Review the Python source code before "
            "asking the AI tutor questions."
        )

        st.code(
            code,
            language="python"
        )


    # ==========================================
    # AI TUTOR TAB
    # ==========================================

    with tutor_tab:

        # ==========================================
        # TUTOR HEADER
        # ==========================================

        st.markdown(
            """
<div class="tutor-header">
<div class="tutor-title">
🤖 Ask your AI Tutor
</div>
<div class="tutor-description">
Ask questions about your code and continue the
conversation with follow-up questions.
</div>
</div>
""",
            unsafe_allow_html=True
        )


        # ==========================================
        # CHAT INFORMATION
        # ==========================================

        st.markdown(
            """
<div class="chat-info">
💡 The tutor remembers your questions during
this session, so you can ask follow-up questions
about the same Python program.
</div>
""",
            unsafe_allow_html=True
        )


        # ==========================================
        # CLEAR CHAT
        # ==========================================

        clear_col1, clear_col2 = st.columns(
            [4, 1]
        )


        with clear_col2:

            st.markdown(
                '<div class="clear-chat-button">',
                unsafe_allow_html=True
            )

            if st.button(
                "🗑️ Clear Chat",
                use_container_width=True
            ):

                st.session_state.messages = []

                st.session_state.last_explanation = ""

                st.session_state.last_question = ""

                st.rerun()

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ==========================================
        # DISPLAY CHAT HISTORY
        # ==========================================

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )


        # ==========================================
        # QUICK QUESTIONS
        # ==========================================

        st.subheader(
            "💡 Quick Questions"
        )

        quick_question = st.selectbox(
            "Select a question",
            [
                "Explain this code",
                "Explain the functions",
                "Explain the execution flow",
                "Explain the data flow",
                "Find potential issues"
            ]
        )


        # ==========================================
        # CUSTOM QUESTION
        # ==========================================

        st.subheader(
            "💬 Ask Your Own Question"
        )

        custom_question = st.text_input(
            "What would you like to understand?",
            placeholder=(
                "Example: What does the "
                "calculate_total() function do?"
            )
        )


        # ==========================================
        # ASK AI BUTTON
        # ==========================================

        if st.button(
            "🤖 Ask AI",
            type="primary",
            use_container_width=True
        ):

            # ==========================================
            # DETERMINE QUESTION
            # ==========================================

            if custom_question.strip():

                question = custom_question.strip()

            else:

                question = quick_question


            # ==========================================
            # SAVE USER QUESTION
            # ==========================================

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            # ==========================================
            # DISPLAY USER QUESTION
            # ==========================================

            with st.chat_message("user"):

                st.markdown(
                    question
                )


            # ==========================================
            # AI RESPONSE
            # ==========================================

            with st.chat_message("assistant"):

                with st.spinner(
                    "🤖 AI is analyzing your code..."
                ):

                    try:

                        # ----------------------------------
                        # SYSTEM PROMPT
                        # ----------------------------------

                        conversation = [

                            {
                                "role": "system",

                                "content": (
                                    "You are a beginner-friendly "
                                    "Python programming tutor. "

                                    "Explain code clearly and simply. "

                                    "Break complex concepts into "
                                    "smaller parts. "

                                    "Use examples when helpful. "

                                    "When explaining execution or "
                                    "data flow, describe the steps "
                                    "in a logical order. "

                                    "Avoid unnecessary advanced "
                                    "terminology. "

                                    "Base your explanation strictly "
                                    "on the uploaded Python code."
                                )
                            }

                        ]


                        # ----------------------------------
                        # CODE CONTEXT
                        # ----------------------------------

                        conversation.append(
                            {
                                "role": "user",

                                "content": (
                                    "Here is the Python code "
                                    "we are discussing:\n\n"
                                    f"{code}"
                                )
                            }
                        )


                        # ----------------------------------
                        # PREVIOUS CONVERSATION
                        # ----------------------------------

                        for message in (
                            st.session_state.messages[:-1]
                        ):

                            conversation.append(
                                {
                                    "role": message["role"],
                                    "content": message["content"]
                                }
                            )


                        # ----------------------------------
                        # CURRENT QUESTION
                        # ----------------------------------

                        conversation.append(
                            {
                                "role": "user",
                                "content": question
                            }
                        )


                        # ----------------------------------
                        # OLLAMA REQUEST
                        # ----------------------------------

                        response = ollama.chat(
                            model="llama3.2",
                            messages=conversation
                        )


                        # ----------------------------------
                        # GET ANSWER
                        # ----------------------------------

                        answer = response[
                            "message"
                        ][
                            "content"
                        ]


                        # ----------------------------------
                        # DISPLAY ANSWER
                        # ----------------------------------

                        st.markdown(
                            answer
                        )


                        # ----------------------------------
                        # SAVE ANSWER
                        # ----------------------------------

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )


                        # ----------------------------------
                        # SAVE LAST EXPLANATION
                        # ----------------------------------

                        st.session_state.last_explanation = answer

                        st.session_state.last_question = question


                        # ----------------------------------
                        # DOWNLOAD EXPLANATION
                        # ----------------------------------

                        download_text = (
                            "CODE EXPLANATION TUTOR\n"
                            "======================\n\n"
                            f"Python File: "
                            f"{uploaded_file.name}\n\n"
                            "Question:\n"
                            f"{question}\n\n"
                            "AI Explanation:\n"
                            "---------------\n\n"
                            f"{answer}\n"
                        )


                        st.download_button(
                            label="📥 Download Latest Explanation",
                            data=download_text,
                            file_name="code_explanation.txt",
                            mime="text/plain",
                            use_container_width=True
                        )


                    except Exception as e:

                        st.error(
                            "❌ Unable to connect to the AI model."
                        )

                        st.info(
                            "Please make sure Ollama is running "
                            "and the llama3.2 model is installed."
                        )

                        with st.expander(
                            "Technical details"
                        ):

                            st.code(
                                str(e)
                            )


# ==========================================
# INITIAL STATE
# ==========================================

else:

    # ==========================================
    # EMPTY STATE
    # ==========================================

    st.markdown(
        """
<div class="empty-state">
<div class="empty-state-title">
🚀 Ready to understand your code?
</div>
<div class="empty-state-text">
Upload a Python file above and ask the AI tutor
anything about your program.
</div>
</div>
""",
        unsafe_allow_html=True
    )


    # ==========================================
    # QUESTION SECTION
    # ==========================================

    st.markdown(
        """
<div class="question-section">
<div class="question-section-title">
💡 What can you ask?
</div>
<div class="question-section-subtitle">
Explore your Python program from different perspectives.
</div>
</div>
""",
        unsafe_allow_html=True
    )


    # ==========================================
    # QUESTION CARDS
    # ==========================================

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            """
<div class="question-card">
<div class="question-card-icon">🔍</div>
<div class="question-card-title">
Explain the Code
</div>
<div class="question-card-description">
Get a simple overview of what the entire Python
program does.
</div>
</div>
""",
            unsafe_allow_html=True
        )


        st.markdown(
            """
<div class="question-card">
<div class="question-card-icon">🔄</div>
<div class="question-card-title">
Execution Flow
</div>
<div class="question-card-description">
Understand what happens first, next, and how the
program executes.
</div>
</div>
""",
            unsafe_allow_html=True
        )


        st.markdown(
            """
<div class="question-card">
<div class="question-card-icon">🐛</div>
<div class="question-card-title">
Find Potential Issues
</div>
<div class="question-card-description">
Ask the AI to identify possible problems or
suspicious parts of the code.
</div>
</div>
""",
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
<div class="question-card">
<div class="question-card-icon">⚙️</div>
<div class="question-card-title">
Explain Functions
</div>
<div class="question-card-description">
Understand what each function does and how it
contributes to the program.
</div>
</div>
""",
            unsafe_allow_html=True
        )


        st.markdown(
            """
<div class="question-card">
<div class="question-card-icon">🔗</div>
<div class="question-card-title">
Data Flow
</div>
<div class="question-card-description">
See how information moves through variables,
functions, and different parts of the program.
</div>
</div>
""",
            unsafe_allow_html=True
        )


        st.markdown(
            """
<div class="question-card">
<div class="question-card-icon">💬</div>
<div class="question-card-title">
Ask Your Own Question
</div>
<div class="question-card-description">
Ask anything about your Python code using
natural language.
</div>
</div>
""",
            unsafe_allow_html=True
        )