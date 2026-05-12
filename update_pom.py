import xml.etree.ElementTree as ET

def increment_version(version):
    snapshot = False

    parts = version.split(".")

    for i in range(len(parts) - 1, -1, -1):
        if parts[i].isdigit():
            parts[i] = str(int(parts[i]) + 1)
            break

    new_version = ".".join(parts)

    if snapshot:
        new_version += "-SNAPSHOT"

    return new_version


def update_pom(file_path="pom.xml"):
    tree = ET.parse(file_path)
    root = tree.getroot()

    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    version_elem = root.find(f"{ns}version")

    if version_elem is None:
        parent = root.find(f"{ns}parent")
        if parent is not None:
            version_elem = parent.find(f"{ns}version")

    if version_elem is None:
        print("No version found")
        return False

    old_version = version_elem.text.strip()
    new_version = increment_version(old_version)

    if old_version == new_version:
        return False

    print(f"{old_version} → {new_version}")
    version_elem.text = new_version

    tree.write(file_path, encoding="utf-8", xml_declaration=True)

    return True


if __name__ == "__main__":
    try:
        changed = update_pom()
        print("Updated" if changed else "No change")
    except Exception as e:
        print(f"Error: {e}")
