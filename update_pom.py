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


def split_header_and_body(content):
    """
    ✅ Extract header WITHOUT modifying it
    """
    match = re.match(r'(<\?xml[^>]+\?>\s*)(.*)', content, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return "", content


def get_namespace(tag):
    if tag.startswith("{"):
        return tag.split("}")[0] + "}"
    return ""


def find_project_version(root, ns):
    """
    ✅ STRICT:
    Only allow:
      - <project><version>
      - <project><parent><version>
    """

    # ✅ Direct project version ONLY
    for child in root:
        if child.tag == f"{ns}version":
            return child

    # ✅ Parent fallback ONLY
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
        # ✅ Step 1: Read full file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # ✅ Step 2: Split header and XML body
        header, body = split_header_and_body(content)

        # ✅ Step 3: Parse ONLY XML body
        root = ET.fromstring(body)

        ns = get_namespace(root.tag)

        version_elem = find_project_version(root, ns)

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

        # ✅ Update ONLY project version
        version_elem.text = new_version

        # ✅ Convert body back to XML
        updated_body = ET.tostring(root, encoding="unicode")

        # ✅ Step 4: Write back (header untouched)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(header)      # EXACT original header
            f.write(updated_body)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    update_pom()
