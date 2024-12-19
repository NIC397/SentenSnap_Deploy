import streamlit as st
from senten_snap import SentenSnap
import sys
import os
import string  # Import the string module for handling punctuation
import wordfreq  # For evaluating word difficulty based on frequency

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class SentenSnapUI:
    def __init__(self):
        self.senten_snap = None
        self.quote_result = None  # To store the generated quote result
        self.definition_result = None  # To store the word definition result

    def render_sidebar(self):
        st.sidebar.header("Settings")
        api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")
        if api_key:
            self.senten_snap = SentenSnap(gemini_api_key=api_key)

    def render_home_page(self):
        st.title("🌟 Welcome to SentenSnap")
        st.markdown(
            "Explore **motivational quotes** and get **detailed word definitions** with ease!"
        )
        st.markdown("---")

        # Expandable sections with mutual exclusivity
        with st.expander("📜 Generate a Random Quote", expanded=st.session_state.get("quote_expanded", False)):
            # Set session state for mutual exclusivity
            if not st.session_state.get("quote_expanded", False):
                st.session_state["quote_expanded"] = True
                st.session_state["definition_expanded"] = False

            self.render_quote_section()

        with st.expander("📚 Get a Word Definition", expanded=st.session_state.get("definition_expanded", False)):
            # Set session state for mutual exclusivity
            if not st.session_state.get("definition_expanded", False):
                st.session_state["definition_expanded"] = True
                st.session_state["quote_expanded"] = False

            self.render_definition_section()


    def render_quote_section(self):
        # Ensure session state initialization
        if "clicked_word" not in st.session_state:
            st.session_state["clicked_word"] = None

        # Section 1: Display Quote Words Prettily (Non-clickable)
        st.write("Click the button below to generate a motivational quote.")
        if st.button("Generate Random Quote"):
            if not self.senten_snap:
                st.error("Please enter your Gemini API key in the sidebar.")
            else:
                st.session_state["definition_expanded"] = False
                st.session_state["quote_result"] = self.fetch_random_quote()

        if "quote_result" in st.session_state and st.session_state["quote_result"]:
            st.subheader("Random Quote")
            quote = st.session_state["quote_result"].get('Quote', 'No quote available.')
            words = quote.split()

            # Display words prettily (non-clickable)
            st.markdown(
                " ".join([f"<span style='font-size:18px; margin:4px;'>{word}</span>" for word in words]),
                unsafe_allow_html=True,
            )

            author = st.session_state["quote_result"].get("Author", "Unknown")
            source_type = st.session_state["quote_result"].get("Source Type", "Unknown Source Type")
            context = st.session_state["quote_result"].get("Context", "")
            st.write(f"— {author}")
            st.write(f"Source Type: {source_type}")
            st.write(f"Context: {context}")

            # Section 2: Display Unique Words in a Table (Clickable)
            st.markdown("---")
            st.subheader("Words in Quote (Clickable for Snapshots)")

            # Get unique words (remove punctuation and ignore case)
            unique_words = set(
                word.translate(str.maketrans("", "", string.punctuation)).lower()
                for word in words
            )
            
            # Compute difficulty and sort from hard to easy
            words_with_difficulty = [
                (word, self.get_word_difficulty(word), self.get_difficulty_rank(word))
                for word in unique_words if word
            ]
            words_with_difficulty.sort(key=lambda x: x[2], reverse=True)  # Sort by difficulty rank (higher rank = harder)

            # Create a Streamlit-based table layout
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.markdown("**Word**")
            col2.markdown("**Difficulty**")
            col3.markdown("**Action**")

            for word, difficulty, _ in words_with_difficulty:
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(word)
                col2.write(difficulty)
                if col3.button("Get Snapshot", key=f"word_{word}"):
                    st.session_state["clicked_word"] = word  # Store clicked word in session state

            # Display definition in the sidebar
            if st.session_state["clicked_word"]:
                word = st.session_state["clicked_word"]
                with st.sidebar:
                    st.header("Word Snapshot")
                    st.subheader(f"{word}")
                    definition = self.fetch_definition(word)
                    if definition:
                        st.write(f"**Definition:** {definition.get('Definition', 'No definition available.')}")
                        st.write(f"**Part of Speech:** {definition.get('Part of Speech', 'N/A')}")
                        synonyms = definition.get('Synonyms', 'N/A')
                        if synonyms != 'N/A':
                            synonyms_list = synonyms.split(", ")
                            st.write(f"**Synonyms:** {', '.join(synonyms_list)}")
                        else:
                            st.write(f"**Synonyms:** N/A")
                        st.write(f"**Example Sentence:** {definition.get('Example Sentence', 'N/A')}")

    def get_word_difficulty(self, word):
        """
        Calculate the difficulty level of a word based on frequency.
        Uses the 'wordfreq' package.
        """
        try:
            freq = wordfreq.word_frequency(word, 'en')  # Get word frequency in English
            if freq > 0.001:
                return "Easy"
            elif 0.00001 < freq <= 0.001:
                return "Medium"
            else:
                return "Hard"
        except Exception as e:
            return "Unknown"

    def get_difficulty_rank(self, word):
        """
        Get a numeric difficulty rank for sorting (higher = harder).
        """
        try:
            freq = wordfreq.word_frequency(word, 'en')  # Get word frequency in English
            if freq > 0.001:
                return 1  # Easy
            elif 0.00001 < freq <= 0.001:
                return 2  # Medium
            else:
                return 3  # Hard
        except Exception as e:
            return 0  # Unknown or error

    def render_definition_section(self):
        """
        Render the word definition section.
        """
        word = st.text_input(
            "Enter a word to search for its definition:",
            placeholder="Type a word here...",
        )

        if st.button("Search Word Definition"):
            if not self.senten_snap:
                st.error("Please enter your Gemini API key in the sidebar.")
            elif not word:
                st.error("Please enter a word to search.")
            else:
                st.session_state["quote_expanded"] = False
                self.definition_result = self.fetch_definition(word)

        # Display the fetched definition if available
        if self.definition_result:
            st.subheader(self.definition_result.get('Word', 'Unknown'))
            st.write(f"**Definition:** {self.definition_result.get('Definition', 'No definition available.')}")
            st.write(f"**Part of Speech:** {self.definition_result.get('Part of Speech', 'N/A')}")
            synonyms = self.definition_result.get('Synonyms', 'N/A')
            if synonyms != 'N/A':
                synonyms_list = synonyms.split(", ")
                st.write(f"**Synonyms:** {', '.join(synonyms_list)}")
            else:
                st.write(f"**Synonyms:** N/A")
            st.write(f"**Example Sentence:** {self.definition_result.get('Example Sentence', 'N/A')}")

    def fetch_random_quote(self):
        """
        Fetch a random quote from the backend and parse it.
        """
        raw_response = self.senten_snap.generate_random_quote()
        
        if "error" in raw_response:
            st.error(raw_response["error"])
            return None
        print("Quote Raw:", raw_response)
        return raw_response

    def fetch_definition(self, word):
        """
        Fetch a word definition from the backend and parse it.
        """
        raw_response = self.senten_snap.define_word(word)
        
        if "error" in raw_response:
            st.error(raw_response["error"])
            return None
        
        # Add the searched word to the result for display purposes
        raw_response["Word"] = word
        return raw_response


# Main entry point for the Streamlit app
if __name__ == "__main__":
    # Initialize session state for expand/collapse functionality
    if "quote_expanded" not in st.session_state:
        st.session_state["quote_expanded"] = False
    if "definition_expanded" not in st.session_state:
        st.session_state["definition_expanded"] = False

    ui = SentenSnapUI()
    ui.render_sidebar()
    ui.render_home_page()
