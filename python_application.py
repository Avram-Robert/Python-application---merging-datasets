import csv
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Define the file paths for the existing three datasets
facebook_file = 'facebook_dataset.csv'
google_file = 'google_dataset.csv'
website_file = 'website_dataset.csv'
fourth_dataset_file = 'fourth_dataset.csv'  # Define the fourth dataset file

# Function to read data from CSV file
def read_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        data = list(csvreader)[1:]  # Skip the header row
    return data

# Read data from the existing three datasets
facebook_data = read_csv(facebook_file)
google_data = read_csv(google_file)
website_data = read_csv(website_file)

# Define the columns mapping
column_mapping = {
    0: {'facebook': 0, 'google': 14, 'website': 0},
    1: {'facebook': 1, 'google': 0},
    2: {'facebook': 9, 'google': 6, 'website': 3},
    3: {'facebook': 2, 'google': 1, 'website': 10},
    4: {'facebook': 6, 'google': 12, 'website': 9},
    5: {'facebook': 8, 'website': 8},
    6: {'facebook': [12, 11], 'google': 9, 'website': 7},
    7: {'facebook': 5, 'google': 4, 'website': 5},
    8: {'facebook': 3, 'google': 2, 'website': 4},
    9: {'facebook': 4, 'google': 3},
    10: {'facebook': 14, 'google': 11, 'website': 6},
    11: {'facebook': 13, 'google': 10},
    12: {'facebook': 15, 'google': 13},
    13: {'facebook': 7},
    14: {'facebook': 8},
    15: {'website': 2}
}

def preprocess_text(text):
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return ' '.join(words)

def calculate_similarity(text1, text2):
    if not text1 or not text2:
        return 0
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    return cosine_similarity(vectorizer[0:1], vectorizer[1:2])

priority_order = ['facebook', 'google', 'website']

def similar_categories(cat1, cat2):
    return calculate_similarity(cat1, cat2)

def resolve_categories_conflicts(categories):
    highest_priority_source = priority_order[0]
    for i in range(len(categories)):
        for j in range(i + 1, len(categories)):
            similarity = similar_categories(categories[i], categories[j])
            if similarity < 0.5:
                return categories[priority_order.index(highest_priority_source)]
    return categories[0]  # Return the first category when they are similar

def merge_datasets(facebook_data, google_data, website_data):
    final_dataset = []
    min_length = min(len(facebook_data), len(google_data), len(website_data))
    for i in range(min_length):
        new_row = []
        for column, sources in column_mapping.items():
            categories = []
            for source in priority_order:
                if source in sources:
                    if isinstance(sources[source], list):  # Handle the case where there are multiple columns for a source
                        for index in sources[source]:
                            if source == 'facebook' and index < len(facebook_data[i]):
                                categories.append(facebook_data[i][index])
                            elif source == 'google' and index < len(google_data[i]):
                                categories.append(google_data[i][index])
                            elif source == 'website' and index < len(website_data[i]):
                                categories.append(website_data[i][index])
                    else:
                        if source == 'facebook' and sources[source] < len(facebook_data[i]):
                            categories.append(facebook_data[i][sources[source]])
                        elif source == 'google' and sources[source] < len(google_data[i]):
                            categories.append(google_data[i][sources[source]])
                        elif source == 'website' and sources[source] < len(website_data[i]):
                            categories.append(website_data[i][sources[source]])
            if categories:  # Check if the list is not empty
                if column == 3:  # 'categories' column
                    new_row.append(resolve_categories_conflicts(categories))
                else:
                    new_row.append(categories[0])
            else:
                new_row.append(None)  # Append None or some default value if the list is empty
        final_dataset.append(new_row)
    return final_dataset

final_dataset = merge_datasets(facebook_data, google_data, website_data)

with open(fourth_dataset_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows([['domain', 'address', 'name', 'categories', 'description', 'link', 'phone', 'country', 'city', 'country_code', 'region', 'region_code', 'zip_code', 'email', 'page_type', 'language']])
    csvwriter.writerows(final_dataset)