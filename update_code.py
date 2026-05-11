import os
import re

# Example: replace OLD_URL with NEW_URL
PATTERN = r"OLD_URL"
REPLACEMENT = "NEW_URL"

def update_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(PATTERN, REPLACEMENT, content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True

    except Exception:
        pass

    return False


def process_repo(repo_path):
    changes_made = False

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith((".py", ".java", ".js", ".xml", ".yml", ".yaml", ".properties")):
                file_path = os.path.join(root, file)
                if update_file(file_path):
                    changes_made = True

    return changes_made


if __name__ == "__main__":
    repo_dir = os.getcwd()
    updated = process_repo(repo_dir)

    if updated:
        print("CHANGES_MADE")
    else:
        print("NO_CHANGES")