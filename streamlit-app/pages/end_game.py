import streamlit as st

def clear_history():
    if "history_data" in st.session_state:
        st.session_state.history_data = []

def last_page():
    st.title("Fatebound Chronicles: Choose Your Destiny")
    st.markdown(
        f"""
            <div style="display: flex; justify-content: center;">
            <img src="https://static0.gamerantimages.com/wordpress/wp-content/uploads/wm/2023/03/best-multiplayer-rpg-games-featured-image.jpg" style="width: 100%; height: auto;"></div>
        """,
        unsafe_allow_html=True
    )
    if "total_questions_answered" in st.session_state:
        st.write("Total questions you answered are:", st.session_state.total_questions_answered)
        del st.session_state["total_questions_answered"]

    st.write("The game has ended")
    if st.button("Play the game again"):
        clear_history()
        st.switch_page("streamlit-dummy.py")

last_page()
