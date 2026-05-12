import xml.etree.ElementTree as ET
import os
import re

# ✅ Prevent ns0 prefix
ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")


def increment_version(version):
    version = version.replace("-SNAPSHOT", "").strip()

    parts = version.split(".")
    parts = [int(p) if p.isdigit() else 0 for p in parts]

    while len(parts) < 3:
        parts.append(0)

    parts[-1] += 1  # ✅ patch increment

    return ".".join(map(str, parts))


def get_namespace(tag):
    if tag.startswith("{"):
        return tag.split("}")[0] + "}"
    return ""


def find_project_version(root, ns):
    """
    ✅ STRICT LOGIC:
    Only match:
      - <project><version>
      - <project><parent><version>

    ❌ DO NOT use .//version (prevents dependency/plugin update)
    """

    # ✅ Direct project version only
    for child in root:
        if child.tag == f"{ns}version":
            return child

    # ✅ Parent fallback only
    parent = root.find(f"{ns}parent")
    if parent is not None:
        for child in parent:
            if child.tag == f"{ns}version":
                return child

    return None


def extract_xml_header(file_path):
    """Preserve original XML header"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r'(<!\?xml[^>]+\?>)', content)
    return match.group(1) if match else ""


def update_pom(file_path="pom.xml"):
    if not os.path.exists(file_path):
        print("❌ pom.xml not found")
        return False

    try:
        # ✅ Preserve header
        xml_header = extract_xml_header(file_path)

        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = get_namespace(root.tag)

        # ✅ Get ONLY project version
        version_elem = find_project_version(root, ns)

        if version_elem is None or not version_elem.text:
            print("❌ No valid project <version> found")
            return False

        old_version = version_elem.text.strip()

        # ✅ Skip dynamic values
        if old_version.startswith("${"):
            print(f"⚠️ Skipping dynamic version: {old_version}")
            return False

        new_version = increment_version(old_version)

        if old_version == new_version:
            print("⚠️ No version change needed")
            return False

        print(f"✅ Updating version: {old_version} → {new_version}")

        # ✅ Update ONLY this node
        version_elem.text = new_version

        # ✅ Convert XML (preserve namespace)
        xml_body = ET.tostring(root, encoding="unicode")

        # ✅ Write back (preserve header)
        with open(file_path, "w", encoding="utf-8") as f:
            if xml_header:
                f.write(xml_header + "\n")
            f.write(xml_body)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    update_pom()
