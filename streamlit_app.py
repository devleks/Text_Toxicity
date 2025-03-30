import streamlit as st
from gradio_client import Client
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import json

st.title(" Text Toxicity App")
st.write( "😃 Welcome To The Friendly Text Moderation")


def get_toxic(text,lever):
    client = Client("duchaba/Friendly_Text_Moderation")
    result = client.predict(
            msg=f"{text}",
            safer=lever,
            api_name="/fetch_toxicity_level"
    )
    return result

def display_outcome(encoded_image): 
    # Decode the base64 string
    image_data = base64.b64decode(encoded_image)
    
    # Convert to an image and display
    image = plt.imread(BytesIO(image_data), format='webp')
    
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.axis('off')  # Hide axes

    return fig

def process_metrics(text):
    # Join the list into a single JSON string
    json_string = "".join(text)

    # Convert the string into a JSON object
    json_data = json.loads(json_string)
    return json_data

def get_tweets():
    client = Client("duchaba/Friendly_Text_Moderation")
    result = client.predict(
            api_name="/fetch_toxic_tweets"
    )
    return result


tab1, tab2 = st.tabs(["Enter Text", "Fetch Sample Texts"])

with tab1:
    review_text = st.text_area("Text to reviewed", key="text_input_tab1")
    safety = st.slider('Personalize Safer Value: (larger value is less safe)',
                    min_value=0.005,
                    max_value=0.1,
                    value=0.02,
                    step=0.005,
                    key="safety_slider_tab1"
                    )
    
    if st.button("Measure 14 categories of Text Toxicity", type="primary", key="analyze_button_tab1"):
        eval_result = get_toxic(review_text,safety)
        processed_metrics = process_metrics(eval_result[1])
        img = eval_result[0]['plot'][23::]
        chart,metric = st.columns(2)           
        with chart:
            st.subheader('Toxicity')
            st.pyplot(display_outcome(img))
        with metric:
            st.subheader('Toxicity Categories')
            st.dataframe(processed_metrics,column_config={'':'Catergory','value':'Score'})

with tab2:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("Fetch Toxic Text", type="primary", key="fetch_button_tab2"):
            toxic_tweets = get_tweets()
            tweet = toxic_tweets[1]
            st.session_state['fetched_tweet'] = tweet
            st.session_state['tweet_info'] = toxic_tweets[0]
    
    # Initialize session state for fetched tweet if not exists
    if 'fetched_tweet' not in st.session_state:
        st.session_state['fetched_tweet'] = ""
    if 'tweet_info' not in st.session_state:
        st.session_state['tweet_info'] = ""
    
    # Text area for editing fetched text
    review_text = st.text_area("Text to analyze", 
                             value=st.session_state['fetched_tweet'],
                             height=150,
                             key="text_input_tab2")
    
    safety = st.slider('Personalize Safer Value: (larger value is less safe)',
                    min_value=0.005,
                    max_value=0.1,
                    value=0.02,
                    step=0.005,
                    key="safety_slider_tab2")
    
    # Only show analysis if there's text to analyze
    if review_text:
        if st.button("Analyze Fetched Text", type="primary", key="analyze_button_tab2"):
            eval_result = get_toxic(review_text, safety)
            processed_metrics = process_metrics(eval_result[1])
            img = eval_result[0]['plot'][23::]
            
            chart, metric = st.columns(2)
            with chart:
                st.subheader('Toxicity')
                st.pyplot(display_outcome(img))
            with metric:
                st.subheader('Toxicity Categories')
                st.dataframe(processed_metrics,column_config={'':'Catergory','value':'Score'})
            
            if st.session_state['tweet_info']:
                st.subheader("Original Text Info")
                st.html(st.session_state['tweet_info'])
