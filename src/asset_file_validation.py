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
    needed_files = [
        "d4/dice1.png",
        "d4/dice2.png",
        "d4/dice3.png",
        "d4/dice4.png",
        "d6/dice1.png",
        "d6/dice2.png",
        "d6/dice3.png",
        "d6/dice4.png",
        "d6/dice5.png",
        "d6/dice6.png",
        "d8/dice1.png",
        "d8/dice2.png",
        "d8/dice3.png",
        "d8/dice4.png",
        "d8/dice5.png",
        "d8/dice6.png",
        "d8/dice7.png",
        "d8/dice8.png",
        "d10/dice1.png",
        "d10/dice2.png",
        "d10/dice3.png",
        "d10/dice4.png",
        "d10/dice5.png",
        "d10/dice6.png",
        "d10/dice7.png",
        "d10/dice8.png",
        "d10/dice9.png",
        "d10/dice10.png",
        "d12/dice1.png",
        "d12/dice2.png",
        "d12/dice3.png",
        "d12/dice4.png",
        "d12/dice5.png",
        "d12/dice6.png",
        "d12/dice7.png",
        "d12/dice8.png",
        "d12/dice9.png",
        "d10/dice10.png",
        "d12/dice11.png",
        "d12/dice12.png",
        "d20/dice1.png",
        "d20/dice2.png",
        "d20/dice3.png",
        "d20/dice4.png",
        "d20/dice5.png",
        "d20/dice6.png",
        "d20/dice7.png",
        "d20/dice8.png",
        "d20/dice9.png",
        "d20/dice10.png",
        "d20/dice11.png",
        "d20/dice12.png",
        "d20/dice13.png",
        "d20/dice14.png",
        "d20/dice15.png",
        "d20/dice16.png",
        "d20/dice17.png",
        "d20/dice18.png",
        "d20/dice19.png",
        "d20/dice20.png",
        "diceTransparent.png"
    ]
    base_url = "https://raw.githubusercontent.com/ECantDo/DiceRolling/master/src/assets/"
    print("Checking Assets...")
    for relative_path in needed_files:
        local_path = os.path.join(base_folder, relative_path)
        file_url = base_url + relative_path.replace("\\", "/")
        download_if_missing(local_path, file_url)


# Usage example:
if __name__ == "__main__":
    assets_folder = roller_app.resource_path("assets")
    check_and_download_assets(assets_folder)
