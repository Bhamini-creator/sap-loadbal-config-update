import xml.etree.ElementTree as ET
import os


def increment_version(version):
    version = version.replace("-SNAPSHOT", "").strip()
    parts = version.split(".")

    for i in range(len(parts) - 1, -1, -1):
        if parts[i].isdigit():
            parts[i] = str(int(parts[i]) + 1)
            break

    return ".".join(parts)


def strip_namespace(root):
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]


def update_pom(file_path="pom.xml"):
    if not os.path.exists(file_path):
        print("❌ pom.xml not found")
        return False

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # ✅ Remove namespace
        strip_namespace(root)

        version_elem = None

        # ✅ 1. PRIORITY: direct project version
        for child in list(root):
            if child.tag == "version":
                version_elem = child
                break

        # ✅ 2. FALLBACK: parent version (only if no project version)
        if version_elem is None:
            parent = root.find("parent")
            if parent is not None:
                for child in list(parent):
                    if child.tag == "version":
                        version_elem = child
                        break

        # ❌ DO NOT use .//version (this avoids dependencies/plugins)

        if version_elem is None:
            print("❌ No project <version> found")
            return False

        old_version = version_elem.text.strip()
        new_version = increment_version(old_version)

        if old_version == new_version:
            print("⚠️ No version change needed")
            return False

        print(f"✅ Updating project version: {old_version} → {new_version}")

        version_elem.text = new_version

        tree.write(file_path, encoding="UTF-8", xml_declaration=True)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    update_pom()
