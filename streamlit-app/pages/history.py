import streamlit as st

def handle_back_to_game():
    if "history" in st.session_state and not st.session_state.history:
        st.session_state.history = True
        st.session_state.qupdate = False
        

def history_page():
    if "history" in st.session_state and st.session_state.history:
        del st.session_state["history"]
        st.switch_page("pages/start_game.py")
        
    st.title("Your History")
    st.button("Go back to game", on_click=handle_back_to_game)

    for message in st.session_state.history_data:
        with st.chat_message("assistant"):
            st.markdown(message["story"])

        with st.chat_message("user"):
            st.markdown(message["option"])


history_page()
