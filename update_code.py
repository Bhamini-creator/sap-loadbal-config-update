import os
import re

# Example: replace OLD_URL with NEW_URL
PATTERN = re.compile(
    r'<sap:sap-config\b[^>]*>.*?</sap:sap-config>',
    re.DOTALL | re.IGNORECASE
)

REPLACEMENT = """<sap:sap-config name="SAP_Config" doc:name="SAP Config" doc:id="fbdce40b-5788-40a9-872a-9ec3aa9aa247">
<sap:simple-connection-provider-connection
        username="RFCMULEGRP"
        password="Mulegrp@369"
        client="${zuul::sap.client}"
        systemNumber="${zuul::sap.sysno}">
 
        <sap:extended-properties>
<sap:extended-property key="jco.client.mshost" value="ecqhost.global.bdx.com"/>
<sap:extended-property key="jco.client.msserv" value="3600"/>
<sap:extended-property key="jco.client.group" value="MULESOFT"/>
 
            <!-- Optional JCo pool properties -->
<sap:extended-property key="jco.destination.pool_capacity" value="40"/>
<sap:extended-property key="jco.destination.peak_limit" value="40"/>
<sap:extended-property key="jco.destination.expiration_time" value="600000"/>
</sap:extended-properties>
 
        <sap:message-server
            host="ecqhost.global.bdx.com"
            systemId="ECQ"
            port="3600"
            group="MULESOFT"/>
</sap:simple-connection-provider-connection>
</sap:sap-config>
""".strip()

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
            if file.endswith((".xml")):
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
