# SentenSnap: Motivational Quotes and Word Snapshots

## Note
This application is a modified version of the [SentenSnap](https://github.com/NIC397/SentenSnap "SentenSnap") repository, originally built to run with locally installed large language models (LLMs). The current version leverages [Streamlit](https://streamlit.io/) for its user interface and integrates the [Gemini API](https://ai.google.dev/gemini-api/docs/api-key) to deliver a fully deployed, cloud-based experience. While the image generation functionality from the original version has been omitted, this modification focuses on providing seamless access to motivational quotes and interactive word snapshots without requiring local LLM installations.


## Overview
SentenSnap is a **Streamlit-based application** that allows users to:
- Generate random **motivational quotes**.
- Explore **word snapshots**, which include definitions, part of speech, synonyms, and example sentences.

The application provides two key functionalities for word snapshots:
1. **Clickable Words in Quotes**: Users can click on any word from a generated quote to instantly view its detailed snapshot in the sidebar.
2. **Search Bar Functionality**: Users can search for any word using the input field to retrieve its complete definition and related information.

By leveraging the **Gemini API**, SentenSnap offers an interactive platform for exploring both inspiring quotes and enriching vocabulary.


## Features
### 1. **Motivational Quotes**
- Generate random motivational or inspirational quotes.
- View details such as:
  - Quote text.
  - Author.
  - Source type (e.g., Speech, Book, Movie).
  - Context of the quote.
- Explore unique words in the quote with difficulty levels (Easy, Medium, Hard).

### 2. **Word Definitions**
- Input any word to retrieve:
  - A detailed definition.
  - Part of speech.
  - Synonyms.
  - An example sentence showcasing the word's usage.

### 3. **Interactive Interface**
- Expandable sections for quotes and word definitions with mutual exclusivity for better navigation.
- Sidebar for API key input and displaying word snapshots.


## Usage (Run on Deployed Streamlit App)
1. Access the application by visiting [SentenSnap Streamlit App](https://sentensnap.streamlit.app/).
2. Enter your **Gemini API Key** in the sidebar to enable all functionalities.
3. Explore the following features via the expandable sections:
   - **Generate a Random Quote**: Click the button to fetch a motivational or inspirational quote. Each word in the quote is clickable, allowing you to instantly view its detailed snapshot, including definition, part of speech, synonyms, and example sentences.
   - **Get a Word Definition**: Use the search bar to input any word and retrieve its detailed snapshot, including its definition, part of speech, synonyms, and example sentences.


## Installation (Run Locally)
1. Clone the repository:
```
git clone https://github.com/NIC397/SentenSnap_Deploy.git
```
2. Navigate to the project directory and install dependencies:
```
pip install -r requirements.txt
```
3. Run the application:
```
streamlit run src/streamlit_app.py
```
Once running locally, enter your **Gemini API Key** in the sidebar to enable functionality and use the app as described above.


## Dependencies
- `streamlit`: For building the web interface.
- `google.generativeai`: For interacting with the Gemini API.
- `wordfreq`: For evaluating word difficulty based on frequency.


## Code Structure
| File Name         | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `streamlit_app.py` | Main Streamlit application handling UI and user interactions. |
| `senten_snap.py`   | Backend logic for interacting with Gemini API and processing responses. |


## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Submit a pull request with a detailed description of your changes.

## License
This project is licensed under the Apache-2.0 License.

