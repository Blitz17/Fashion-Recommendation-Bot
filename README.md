# StyleMate - Multimodal Fashion Recommendation Bot

StyleMate is a multimodal fashion recommendation system built using Python and Azure AI services.

The project combines:
- Azure AI Vision
- Azure OpenAI
- Streamlit
- weighted recommendation ranking
- multimodal image + text understanding

## Features

- Upload clothing images
- Enter natural language fashion requests
- Azure Vision image analysis
- Azure OpenAI intent extraction
- AI-generated recommendation explanations
- Ranked fashion recommendations

## Technologies Used

- Python
- Streamlit
- Azure AI Vision
- Azure OpenAI
- Pandas

## Dataset

Fashion Product Images Dataset:
https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small

Download, extract and add this in a folder called "dataset" in your root folder.

## Run Locally
Create Azure AI service and Azure OpenAI resources and enter the key and endpoints in .env file
Install dependencies:
pip install -r requirements.txt
Run application: 
streamlit run app.py