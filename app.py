import streamlit as st
import os
from api_key import api_key
from pathlib import Path
import google.generativeai as genai

# Configure Generative AI with API key
genai.configure(api_key=auth_key)

def upload_to_gemini(file_data, mime_type=None):
    with open(file_data.name, 'wb') as f:
        f.write(file_data.getbuffer())

    file = genai.upload_file(file_data.name, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file
# Define model generation configuration and system prompt

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your responsibilities include:
1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings that may indicate underlying medical conditions.
2. Finding Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured report format, ensuring accuracy and clarity.
3. Recommendations and Next Steps: Provide detailed recommendations based on your findings. Outline the necessary follow-up actions or additional tests required to confirm diagnoses or assess treatment options.
4. Treatment Suggestions: Offer preliminary treatment suggestions or interventions based on the identified conditions, collaborating with the healthcare team to develop comprehensive patient care plans.

Important Notes:
1. Scope of Response: Only respond if the image pertains to a human health issue.
2. Clarity of Image: Ensure the image is clear and suitable for accurate analysis.
3. Disclaimer: Accompany your analysis with the disclaimer: “Consult with a doctor before making any decisions.”
4. Your Insights are Invaluable: Your insights play a crucial role in guiding clinical decisions. Please proceed with your analysis, adhering to the structured approach outlined above.
"""

# Initialize GenerativeModel
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Set Streamlit page configuration
st.set_page_config(page_title="VitalImage Analysis", page_icon=":robot:")

# Display title and image
st.image('img.jpeg', width=150)
st.title("🥼 Vital🩻Image Analysis 📊")
st.subheader("An app that assists users in effortlessly recognizing medical images.")

# File uploader and submit button
uploaded_file = st.file_uploader('Upload Medical Images', type=['png', 'jpg', 'jpeg'])
submit_button = st.button('Generate Analysis')

# Process on submit
if submit_button:
    if uploaded_file is not None:
        files = upload_to_gemini(uploaded_file, mime_type="image/webp")
        # Rest of your code
    else:
        st.warning("Please upload a file.")
    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            files,
            "describe what people are doing in this image. what is going on in this particular image?",
        ],
        },
        {
        "role": "model",
        "parts": [
            "This is a cricket match, likely a world cup game given the logos on the field and players uniforms. \n\n* **Batter:** A batsman wearing an England cricket uniform is driving the ball,  having just made contact with the cricket ball.  You can tell he's playing a drive shot by the positioning of his body, and bat. \n* **Wicketkeeper:** An Australian wicketkeeper crouched behind the stumps is watching the ball intently. \n* **Fielder:** Another Australian fielder,  also in yellow, is moving towards the direction of the ball, ready to field it if it passes the batsman. \n\nThe intensity of the moment suggests that every run matters and the outcome of the game could be on the line. \n",
        ],
        },
        {
        "role": "user",
        "parts": [
            "As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.\n\nYour responsibilities include:\n\n\t1.\tDetailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings that may indicate underlying medical conditions.\n\t2.\tFinding Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured report format, ensuring accuracy and clarity.\n\t3.\tRecommendations and Next Steps: Provide detailed recommendations based on your findings. Outline the necessary follow-up actions or additional tests required to confirm diagnoses or assess treatment options.\n\t4.\tTreatment Suggestions: Offer preliminary treatment suggestions or interventions based on the identified conditions, collaborating with the healthcare team to develop comprehensive patient care plans.\n\nImportant Notes:\n\n\t1.\tScope of Response: Only respond if the image pertains to a human health issue.\n\t2.\tClarity of Image: Ensure the image is clear and suitable for accurate analysis.\n\t3.\tDisclaimer: Accompany your analysis with the disclaimer: “Consult with a doctor before making any decisions.”\n\t4.\tYour Insights are Invaluable: Your insights play a crucial role in guiding clinical decisions. Please proceed with your analysis, adhering to the structured approach outlined above.\n",
        ],
        },
        {
        "role": "model",
        "parts": [
            "Please provide me with the medical image you would like me to analyze. I will do my best to provide a detailed analysis, but please remember that my insights should not be taken as a substitute for professional medical advice. \n\nPlease also tell me what type of medical image it is (e.g., X-ray, MRI, CT scan) and any relevant patient history or symptoms you are able to share. This will help me to provide a more accurate and helpful analysis. \n",
        ],
        },
    ]
    )
    st.title('Here is the Analysis of your image:')
    response = chat_session.send_message("INSERT_INPUT_HERE")
    st.image(uploaded_file,width = 250)
    st.write(response.text)
