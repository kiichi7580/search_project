import requests

def get_cover_image_url(isbn):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(api_url)
    print(f"status_code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"data: {data}")

        thumbnail_url = data.get("items", [{}])[0].get("volumeInfo", {}).get("imageLinks", {}).get("thumbnail", "No image available")

        print(thumbnail_url)
        if thumbnail_url:
            return thumbnail_url
        else:
            return None