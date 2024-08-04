# filename: download_robot_books.py
import os
import requests
from bs4 import BeautifulSoup

# Function to get the download link for the plain text UTF-8 version of the book
def get_download_link(ebook_url):
    return ebook_url + '.txt.utf-8'

# Function to sanitize the title to create a valid filename
def sanitize_filename(title):
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

# Create a directory for robot books if it doesn't exist
os.makedirs('robot_books', exist_ok=True)

# URL of the Gutenberg search for books related to robots
search_url = 'https://www.gutenberg.org/ebooks/search/?query=robots'

# Perform the HTTP request to get the search results
response = requests.get(search_url)

# Parse the response content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the book entries
book_entries = soup.find_all('li', class_='booklink')

# Loop through all found book entries
for book_entry in book_entries:
    # Extract the book title and the relative link to the book's page
    title = book_entry.find('span', class_='title').text
    relative_link = book_entry.find('a').get('href')
    
    # Construct the full URL to the book's page
    book_url = f'https://www.gutenberg.org{relative_link}'
    
    # Get the download link for the plain text UTF-8 version of the book
    download_link = get_download_link(book_url)
    
    # Sanitize the title to create a valid filename
    filename = sanitize_filename(title) + '.txt'
    
    # Download the book and save it with the title as the filename
    book_response = requests.get(download_link)
    if book_response.status_code == 200:
        with open(os.path.join('gutenberg_robot_books', filename), 'wb') as book_file:
            book_file.write(book_response.content)
        print(f'Downloaded and saved: {filename}')
    else:
        print(f'Failed to download: {title}')