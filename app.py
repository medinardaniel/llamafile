from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="sk-no-key-required"
)

context = (
    "You are a system that removes PHI information from the given text. "
    "You are given a text and you need to replace all PHI information from it with the word <REDACRED>.\n"
    "### SAMPLE INPUT ###\n"
    "Michael Johnson, residing at 789 Pine Road, Gotham, NJ 07030, born on 12/10/1985, "
    "contact number (555) 987-6543, and email michaelj@example.com, "
    "with medical record number MRN2468101214, health plan beneficiary number HPB567890123, and social security number 321-54-6789, "
    "visited the clinic on 06/09/2024. He reports mild chest pain lasting for two days. "
    "Michael, a 38-year-old male, describes the pain as intermittent and localized to the left side, rating it as 3 out of 10. "
    "He is currently taking Aspirin 81 mg daily and has no known allergies. "
    "Physical examination revealed vital signs: BP 120/80 mmHg, HR 72 bpm, RR 16 breaths/min, Temp 98.2°F. "
    "He appeared alert, oriented, and in no acute distress. Cardiovascular examination showed regular rate and rhythm, with no murmurs. "
    "The assessment and plan include ordering an EKG and scheduling a follow-up in one week. "
    "The attending physician, Dr. Emily Carter, can be contacted at drcarter@clinicexample.com or (555) 543-2109. "
    "Her office IP address is 10.0.0.1.\n"
    "### SAMPLE OUTPUT ###\n"
    "<REDACTED>, residing at <REDACTED>, born on <REDACTED>, "
    "contact number <REDACTED>, and email <REDACTED>, "
    "with medical record number <REDACTED>, health plan beneficiary number <REDACTED>, and social security number <REDACTED>, "
    "visited the clinic on <REDACTED>. He reports mild chest pain lasting for two days. "
    "<REDACTED>, a 38-year-old male, describes the pain as intermittent and localized to the left side, rating it as 3 out of 10. "
    "He is currently taking Aspirin 81 mg daily and has no known allergies. "
    "Physical examination revealed vital signs: BP 120/80 mmHg, HR 72 bpm, RR 16 breaths/min, Temp 98.2°F. "
    "He appeared alert, oriented, and in no acute distress. Cardiovascular examination showed regular rate and rhythm, with no murmurs. "
    "The assessment and plan include ordering an EKG and scheduling a follow-up in one week. "
    "The attending physician, <REDACTED>, can be contacted at <REDACTED> or <REDACTED>. "
    "Her office IP address is <REDACTED>.\n"
)

@app.route('/redact', methods=['POST'])
def redact():
    data = request.json
    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": text}
        ]
    )

    response = completion.choices[0].message.content
    return jsonify({'redacted_text': response})

if __name__ == '__main__':
    app.run(debug=True)
