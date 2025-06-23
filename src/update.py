from network import say
import subprocess

say("Es ist ein Update verfügbar:")
print("Eine neue Version wird installiert")

def get_latest_commit_message(branch="main"):
    try:
        subprocess.run(["git", "checkout", branch], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result = subprocess.run(
            ["git", "log", "-1", "--pretty=%B"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Fehler beim Abrufen der Commit-Message: {e}"
    
commit_message = get_latest_commit_message("main")
print(f"Letzte Commit-Message: {commit_message}")
say(f"Commit-nachricht: {commit_message}. Das update wurde installiert")