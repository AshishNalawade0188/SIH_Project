import time
import os
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from textblob import TextBlob
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# File paths
input_file = r"E:\Project\feedback\feedback_with_sentiment.csv"
output_folder = r"E:\Project\feedback\piechart"  # Folder where the pie chart will be saved

# Email configuration
sender_email = "kutemanjusha4@gmail.com"
receiver_email = ["ashishnalawade683@gmail.com"]
email_password = "ryuu mpuz nkpk xipd"  # Replace with your email password

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Generate feedback-wise recommendations
def generate_feedback_recommendations(feedback, sentiment):
    recommendations = f"Feedback: {feedback}\nSentiment: {sentiment}\n"
    
    if sentiment == "Positive":
        recommendations += "- Thank you for your positive feedback! We are glad you're satisfied.\n- We would love to hear more from you, feel free to share additional thoughts.\n"
    elif sentiment == "Negative":
        recommendations += "- We are sorry to hear about your experience. Please let us know how we can improve.\n- Our customer service team will reach out to you to address your concerns.\n"
    else:  # Neutral
        recommendations += "- Thank you for your feedback. We would like to know more about how we can make your experience better.\n- Your feedback helps us improve.\n"
    
    recommendations += "\n---\n"
    return recommendations

# Process the dataset and update sentiment for the last 7 days
def process_dataset():
    try:
        # Load the dataset
        if not os.path.exists(input_file):
            print(f"File '{input_file}' not found.")
            return None

        data = pd.read_csv(input_file, encoding='utf-8')

        # Check if the dataset has a 'Date' column for filtering by last 7 days
        if 'Date' not in data.columns:
            print("Error: 'Date' column is missing in the dataset.")
            return None

        # Convert 'Date' column to datetime format
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

        # Get today's date and filter data for the last 7 days
        today = datetime.now()
        seven_days_ago = today - timedelta(days=7)

        data_last_7_days = data[data['Date'] >= seven_days_ago]

        if data_last_7_days.empty:
            print("No feedback data available for the last 7 days.")
            return None

        # Analyze sentiment for the filtered data if not already analyzed
        if 'Sentiment' not in data.columns:  # If 'Sentiment' doesn't exist in the entire dataset
            data['Sentiment'] = data['Feedback'].apply(analyze_sentiment)
        
        # Filter data to include only feedback from the last 7 days
        data_last_7_days['Sentiment'] = data_last_7_days['Feedback'].apply(analyze_sentiment)

        # Count sentiment values for the last 7 days
        sentiment_counts = data_last_7_days['Sentiment'].value_counts()

        # Save the updated dataset with sentiment values for all feedback
        data.to_csv(input_file, index=False, encoding='utf-8')
        
        return data_last_7_days, sentiment_counts
    except Exception as e:
        print(f"Error processing dataset: {e}")
        return None, None

# Generate a pie chart for sentiment counts
def generate_pie_chart(sentiment_counts):
    try:
        plt.figure(figsize=(6, 6))
        plt.pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=['#28a745', '#dc3545', '#ffc107']
        )
        plt.title("Sentiment Analysis of Feedback (Last 7 Days)")
        
        # Ensure the folder exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the chart in the specified folder
        chart_path = os.path.join(output_folder, "sentiment_pie_chart.png")
        plt.savefig(chart_path)  # Save the chart as an image
        plt.close()  # Close the plot to avoid display issues
        print(f"Pie chart saved at {chart_path}")
    except Exception as e:
        print(f"Error generating pie chart: {e}")

# Generate recommendations based on sentiment percentages
def generate_recommendations(sentiment_counts, data_last_7_days):
    recommendations = ""
    total_feedback = sentiment_counts.sum()
    positive = sentiment_counts.get('Positive', 0)
    negative = sentiment_counts.get('Negative', 0)
    neutral = sentiment_counts.get('Neutral', 0)

    # Calculate percentages
    positive_percentage = (positive / total_feedback) * 100 if total_feedback > 0 else 0
    negative_percentage = (negative / total_feedback) * 100 if total_feedback > 0 else 0
    neutral_percentage = (neutral / total_feedback) * 100 if total_feedback > 0 else 0

    recommendations += f"Sentiment Summary (Last 7 Days):\n"
    recommendations += f"- Total Feedback: {total_feedback}\n"
    recommendations += f"- Positive: {positive} ({positive_percentage:.1f}%)\n"
    recommendations += f"- Negative: {negative} ({negative_percentage:.1f}%)\n"
    recommendations += f"- Neutral: {neutral} ({neutral_percentage:.1f}%)\n\n"

    # Feedback-wise recommendations
    recommendations += "Individual Feedback Recommendations:\n"
    for index, row in data_last_7_days.iterrows():
        sentiment = row['Sentiment']
        feedback = row['Feedback']
        recommendations += generate_feedback_recommendations(feedback, sentiment)

    recommendations += "\nAction Plan: Consider implementing a feedback loop to better understand why users are leaving neutral or negative responses and address those concerns directly."

    print(recommendations)
    return recommendations

# Send an email with recommendations and embed the pie chart in the email body
def send_email(recommendations):
    try:
        # Create email message with HTML content
        subject = "Feedback Analysis and Recommendations (Last 7 Days)"
        body = f"""
        <html>
        <body>
        <h2>Feedback Analysis and Recommendations (Last 7 Days)</h2>
        <p>{recommendations}</p>
        <p>Here is the sentiment analysis pie chart for the feedback received in the last 7 days:</p>
        <img src="cid:sentiment_pie_chart" alt="Sentiment Pie Chart" width="500"/>
        </body>
        </html>
        """
        
        msg = MIMEMultipart('related')
        msg['From'] = sender_email
        msg['To'] = ", ".join(receiver_email)  # Join email addresses with commas
        msg['Subject'] = subject

        # Attach the HTML body
        msg.attach(MIMEText(body, 'html'))

        # Attach pie chart image
        chart_path = os.path.join(output_folder, "sentiment_pie_chart.png")
        if os.path.exists(chart_path):
            with open(chart_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"inline; filename=sentiment_pie_chart.png",
                disposition="inline",
                param={"Content-ID": "<sentiment_pie_chart>"}
            )
            msg.attach(part)

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main function to run with a 7-day delay
def main():
    while True:
        # Run the dataset processing
        data, sentiment_counts = process_dataset()
        if sentiment_counts is not None:
            # Generate pie chart and recommendations
            generate_pie_chart(sentiment_counts)
            recommendations = generate_recommendations(sentiment_counts, data)
            
            # Wait for 7 days (7 * 24 * 60 * 60 seconds) before sending email
            print("Waiting for 7 days before sending the email...")
            time.sleep(7 * 24 * 60 * 60)  # Delay for 7 days
            
            # Send the email after 7 days
            send_email(recommendations)
        
        # Once the email is sent, repeat the process
        print("Waiting for 7 days before starting the process again...")

if __name__ == "__main__":
    print("Starting the process with a 7-day delay before sending emails...")
    main()  # Run the entire process repeatedly with a 7-day delay
