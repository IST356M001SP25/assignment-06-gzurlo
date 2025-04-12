import streamlit as st
import pandas as pd
import requests
import json
import os
from pandas import json_normalize

if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition
else:
    from code.apicalls import get_google_place_details, get_azure_sentiment, get_azure_named_entity_recognition

# Define paths with proper directory creation
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # Create cache directory if it doesn't exist

PLACE_IDS_SOURCE_FILE = os.path.join(CACHE_DIR, "place_ids.csv")
CACHE_REVIEWS_FILE = os.path.join(CACHE_DIR, "reviews.csv")
CACHE_SENTIMENT_FILE = os.path.join(CACHE_DIR, "reviews_sentiment_by_sentence.csv")
CACHE_ENTITIES_FILE = os.path.join(CACHE_DIR, "reviews_sentiment_by_sentence_with_entities.csv")

def reviews_step(place_ids: str|pd.DataFrame) -> pd.DataFrame:
    '''
    Step 1: Get reviews for each place ID
    Input: place_ids (filename or DataFrame)
    Output: DataFrame with columns: place_id, name, author_name, rating, text
    '''
    # Read input if it's a filename
    if isinstance(place_ids, str):
        try:
            place_ids = pd.read_csv(place_ids)
        except FileNotFoundError:
            st.error(f"Input file not found: {place_ids}")
            return pd.DataFrame()  # Return empty DataFrame to prevent further errors
    
    reviews_list = []
    
    for _, row in place_ids.iterrows():
        place_id = row['place_id']
        response = get_google_place_details(place_id)
        
        if 'result' in response:
            place_data = response['result']
            place_name = place_data.get('name', '')
            
            # Normalize reviews and add place info
            if 'reviews' in place_data:
                for review in place_data['reviews']:
                    reviews_list.append({
                        'place_id': place_id,
                        'name': place_name,
                        'author_name': review.get('author_name', ''),
                        'rating': review.get('rating', 0),
                        'text': review.get('text', '')
                    })
    
    # Create DataFrame and save to cache
    reviews_df = pd.DataFrame(reviews_list)
    reviews_df.to_csv(CACHE_REVIEWS_FILE, index=False)
    return reviews_df

# [Rest of your functions remain the same...]

if __name__ == '__main__':
    st.title("ETL Pipeline Debugger")
    
    # Check if input file exists
    if not os.path.exists(PLACE_IDS_SOURCE_FILE):
        st.warning(f"Input file {PLACE_IDS_SOURCE_FILE} not found. Please ensure it exists.")
        # You could add a file uploader here as a fallback
        uploaded_file = st.file_uploader("Or upload place_ids.csv", type="csv")
        if uploaded_file is not None:
            # Save uploaded file to cache directory
            with open(PLACE_IDS_SOURCE_FILE, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File saved to {PLACE_IDS_SOURCE_FILE}")
    
    option = st.selectbox(
        "What do you want to debug?",
        ("Full Pipeline", "Reviews Step", "Sentiment Step", "Entity Extraction Step")
    )
    
    if st.button("Run Selected Step"):
        if option == "Full Pipeline":
            if os.path.exists(PLACE_IDS_SOURCE_FILE):
                st.write("Running full pipeline...")
                reviews = reviews_step(PLACE_IDS_SOURCE_FILE)
                st.write("Reviews Step Complete", reviews.head())
                
                sentiment = sentiment_step(reviews)
                st.write("Sentiment Step Complete", sentiment.head())
                
                entities = entity_extraction_step(sentiment)
                st.write("Entity Extraction Complete", entities.head())
            else:
                st.error("Cannot run pipeline - input file missing")
                
        elif option == "Reviews Step":
            if os.path.exists(PLACE_IDS_SOURCE_FILE):
                st.write("Running Reviews Step...")
                reviews = reviews_step(PLACE_IDS_SOURCE_FILE)
                st.write("Results:", reviews)
                st.write(f"Saved to {CACHE_REVIEWS_FILE}")
            else:
                st.error("Cannot run Reviews Step - input file missing")
                
        elif option == "Sentiment Step":
            if os.path.exists(CACHE_REVIEWS_FILE):
                st.write("Running Sentiment Step...")
                sentiment = sentiment_step(CACHE_REVIEWS_FILE)
                st.write("Results:", sentiment)
                st.write(f"Saved to {CACHE_SENTIMENT_FILE}")
            else:
                st.error("Cannot run Sentiment Step - reviews file missing. Run Reviews Step first.")
                
        elif option == "Entity Extraction Step":
            if os.path.exists(CACHE_SENTIMENT_FILE):
                st.write("Running Entity Extraction Step...")
                entities = entity_extraction_step(CACHE_SENTIMENT_FILE)
                st.write("Results:", entities)
                st.write(f"Saved to {CACHE_ENTITIES_FILE}")
            else:
                st.error("Cannot run Entity Extraction Step - sentiment file missing. Run Sentiment Step first.")
    
    st.write("Cache Files Status:")
    st.write(f"- Input Place IDs: {os.path.exists(PLACE_IDS_SOURCE_FILE)}")
    st.write(f"- Reviews: {os.path.exists(CACHE_REVIEWS_FILE)}")
    st.write(f"- Sentiment: {os.path.exists(CACHE_SENTIMENT_FILE)}")
    st.write(f"- Entities: {os.path.exists(CACHE_ENTITIES_FILE)}")