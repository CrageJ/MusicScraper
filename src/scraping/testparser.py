from bs4 import BeautifulSoup
import io
# Assuming the HTML content is stored in a variable called 'html_content'
html_content = open("out.html","r",encoding='utf-8')
soup = BeautifulSoup(html_content, 'html.parser')

# Find all album list rows
album_rows = soup.find_all('div', class_='albumListRow')

albums = []

for row in album_rows:
    album = {}

    # Extract rank
    rank = row.find('span', class_='albumListRank').text.strip().rstrip('.')
    album['rank'] = int(rank)

    # Extract title and artist
    title_element = row.find('h2', class_='albumListTitle')
    title_text = title_element.find('a').text.strip()
    artist, title = title_text.split(' - ', 1)
    album['artist'] = artist
    album['title'] = title

    # Extract release date
    date = row.find('div', class_='albumListDate').text.strip()
    album['release_date'] = date

    # Extract genres
    genres = row.find('div', class_='albumListGenre')
    if genres:
        album['genres'] = [a.text for a in genres.find_all('a')]

    # Extract user score
    score_container = row.find('div', class_='albumListScoreContainer')
    if score_container:
        score = score_container.find('div', class_='scoreValue').text.strip()
        album['user_score'] = int(score)

        ratings = score_container.find('div', class_='scoreText').text.strip()
        album['ratings'] = ratings

    albums.append(album)

# Print the parsed data
for album in albums:
    print(album)
