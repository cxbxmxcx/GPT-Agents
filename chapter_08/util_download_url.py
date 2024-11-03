import requests

def download_html(url, output_filename):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the download failed

    # Save the HTML content to a file
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

# Example usage
url = 'https://www.gutenberg.org/cache/epub/10607/pg10607-images.html'  # Replace with the URL of the HTML page you want to download
output_filename = 'sample_documents/mother_goose.html'  # Replace with your desired output filename
download_html(url, output_filename)
