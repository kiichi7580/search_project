import requests

def get_cover_image_url(isbn):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(api_url)
    print(f"status_code: {response.status_code}")

    if response.status_code == 200:
      data = response.json()
      print(f"data: {data}")

      if "item" in data:
        for item in data["items"]:
          volume_info = item.get("volumeInfo", {})
          identifiers = volume_info.get("industryIdentifiers", [])
          isbn_found = any(id["identifier"] == isbn for id in identifiers)

          if isbn_found:
            title = volume_info.get("title", "No Title")
            authors = volume_info.get("authors",  [])
            print(f"Title: {title}, Authors: {authors}")

            image_links = volume_info.get("imageLinks", {})
            return image_links.get("thumbnail", None)
    
    return None