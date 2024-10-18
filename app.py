from flask import Flask, request, jsonify, render_template
import csv
import pandas as pd
import numpy as np

app = Flask(__name__)


def load_data(file_name):
    return pd.read_csv(file_name).to_dict(orient='records')


flu_data = load_data('flu_data.csv')
diabetes_data = load_data('diabetes_data.csv')
asthma_data = load_data('asthma_data.csv')
glaucoma_data = load_data('glaucoma_data.csv')
symptom_description_data = load_data('symptom_Description.csv')  


combined_data = flu_data + diabetes_data + asthma_data + glaucoma_data + symptom_description_data


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message'].lower()

    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    if any(greet in user_message for greet in greetings):
        return jsonify({'response': "Hello! How can I assist you today?"})


    farewells = ["bye", "goodbye", "see you", "take care", "farewell"]
    if any(farewell in user_message for farewell in farewells):
        return jsonify({'response': "Goodbye! Stay safe and take care."})


    symptoms_keywords = ["symptoms", "what is", "what are", "describe", "explain", "define", "name", "How to", "Who"]

   
    for entry in combined_data:
        if any(keyword in user_message for keyword in symptoms_keywords):
            if entry['question'].lower() in user_message:
                return jsonify({'response': entry['answer']})

    return jsonify({'response': "I'm sorry, I don't understand. Please ask another question."})

if __name__ == '__main__':
    app.run(debug=True)
