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

    parts[-1] += 1
    return ".".join(map(str, parts))


def split_xml_header(content):
    """
    ✅ Split XML header and body WITHOUT modifying it
    """
    match = re.match(r'(<!\?xml[^>]+\?>\s*)(.*)', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def get_namespace(tag):
    if tag.startswith("{"):
        return tag.split("}")[0] + "}"
    return ""


def find_project_version(root, ns):
    # ✅ Only direct <project><version>
    for child in root:
        if child.tag == f"{ns}version":
            return child

    # ✅ Fallback: <parent><version>
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
        # ✅ Read file as text
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # ✅ Split header and XML body
        xml_header, xml_body = split_xml_header(content)

        # ✅ Parse ONLY the body
        root = ET.fromstring(xml_body)

        ns = get_namespace(root.tag)

        version_elem = find_project_version(root, ns)

        if version_elem is None or not version_elem.text:
            print("❌ No valid project <version> found")
            return False

        old_version = version_elem.text.strip()

        if old_version.startswith("${"):
            print(f"⚠️ Skipping dynamic version: {old_version}")
            return False

        new_version = increment_version(old_version)

        if old_version == new_version:
            print("⚠️ No version change needed")
            return False

        print(f"✅ Updating version: {old_version} → {new_version}")

        version_elem.text = new_version

        # ✅ Convert back to XML string (ONLY body)
        updated_body = ET.tostring(root, encoding="unicode")

        # ✅ Write back WITHOUT touching header
        with open(file_path, "w", encoding="utf-8") as f:
            if xml_header:
                f.write(xml_header)  # unchanged
            f.write(updated_body)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    update_pom()
