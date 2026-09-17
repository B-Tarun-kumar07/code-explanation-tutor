import streamlit as st
import ollama


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Code Explanation Tutor",
    page_icon="💻",
    layout="wide"
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

    # Read file
    try:

        code = uploaded_file.read().decode("utf-8")

    except UnicodeDecodeError:

        st.error(
            "❌ Unable to read this file. "
            "Please upload a valid UTF-8 Python file."
        )

        st.stop()


    # Check empty file
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


        st.subheader("💬 Ask Your Own Question")

        custom_question = st.text_input(
            "Type your question about the code"
        )


        st.write("")


        if st.button(
            "🤖 Ask AI",
            type="primary",
            use_container_width=True
        ):

            # Select question
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


else:

    # ==========================================
    # INITIAL STATE
    # ==========================================

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