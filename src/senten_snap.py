import google.generativeai as genai


class SentenSnap:
    def __init__(self, gemini_api_key=None):
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def parse_table_response(self, response):
        """
        Parse a table-like response into a dictionary.
        """
        lines = response.strip().split("\n")
        result = {}
        for line in lines:
            if "|" in line:  # Process only table rows
                parts = line.split("|")
                if len(parts) >= 3:  # Ensure valid row with Field and Value
                    field = parts[1].strip()
                    value = parts[2].strip()
                    result[field] = value
        return result

    def define_word(self, word):
        if not self.model:
            return {"error": "Gemini API key not configured"}
        try:
            prompt = f"""
            Provide a detailed definition for the word "{word}". Respond in a table format as follows:

            | Field           | Value                                                                 |
            |------------------|----------------------------------------------------------------------|
            | Definition       | A brief and detailed definition of the word.                        |
            | Part of Speech   | The part of speech for the word (e.g., noun, verb).                 |
            | Synonyms         | synonym1, synonym2, synonym3                                        |
            | Example Sentence | A sentence demonstrating the usage of the word.                    |
            """
            response = self.model.generate_content(prompt)
            raw_response = response.text if response.parts else "No response generated"
            
            return self.parse_table_response(raw_response)
        except Exception as e:
            return {"error": f"Error during word definition retrieval: {e}"}

    def generate_random_quote(self):
        if not self.model:
            return {"error": "Gemini API key not configured"}
        try:
            prompt = """
            Generate a motivational or inspirational quote that is unique, diverse, and not overused. The quote should be sourced from a variety of materials, including but not limited to speeches, books, movies, music lyrics, interviews, and statements by historical figures. Respond in a table format as follows:

            | Field        | Value                                                                 |
            |--------------|----------------------------------------------------------------------|
            | Quote        | "The exact quote, enclosed in quotation marks."                      |
            | Author       | The full name of the person who said or wrote the quote.             |
            | Source Type  | The type of source (e.g., Speech, Book, Movie, Music, Historical Figure). |
            | Context      | A brief explanation of where the quote comes from, including the title of the work (if applicable) and the year. |
            """
            response = self.model.generate_content(prompt)
            raw_response = response.text if response.parts else "No response generated"
            
            return self.parse_table_response(raw_response)
        except Exception as e:
            return {"error": f"Error during random quote generation: {e}"}
    
    def generate_random_knowledge(self):
        if not self.model:
            return {"error": "Gemini API key not configured"}
        try:
            prompt = """
            Generate a random piece of knowledge or trivia that is unique and interesting. The knowledge should be sourced from a variety of materials, including but not limited to scientific facts, historical events, cultural information, and general trivia. Respond in a table format as follows:

            | Field        | Value                                                                 |
            |--------------|----------------------------------------------------------------------|
            | Knowledge    | "The exact piece of knowledge or trivia, enclosed in quotation marks."|
            | Source       | The source of the knowledge or trivia.                                |
            | Context      | A brief explanation of the context or background of the knowledge.    |
            """
            response = self.model.generate_content(prompt)
            raw_response = response.text if response.parts else "No response generated"
            
            return self.parse_table_response(raw_response)
        except Exception as e:
            return {"error": f"Error during random knowledge generation: {e}"}

    def generate_random_book(self):
        if not self.model:
            return {"error": "Gemini API key not configured"}
        try:
            prompt = """
            Genreate a random book and provide information of it in a table format as follows:

            | Field        | Value                                                                |
            |--------------|----------------------------------------------------------------------|
            | Book Title   | The title of the book.                                               |
            | Author       | The full name of the author.                                         |
            | Intro        | A brief introduction and overview of the book.                       |
            | Excerpt      | An excerpt or a famous piece of text of the book.                    |
            """
            response = self.model.generate_content(prompt)
            raw_response = response.text if response.parts else "No response generated"
            
            return self.parse_table_response(raw_response)
        except Exception as e:
            return {"error": f"Error during random book generation: {e}"}