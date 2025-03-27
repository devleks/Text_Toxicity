import streamlit as st
from gradio_client import Client
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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
    

review_text = st.text_area("Text to reviewed",
                            placeholder="Enter text for review",
                            )

safety = st.slider('Personalize Safer Value: (larger value is less safe)',
                   min_value=0.005,max_value=0.1,value=0.02,step=0.005)

eval_result = get_toxic(review_text,safety)


st.pyplot(display_outcome((eval_result[0]['plot'][23::])))

