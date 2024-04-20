import streamlit as st

# A dummy funtion that acts as an inference endpoint and returns a response from model
def get_response():
    response = {
            "role": "assistant",
            "content": {
                "story": "This is the next scene.",
                "options": ["option-1", "option-2", "option-3"],
                "damage": [5, 0, 0]
                }
            }
    return response

# updates the state variables after a choice is selected
def update_state(damage, selected, user_response):
    st.session_state.hp -= damage
    st.session_state.damage = damage
    st.session_state.past_choices.append(selected)
    st.session_state.messages.append(user_response)
    # append new response
    assistant_response = get_response()
    st.session_state.messages.append(assistant_response)

# cleanup and exit
def finish():
    st.session_state.hp = None
    st.session_state.messages = None
    st.session_state.choices = None
    with st.chat_message("assistant"):
        st.markdown("Better Luck Next Time. Game Ended!")

def main():
    st.title("Choice-Based Dummy Game")

    # Initialize state
    if 'hp' not in st.session_state:
        st.session_state.hp = 10
        st.session_state.damage = 0

    # Display status in sidebar
    with st.sidebar:
        st.write("Health: ", st.session_state.hp)
        st.write("Damage Received: ", st.session_state.damage)

    if "messages" not in st.session_state:
        st.session_state.messages = []
        # A list of history of choices made to render the application history
        st.session_state.past_choices = []
        # Initial response generated in response to the system prompt
        # TODO: brainstorming required to handle this during integration with the LLM endpoint
        initial_response = {
                "role": "assistant",
                "content": {
                    "story": "This is the initial scene.",
                    "options": ["option-1", "option-2", "option-3"],
                    "damage": [0, 0, 5]
                    }
                }
        st.session_state.messages.append(initial_response)

    # Print history if there are any past choices
    if len(st.session_state.past_choices) > 0:
        # The last response always has to be the latest assistant_response (not history)
        for i, message in enumerate(st.session_state.messages[:-1]):
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(message["content"]["story"])
                    # assistant responses are placed at even indices in messages i.e, 0,2,4.. therefore, i needs to be divided by 2
                    st.radio("", message["content"]["options"], label_visibility="collapsed", disabled=True, index=st.session_state.past_choices[i//2], key=i)
                elif message["role"] == "user":
                    st.markdown(message["content"])

    if st.session_state.hp > 0:
        # Deal with the latest response from LLM
        message = st.session_state.messages[-1]
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                response = message["content"]
                st.markdown(response["story"])
                option = None
                option = st.radio("", response["options"], index=None, label_visibility="collapsed")
                if option:
                    selected = [i for i, opt in enumerate(response["options"]) if opt == option][0] # integer
                    damage = response["damage"][selected]
                    user_response = {
                            "role": "user",
                            "content": f"I choose to go with the option, {option} "
                            }
                    st.button('Proceed', on_click=update_state, args=[damage, selected, user_response])
            else:
                st.warning("Something went wrong!")
                st.stop()
    else:
        finish()

if __name__ == "__main__":
    main()
