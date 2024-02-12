import pandas as pd
import re
from urllib.parse import urlparse
import spacy
import nltk

data = pd.read_csv("Posts.csv")
print(data.shape)

data.shape

data.drop_duplicates(subset=['Title', 'Post URL', 'Total Comments', 'ID'], inplace = True)
data.shape

data.drop("Unnamed: 0", axis = 1, inplace = True)
data.head()

data.isna().sum()

data.shape

"""# Website Domain Name"""

# Function to extract the domain from the URL
def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        # print(parsed_url)
        domain = parsed_url.netloc
        # print(domain)
        if domain.startswith('www.'):
            domain = domain[4:]  # Remove 'www.' if present
        if domain.endswith(".com"):
            domain = domain[:-4]
        # print(domain)
        return domain
    except Exception as e:
        print(f"Error extracting domain: {e}")
        return None

# Create a new column 'domain_url' with the extracted domains
data['Domain URL'] = data['Post URL'].apply(extract_domain)

# Now, you have a DataFrame with a new 'domain_url' column containing "theverge.com"
print(data.head())

"""# Title: Keywords and Topics"""

# Initialize NLTK stopwords and spaCy NLP model
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))
nlp = spacy.load('en_core_web_sm')

def extract_keywords_and_topics(title):
    # Tokenize and process the title with spaCy
    doc = nlp(title)

    # Extract keywords (non-stop words and non-punctuation)
    keywords = [token.text.lower() for token in doc if token.text.lower() not in stop_words and not token.is_punct]

    # Extract topics (noun phrases)
    topics = [chunk.text for chunk in doc.noun_chunks]

    return {
        'Keywords': ', '.join(keywords),
        'Topics': ', '.join(topics)
    }

# Apply the function to each title in the DataFrame
data[['Keywords', 'Topics']] = data['Title'].apply(extract_keywords_and_topics).apply(pd.Series)

data.head()

data.to_csv("Preprocessed.csv", index = False)
