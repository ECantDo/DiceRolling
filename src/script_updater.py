import requests
import sys
import os
import platform
import subprocess

GITHUB_API_RELEASES_URL = "https://api.github.com/repos/{owner}/{repo}/releases/latest"
GITHUB_OWNER = "ECantDo"
GITHUB_REPO = "DiceRolling"
CURRENT_VERSION = "1.5.0-SNAPSHOT-3"
EXECUTABLE_NAME = "roller_app.exe"


def parse_version(v):
    v = v.lstrip("v")
    return tuple(map(int, v.split(".")))


def is_newer_version(current, latest):
    return parse_version(latest) > parse_version(current)


def get_latest_release_info(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    r = requests.get(url)
    r.raise_for_status()
    data = r.json()
    return data["tag_name"], data["assets"]


def download_asset(asset_url, output_path):
    headers = {"Accept": "application/octet-stream"}
    with requests.get(asset_url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def replace_executable(current_path, new_path):
    if platform.system() == "Windows":
        backup_path = current_path + ".old"
        if os.path.exists(backup_path):
            os.remove(backup_path)
        os.rename(current_path, backup_path)
        os.rename(new_path, current_path)
    else:
        os.rename(new_path, current_path)


def restart_app(executable_path, args):
    print("Restarting app...")
    if platform.system() == "Windows":
        subprocess.Popen([executable_path] + args, shell=True)
    else:
        subprocess.Popen([executable_path] + args)
    sys.exit(0)


def check_for_update(current_version, owner, repo, executable_name):
    print(f"Checking for updates to {owner}/{repo}...")

    try:
        latest_version, assets = get_latest_release_info(owner, repo)
        print(f"Latest version on GitHub: {latest_version}")

        if is_newer_version(current_version, latest_version):
            print(f"Newer version available! Updating from {current_version} to {latest_version}.")

            asset = None
            for a in assets:
                if a["name"] == executable_name:
                    asset = a
                    break

            if asset is None:
                print(f"Error: Release asset named '{executable_name}' not found.")
                return False

            download_url = asset["url"]
            temp_file = executable_name + ".new"

            print(f"Downloading new executable: {executable_name} ...")
            download_asset(download_url, temp_file)

            current_exe_path = os.path.abspath(executable_name)

            print("Replacing old executable with new one...")
            replace_executable(current_exe_path, temp_file)

            print("Update complete!")

            # Restart app with same args (excluding first arg which is script path)
            restart_app(current_exe_path, sys.argv[1:])

            return True
        else:
            print("You are running the latest version.")
            return False

    except Exception as e:
        print("Update check failed:", e)
        return False


def run_update_checker():
    check_for_update(CURRENT_VERSION, GITHUB_OWNER, GITHUB_REPO, EXECUTABLE_NAME)
