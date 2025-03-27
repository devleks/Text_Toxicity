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

review_text = st.text_area("Text to reviewed",
                            placeholder="We in these hot ass Texas streets, honey. Y’all know we got Governor Hot Wheels down there, Come on now! And the only thing hot about him is that he is a hot ass mess, honey! So, um, so yes! Yes, yes, yes.Jasmine Crocket",
                            )

safety = st.slider('Personalize Safer Value: (larger value is less safe)',
                   min_value=0.005,max_value=0.1,value=0.02,step=0.005)

eval_result = get_toxic(review_text,safety)
processed_metrics = process_metrics(eval_result[1])

chart,metric = st.columns(2)

with chart:
    st.subheader('Rating')
    st.pyplot(display_outcome((eval_result[0]['plot'][23::])))
with metric:
    st.subheader('Json Output')
    st.dataframe(processed_metrics,column_config={'':'Key','value':'Value'})
