import os
import urllib.request
import roller_app


def download_if_missing(file_path: str, url: str):
    """
    Download the file from url only if file_path does not exist.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Downloading missing asset: {file_path}...")
        try:
            urllib.request.urlretrieve(url, file_path)
            print(f"Downloaded {file_path}")
        except Exception as e:
            print(f"Failed to download {file_path}: {e}")


def check_and_download_assets(base_folder: str):
    """
    Check a list of expected files, download those missing.
    Adjust file list and base URL to your setup.
    """
    # Base URL of your raw GitHub assets folder
    base_url = "https://raw.githubusercontent.com/ECantDo/DiceRolling/master/src/assets/"

    needed_files = [
        "d6/dice1.png",
        "d6/dice2.png",
        "d6/dice3.png",
        "d6/dice4.png",
        "d6/dice5.png",
        "d6/dice6.png",
        "diceTransparent.png"
        # Add any other files you want to check
    ]

    for relative_path in needed_files:
        local_path = os.path.join(base_folder, relative_path)
        file_url = base_url + relative_path.replace("\\", "/")
        download_if_missing(local_path, file_url)


# Usage example:
if __name__ == "__main__":
    assets_folder = roller_app.resource_path("assets")
    check_and_download_assets(assets_folder)
