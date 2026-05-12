import xml.etree.ElementTree as ET
import os


def increment_version(version):
    """
    Remove '-SNAPSHOT' and increment last numeric part.
    Examples:
      1.0.0-SNAPSHOT → 1.0.1
      1.2.3          → 1.2.4
      2.5            → 2.6
      3              → 4
    """

    # ✅ Remove SNAPSHOT
    version = version.replace("-SNAPSHOT", "").strip()

    parts = version.split(".")

    # ✅ Increment last numeric segment
    for i in range(len(parts) - 1, -1, -1):
        if parts[i].isdigit():
            parts[i] = str(int(parts[i]) + 1)
            break

    return ".".join(parts)


def update_pom(file_path="pom.xml"):
    if not os.path.exists(file_path):
        print("❌ pom.xml not found")
        return False

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # ✅ No namespace handling
        version_elem = root.find("version")

        # ✅ Check parent version if needed
        if version_elem is None:
            parent = root.find("parent")
            if parent is not None:
                version_elem = parent.find("version")

        if version_elem is None:
            print("⚠️ No <version> tag found")
            return False

        old_version = version_elem.text.strip()
        new_version = increment_version(old_version)

        if old_version == new_version:
            print("⚠️ No version change needed")
            return False

        print(f"✅ Updating version: {old_version} → {new_version}")

        version_elem.text = new_version

        tree.write(file_path, encoding="utf-8", xml_declaration=True)

        return True

    except Exception as e:
        print(f"❌ Error updating pom.xml: {e}")
        return False


if __name__ == "__main__":
    updated = update_pom()
    print("✅ Done" if updated else "⚠️ No update applied")
