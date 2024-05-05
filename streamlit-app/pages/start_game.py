import requests
import random
import time
import streamlit as st
from PIL import Image
from io import BytesIO
import openai
import webbrowser
import os
from openai import OpenAI

URL = "https://4880-34-82-255-200.ngrok-free.app/generate"
URL = None
client = OpenAI(api_key="sk-proj-CRnpmaZkHV4qn6PGlqtjT3BlbkFJ8npwUtczrwt6hCGyo1rr")

def get_response(option=None, story=None, initial=False):
    random_sentences = [
        "She found the key to unlock her lost memories.",
        "Stars whispered secrets as they danced across the midnight sky.",
        "In the abandoned house, shadows whispered secrets from the past.",
        "With a single step, he leapt into the unknown abyss.",
        "Their laughter echoed through the empty streets, filling the void."
    ]
    random_choices = [
        "The only way to do great work is to love what you do.",
        "You miss 100% of the shots you don't take.",
        "Exploring the ancient ruins of Machu Picchu in Peru.",
        "Relaxing on the pristine beaches of the Maldives.",
        "A young entrepreneur's journey from rags to riches.",
        "A community coming together to rebuild after a natural disaster.",
        "Humanity colonizing distant planets in the far reaches of space.",
        "The signing of the Declaration of Independence in 1776.",
        "Scaling the towering peaks of the Himalayas.",
        "Discovering hidden portals to mythical worlds."
    ]

    random_health = [5, 5, 5]
    index = random.randint(0, 2)
    random_health[index] = 0
    
    if URL:
        if initial:
            json = {
                    "story": "A soft, gentle voice echoes through the quiet forest, 'Hello?'. The sun begins to set as you ponder the origin of the voice.",
                    "input": "Follow the sound of the voice."
                }
        else:
            json = {
                "story": story,
                "input": option
            }
        with st.spinner('Wait for it...'):
            request = requests.post(
                url=URL,  
                json=json
            )
            if request.status_code == 200:
                response = {
                "role": "assistant",
                "content": {
                    "story": request.json()["story"],
                    "options": request.json()["options"],
                    "damage": list(map(int, request.json()["points"]))
                }
            }
            else:
                st.error("Something went wrong. Please Try again", icon="🚨")
        return response

    response = {
            "role": "assistant",
            "content": {
                "story": random.choice(random_sentences),
                "options": random.sample([choice for choice in random_choices], 3),
                "damage": random_health
                }
            }
    return response

def get_image(prompt=None):
    if URL and prompt:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    random_images = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZkkoLbCK69Monn00MVYWKl6kl3qGyaqRlI4Hk214_AXRA9BHCEgMDSjqQZMEgg8WJgrE&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4GafvNRN5SNrIxDJJs3dpR268DdIH7hgIHn7MPvN22qS94HA30J2kuoDQBz5SSz5te-g&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLmMHImjTDFUv0kH2Z2J-8_Hj617-KkiYw7zotlDcluA&s",
        "https://assets-global.website-files.com/5efc0159f9a97ba05a8b2902/65aa1ac269daf6c1b2e635db_map-editor.webp",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBVbr7KqdbIkeRRhMyh213ULH9VHCCwkCrhqKIj-pfXQ&s",
    ]
    return random.choice(random_images)

def handle_option_click(selected_option, options, damage):
    st.session_state.selected_option = selected_option
    option_index = options.index(selected_option)
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
    if "image" not in st.session_state:
        st.session_state.image = get_image() # Initial Image Prompt?
    if "selected_option" not in st.session_state:
        st.session_state.selected_option = None
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
        request_option = st.session_state.selected_option

        st.session_state.response = get_response(option=request_option, story=request_story)
        st.session_state.image = get_image(prompt=request_story)
    else:
        st.session_state.qupdate = True
    
    # Parse Response
    story = st.session_state.response["content"]["story"]
    options = st.session_state.response["content"]["options"]
    damage = st.session_state.response["content"]["damage"]
    image_url = st.session_state.image

    response_image = requests.get(image_url)
    image = Image.open(BytesIO(response_image.content))

    # Create Initial Scenario
    st.write(story)
    st.image(image)
    for option in options:
        if st.button(option, key=option, on_click=lambda option=option: handle_option_click(option, options, damage)):
            temp = st.empty()
            with temp:
                st.components.v1.html(js)
                time.sleep(.25) # To make sure the script can execute before being deleted
            temp.empty()

start_game()

