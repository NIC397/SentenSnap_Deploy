import streamlit as st
from src.core.senten_snap import SentenSnap


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
        """
        Render the random quote generation section.
        """
        st.write("Click the button below to generate a motivational or inspirational quote.")

        if st.button("Generate Random Quote"):
            if not self.senten_snap:
                st.error("Please enter your Gemini API key in the sidebar.")
            else:
                st.session_state["definition_expanded"] = False
                self.quote_result = self.fetch_random_quote()

        # Display the generated quote if available
        if self.quote_result:
            st.subheader("Random Quote")
            st.write(f"{self.quote_result.get('Quote', 'No quote available.')}")
            author = self.quote_result.get("Author", "Unknown")
            source_type = self.quote_result.get("Source Type", "Unknown Source Type")
            context = self.quote_result.get("Context", "")

            st.write(f"— {author}")
            st.write(f"Source Type: {source_type}")
            st.write(f"Context: {context}")

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
