import streamlit as st
import ollama
import base64


# ==========================================
# BACKGROUND IMAGE FUNCTION
# ==========================================

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


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
           CENTER MAIN CONTENT
           ========================================== */

        .block-container {{
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
            padding-top: 3rem;
            padding-left: 3rem;
            padding-right: 3rem;
            padding-bottom: 3rem;
        }}


        /* ==========================================
           MAIN TEXT - WHITE
           ========================================== */

        .block-container h1,
        .block-container h2,
        .block-container h3,
        .block-container h4,
        .block-container h5,
        .block-container h6,
        .block-container p,
        .block-container label,
        .block-container .stMarkdown,
        .block-container .stText,
        .block-container .stCaption {{
            color: #ffffff !important;
        }}


        /* ==========================================
           SIDEBAR
           ========================================== */

        section[data-testid="stSidebar"] {{
            background: rgba(245, 247, 250, 0.96);
            border-right: 1px solid rgba(0, 0, 0, 0.12);
        }}


        /* Sidebar text - BLACK */

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


        /* Sidebar divider */

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


        /* Upload area text */

        div[data-testid="stFileUploaderDropzone"] span,
        div[data-testid="stFileUploaderDropzone"] small,
        div[data-testid="stFileUploaderDropzone"] p {{
            color: #ffffff !important;
        }}


        /* Upload button */

        div[data-testid="stFileUploaderDropzone"] button {{
            background-color: #111827 !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.35) !important;
            border-radius: 8px !important;
        }}


        /* Upload button text */

        div[data-testid="stFileUploaderDropzone"] button span {{
            color: #ffffff !important;
        }}


        /* Upload button hover */

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
           METRICS
           ========================================== */

        div[data-testid="stMetric"] {{
            background: rgba(0, 0, 0, 0.55);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }}


        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] div {{
            color: #ffffff !important;
        }}


        /* ==========================================
           TABS
           ========================================== */

        button[data-baseweb="tab"] {{
            color: #ffffff !important;
        }}


        /* ==========================================
           BUTTONS
           ========================================== */

        .stButton > button {{
            border-radius: 10px;
            font-weight: 600;
        }}


        /* ==========================================
           CODE BLOCK
           ========================================== */

        pre {{
            border-radius: 12px;
        }}


        /* ==========================================
           INFO / SUCCESS / WARNING BOXES
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
    st.write("5. Understand the explanation")

    st.divider()

    st.caption(
        "Powered by Streamlit + Ollama + Llama 3.2"
    )


# ==========================================
# MAIN HEADER
# ==========================================

st.title("💻 Code Explanation Tutor")

st.write(
    "Learn how your Python code works with "
    "beginner-friendly AI explanations."
)

st.divider()


# ==========================================
# FILE UPLOAD
# ==========================================

st.subheader("📁 Upload Python Code")

uploaded_file = st.file_uploader(
    "Choose a Python (.py) file",
    type=["py"]
)


# ==========================================
# PROCESS FILE
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


    st.success(
        f"✅ Successfully uploaded: {uploaded_file.name}"
    )


    # ==========================================
    # CODE STATISTICS
    # ==========================================

    lines = code.splitlines()

    total_lines = len(lines)

    code_lines = len(
        [
            line for line in lines
            if line.strip()
        ]
    )

    character_count = len(code)


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Total Lines",
            total_lines
        )


    with col2:

        st.metric(
            "Code Lines",
            code_lines
        )


    with col3:

        st.metric(
            "Characters",
            character_count
        )


    st.divider()


    # ==========================================
    # TABS
    # ==========================================

    code_tab, tutor_tab = st.tabs(
        ["📝 View Code", "🤖 AI Tutor"]
    )


    # ==========================================
    # CODE TAB
    # ==========================================

    with code_tab:

        st.subheader(
            f"📝 {uploaded_file.name}"
        )

        st.code(
            code,
            language="python"
        )


    # ==========================================
    # AI TUTOR TAB
    # ==========================================

    with tutor_tab:

        st.subheader("💡 Quick Questions")

        quick_question = st.selectbox(
            "Choose a question",
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

        st.subheader("💬 Ask Your Own Question")

        custom_question = st.text_input(
            "Type your question about the code"
        )


        st.write("")


        # ==========================================
        # ASK AI BUTTON
        # ==========================================

        if st.button(
            "🤖 Ask AI",
            type="primary",
            use_container_width=True
        ):

            # ==========================================
            # SELECT QUESTION
            # ==========================================

            if custom_question.strip():

                question = custom_question.strip()

            else:

                question = quick_question


            # ==========================================
            # AI REQUEST
            # ==========================================

            with st.spinner(
                "🤖 AI is analyzing your code..."
            ):

                try:

                    response = ollama.chat(

                        model="llama3.2",

                        messages=[

                            {
                                "role": "system",

                                "content": (
                                    "You are a beginner-friendly "
                                    "Python programming tutor. "
                                    "Explain code clearly and simply. "
                                    "Break complex concepts into "
                                    "smaller parts. "
                                    "Use examples when helpful. "
                                    "Base your explanation on "
                                    "the uploaded Python code."
                                )
                            },

                            {
                                "role": "user",

                                "content": (
                                    f"Here is the Python code:\n\n"
                                    f"{code}\n\n"
                                    f"Student's question:\n\n"
                                    f"{question}"
                                )
                            }

                        ]
                    )


                    # ==========================================
                    # AI RESPONSE
                    # ==========================================

                    st.divider()

                    st.subheader(
                        "🤖 AI Explanation"
                    )

                    st.info(
                        f"Question: {question}"
                    )

                    st.write(
                        response["message"]["content"]
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

    st.info(
        "👆 Upload a Python file above to get started."
    )

    st.markdown(
        """
        ### What can you ask?

        - **Explain this code** — Get an overview of the program.
        - **Explain the functions** — Understand what each function does.
        - **Explain the execution flow** — Understand what happens first, second, third, etc.
        - **Explain the data flow** — Understand how data moves through the program.
        - **Find potential issues** — Ask the AI to identify possible problems.
        """
    )