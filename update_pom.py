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


def get_namespace(root):
    """Extract namespace from root tag"""
    if root.tag.startswith("{"):
        return root.tag.split("}")[0] + "}"
    return ""


def get_project_version_element(root, ns):
    """
    ✅ Namespace-safe strict matching
    """

    # ✅ Direct project version
    for child in root:
        if child.tag == f"{ns}version":
            return child

    # ✅ Parent fallback
    parent = root.find(f"{ns}parent")
    if parent is not None:
        for child in parent:
            if child.tag == f"{ns}version":
                return child

    return None


def update_pom(file_path="pom.xml"):
    if not os.path.exists(file_path):
        print("❌ pom.xml not found")
        return False

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # ✅ KEEP namespace (do NOT strip)
        ns = get_namespace(root)

        version_elem = get_project_version_element(root, ns)

        if version_elem is None or not version_elem.text:
            print("❌ No valid project <version> found")
            return False

        old_version = version_elem.text.strip()

        # ✅ Skip property-based version
        if old_version.startswith("${"):
            print(f"⚠️ Skipping dynamic version: {old_version}")
            return False

        new_version = increment_version(old_version)

        if old_version == new_version:
            print("⚠️ No version change needed")
            return False

        print(f"✅ Updating version: {old_version} → {new_version}")

        version_elem.text = new_version

        # ✅ Write WITHOUT losing namespace
        tree.write(file_path, encoding="utf-8", xml_declaration=True)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    update_pom()
``
