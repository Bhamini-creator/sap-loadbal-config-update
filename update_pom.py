import xml.etree.ElementTree as ET

def increment_version(version):
    """
    Increment version and REMOVE snapshot.
    Example:
      1.0.0-SNAPSHOT -> 1.0.1
      1.2.3          -> 1.2.4
    """

    parts = version.split(".")

    # ✅ Increment last numeric part
    for i in range(len(parts) - 1, -1, -1):
        if parts[i].isdigit():
            parts[i] = str(int(parts[i]) + 1)
            break

    return ".".join(parts)


def update_pom(file_path="pom.xml"):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # ✅ NO namespace handling
    version_elem = root.find("version")

    # ✅ Check parent version if not found
    if version_elem is None:
        parent = root.find("parent")
        if parent is not None:
            version_elem = parent.find("version")

    if version_elem is None:
        print("No <version> found → skipping")
        return False

    old_version = version_elem.text.strip()
    new_version = increment_version(old_version)

    if old_version == new_version:
        print("No change required")
        return False

    print(f"Updating version: {old_version} → {new_version}")

    version_elem.text = new_version

    tree.write(file_path, encoding="utf-8", xml_declaration=True)

    return True


if __name__ == "__main__":
    try:
        changed = update_pom()
        print("Updated" if changed else "No update")
    except Exception as e:
        print(f"Error: {e}")
