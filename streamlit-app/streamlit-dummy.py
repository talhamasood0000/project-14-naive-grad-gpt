import streamlit as st

def intro_page():
    # Hide Sidebar
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide")
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main Code
    if "forcefully" in st.session_state:
        del st.session_state["forcefully"]

    st.title("Fatebound Chronicles: Choose Your Destiny")
    st.markdown(
        f"""
            <div style="display: flex; justify-content: center;">
            <img src="https://static0.gamerantimages.com/wordpress/wp-content/uploads/wm/2023/03/best-multiplayer-rpg-games-featured-image.jpg" style="width: 100%; height: auto;"></div>
        """,
        unsafe_allow_html=True
    )
    st.write('<div style="text-align: center; padding: 20px;">Click the button below to begin your journey.</div>', unsafe_allow_html=True)

    if st.button("Start Game"):
        st.switch_page("pages/start_game.py")
    
intro_page()
