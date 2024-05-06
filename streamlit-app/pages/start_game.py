import requests
import random
import time
import streamlit as st
from PIL import Image
from io import BytesIO
from openai import OpenAI

URL = "https://d07c-35-204-102-30.ngrok-free.app/generate"
client = OpenAI(api_key="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")

def get_response(story=None, initial=False, rag_query=None):
    if URL:
        if initial:
            json = {
                "story": "",
                "rag_query": ""
            }
        if rag_query:
            json = {
                "story": story,
                "rag_query": rag_query
            }
        else:
            json = {
                "story": story,
                "rag_query": ""
            }
        with st.spinner('Wait for it...'):
            request = requests.post(
                url=URL,  
                json=json
            )
            if request.status_code == 200:
                if not rag_query:
                    response = {
                        "role": "assistant",
                        "content": {
                            "story": request.json()["story"],
                            "options": request.json()["options"],
                            "outcome": request.json()["outcomes"],
                            "damage": list(map(int, request.json()["points"])),
                            "image_prompt": request.json()["image_prompt"],
                            "rag_response": "",
                    }
                }
                else:
                    response = {
                        "role": "assistant",
                        "content": {
                            "story": "",
                            "options": "",
                            "outcome": "",
                            "damage": "",
                            "image_prompt": "",
                            "rag_response": request.json()["rag_response"],
                    }
                }
            else:
                st.error("Something went wrong. Please Try again", icon="🚨")
        return response

def get_image(prompt=None):
    value = "You have been given a scene of a game below. Generate an image of this scene. The genere must be realistic game. Following is the scene."
    prompt = value + st.session_state.response["content"]["image_prompt"]
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def handle_option_click(selected_option, options, damage, outcome):
    st.session_state.selected_option = selected_option
    option_index = options.index(selected_option)
    st.session_state.outcome = outcome[option_index]
    st.session_state.health -= damage[option_index]
    st.session_state.total_questions_answered += 1

    st.session_state.history_data.append({
        "story": st.session_state.response["content"]["story"],
        "option": st.session_state.selected_option
    })

def handle_history_page():
    st.session_state.history = True

def handle_back_page():
    st.session_state.forcefully = True
    st.session_state.history_data = []

def check_health():
    if st.session_state.health <= 0:
        del st.session_state["response"]
        del st.session_state["image"]
        del st.session_state["selected_option"]
        del st.session_state["health"]
        
        st.switch_page("pages/end_game.py")

def create_initial_data():
    if "response" not in st.session_state:
        st.session_state.response = get_response(initial=True) # Intial Text Prompt
    if "rag_response" not in st.session_state:
        st.session_state.rag_response = ""
    if "image" not in st.session_state:
        st.session_state.image = get_image() # Initial Image Prompt?
    if "narrative" not in st.session_state:
        st.session_state.narrative = None
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
    if "outcome" not in st.session_state:
        st.session_state.outcome = None
    if "health" not in st.session_state:
        st.session_state.health = 50
    if "total_questions_answered" not in st.session_state:
        st.session_state.total_questions_answered = 0
    if "forcefully" not in st.session_state:
        st.session_state.forcefully = False
    if "history" not in st.session_state:
        st.session_state.history = False
    if "history_data" not in st.session_state:
        st.session_state.history_data = []
    if "qupdate" not in st.session_state:
        st.session_state.qupdate = True

def submit():    
    rag_response = get_response(story=st.session_state.narrative, rag_query=st.session_state.text_widget)
    st.session_state.rag_response = ""
    st.session_state.rag_response = rag_response["content"]["rag_response"]
    st.session_state.text_widget = ""

js = """
<script>
    var body = window.parent.document.querySelector(".main");
    body.scrollTop = 0;
</script>
"""

def start_game():
    # Go back to start page and reset everything
    if "forcefully" in st.session_state and st.session_state.forcefully:
        del st.session_state["response"]
        del st.session_state["image"]
        del st.session_state["selected_option"]
        del st.session_state["health"]
        st.session_state.forcefully = False
        st.switch_page("streamlit-dummy.py")
    
    # Go to history Pgae
    if "history" in st.session_state and st.session_state.history:
        st.session_state.history = False
        st.switch_page("pages/history.py")

    # Create Initial data
    st.title("Choice-Based Game")
    create_initial_data()

    # Health Bar and history button
    st.divider()
    
    health_col, hiistory_col, exit_game_col = st.columns(3)
    with health_col:
        st.write("Health Remaining:", st.session_state.health)
    with hiistory_col:
        st.button("Your History", on_click=handle_history_page)
    with exit_game_col:
        st.button("Goto start page", on_click=handle_back_page)

    st.divider()

    # Check health and redirect to last page of the game is ended
    check_health()

    # If an option is selected, fetch next response
    if st.session_state.selected_option and st.session_state.qupdate:
        request_story = st.session_state.response["content"]["story"]
        request_outcome = st.session_state.outcome
        request_image = st.session_state.response["content"]["image_prompt"]

        st.session_state.narrative = (st.session_state.narrative or "") + request_story + " " + request_outcome
        st.session_state.response = get_response(story=st.session_state.narrative)
        st.session_state.image = get_image(prompt=request_image)
    else:
        st.session_state.qupdate = True
    
    # Parse Response
    story = st.session_state.response["content"]["story"]
    options = st.session_state.response["content"]["options"]
    outcome = st.session_state.response["content"]["outcome"]
    damage = st.session_state.response["content"]["damage"]
    image_url = st.session_state.image

    response_image = requests.get(image_url)
    image = Image.open(BytesIO(response_image.content))

    # Create Initial Scenario
    st.write(story)
    _, cent_co, _ = st.columns(3)
    with cent_co:
        st.image(image, width=512)
        
    for option in options:
        if st.button(option, key=option, on_click=lambda option=option: handle_option_click(option, options, damage, outcome)):
            temp = st.empty()
            with temp:
                st.components.v1.html(js)
                time.sleep(.25) # To make sure the script can execute before being deleted
            temp.empty()

    output = st.text_input(
        "Take hints 👇",
        placeholder="Ask about anything related to the story",
        key="text_widget", 
        on_change=submit
    )
    
    if st.session_state.rag_response:
        st.markdown(st.session_state.rag_response)
    
    if not st.session_state.rag_response:
        st.markdown("")

start_game()

