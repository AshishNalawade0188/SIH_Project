import pandas as pd
from textblob import TextBlob
import os

# File path
input_file = r"E:\Project\feedback\feedback.csv"

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    # Using TextBlob to get the sentiment polarity of the feedback
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    
    # Classifying the feedback as Positive, Negative, or Neutral based on polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Read the feedback data and perform sentiment analysis
def process_feedback():
    try:
        # Check if the file exists
        if not os.path.exists(input_file):
            print(f"File '{input_file}' not found.")
            return None
        
        # Attempt to read the dataset with different encodings
        try:
            data = pd.read_csv(input_file, encoding='utf-8')
        except UnicodeDecodeError:
            print("UTF-8 decoding failed, trying 'ISO-8859-1' encoding.")
            data = pd.read_csv(input_file, encoding='ISO-8859-1')  # Trying an alternate encoding
        
        # Ensure that the 'Feedback' column exists in the dataset
        if 'Feedback' not in data.columns:
            print("The 'Feedback' column is missing in the dataset.")
            return None
        
        # Apply sentiment analysis to each row in the 'Feedback' column
        data['Sentiment'] = data['Feedback'].apply(analyze_sentiment)
        
        # Save the updated dataset to a new file (to avoid overwriting the original file)
        output_file = r"E:\Project\feedback\feedback_with_sentiment.csv"  # Updated file path
        data.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Sentiment analysis completed and saved to '{output_file}'")
        return data
    except Exception as e:
        print(f"Error processing feedback: {e}")
        return None

# Main function to run the sentiment analysis
if __name__ == "__main__":
    process_feedback()
