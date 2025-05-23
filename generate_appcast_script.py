import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import sys
import re

pattern = r'sparkle:edSignature="([^"]+)" length="([^"]+)"'

BUNDLE_VERSION = sys.argv[1]
BUNDLE_BUILD = sys.argv[2]
EDSA = sys.argv[3]

URL = f"https://github.com/SnipDaddy/mac-releases/releases/download/v{BUNDLE_VERSION}/PromptBox_v{BUNDLE_VERSION}.dmg"

match = re.search(pattern, EDSA)

if match:
    # Extract values
    ed_signature = match.group(1)
    length = match.group(2)

    # Print the extracted values
    print("edSignature:", ed_signature)
    print("length:", length)
else:
    print("No match found.")

# Get current time in UTC
utc_now = datetime.now(timezone.utc)
# Calculate Singapore time (UTC +8 hours)
sgt_now = utc_now + timedelta(hours=8)
# Format the time
pub_date = sgt_now.strftime('%a, %d %b %Y %H:%M:%S +0800')

# Define the new item content
ET.register_namespace('sparkle', 'http://www.andymatuschak.org/xml-namespaces/sparkle')
new_item_content = f'''
    <item xmlns:sparkle="http://www.andymatuschak.org/xml-namespaces/sparkle">
        <title>Version {BUNDLE_VERSION}</title>
        <pubDate>{pub_date}</pubDate>
        <sparkle:version>{BUNDLE_BUILD}</sparkle:version>
        <sparkle:shortVersionString>{BUNDLE_VERSION}</sparkle:shortVersionString>
        <sparkle:minimumSystemVersion>13.0</sparkle:minimumSystemVersion>
        <enclosure url="{URL}" length="{length}" type="application/octet-stream" sparkle:edSignature="{ed_signature}"/>
    </item>
'''

# Parse the existing XML file
tree = ET.parse('./appcast.xml')
root = tree.getroot()

# Find the last item in the channel
channel = root.find('.//channel')

# Append the new item after the last item
channel.insert(1, ET.fromstring(new_item_content))

# Write the modified XML back to the file with manual XML declaration
with open('./appcast.xml', 'wb') as f:
    f.write('<?xml version="1.0" standalone="yes"?>\n'.encode())
    f.write(ET.tostring(root, encoding='utf-8'))