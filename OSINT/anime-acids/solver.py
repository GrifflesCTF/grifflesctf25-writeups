import requests

page_links = ["https://myanimelist.net/manga.php?cat=0&q=&type=1&score=0&status=2&mid=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B0%5D=b&o=4&w=1&show=350",
              "https://myanimelist.net/manga.php?cat=0&q=&type=1&score=0&status=2&mid=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c%5B0%5D=b&o=4&w=1&show=400"]
anime_links = []

start_anime_identifier = """</div><a class="hoverinfo_trigger fw-b" href=\""""
end_anime_identifier = """\" id="""
volume_identifier = """</td><td class="borderClass ac bgColor"""

for page_link in page_links:
    page_html = requests.get(page_link).text

    while start_anime_identifier in page_html:
        i = page_html.index(start_anime_identifier)
        page_html = page_html[i + len(start_anime_identifier):]
        
        j = page_html.index(end_anime_identifier)
        anime_link = page_html[:j]
        
        k = page_html.index(volume_identifier)
        volume_count = int(page_html[k + len(volume_identifier) + 19:k + len(volume_identifier) + 21])

        if volume_count == 24:
            anime_links.append(anime_link + "/reviews?spoiler=on")

comment = "Sep 29, 2023"

review_count_identifier = "Filtered Results: <strong>"

for anime_link in anime_links:
    page_html = requests.get(anime_link).text

    i = page_html.index(review_count_identifier)
    page_html = page_html[i + len(review_count_identifier):]

    j = page_html.index('<')
    review_count = int(page_html[:j])

    page_count = 0
    while page_count * 20 < review_count:
        page_html = requests.get(anime_link + "&p=" + str(page_count + 1)).text
        if comment in page_html:
            print(anime_link + "&p=" + str(page_count + 1))
        page_count += 1