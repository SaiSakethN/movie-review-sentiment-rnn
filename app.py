import numpy as np
import tensorflow as tf
import streamlit as st

from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence

# Load word index
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}

# Load trained model
model = load_model('model/sentiment_rnn_model.h5')

# Function to decode review
def decode_review(encoded_review):
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

# Function to preprocess input review
def preprocess_review(review):
    words = review.lower().split()
    encoded_review = []

    for word in words:
        index = word_index.get(word)
        if index is not None and (index + 3) < 10000:
            encoded_review.append(index + 3)
        else:
            encoded_review.append(2)   # unknown word

    padded_review = sequence.pad_sequences([encoded_review], maxlen=500)
    return padded_review

# Prediction function
def predict_review(review):
    preprocessed_review = preprocess_review(review)
    prediction = model.predict(preprocessed_review, verbose=0)[0][0]

    sentiment = 'positive' if prediction >= 0.5 else 'negative'
    confidence = prediction if prediction >= 0.5 else 1 - prediction

    return f"Predicted sentiment: {sentiment} (confidence: {confidence:.2f})"

# Streamlit UI
st.title("Movie Review Sentiment Analysis")
review_input = st.text_area("Enter a movie review:")

if st.button("Predict Sentiment"):
    if review_input.strip():
        result = predict_review(review_input)
        st.write(result)
    else:
        st.warning("Please enter a movie review.")