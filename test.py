import feedparser
import configparser
import datetime

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')
def get_cfg(sec, name, default=None):
    value=config.get(sec, name, fallback=default)
    if value:
        return value.strip('"')
# Function to collect entries for each XML URL and write to log file
def collect_entries(source_name, source_url, max_items, log_file):
    print(f"\nCollecting entries from {source_name}...")

    # Parse the feed
    feed = feedparser.parse(source_url)

    # Check if the feed was successfully parsed
    if feed.bozo == 0:
        entries = feed.entries[:int(max_items)]
        for entry in entries:
                print("\nTitle: " + entry.title)
                print("\nLink: " + entry.link)
                print("\des: " + entry.description)
                print("\nSummary: " + entry.summary)
                print("\nPublished Date: " + entry.published)
                print("\n" + "=" * 50)
    else:
        print(f"Error parsing feed '{source_name}': {feed.bozo_exception}")

# Log file name with timestamp
log_file = f"entries_log_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

# Iterate through sources in config.ini and collect entries
for section in config.sections():
    if section.startswith("source"):
       if get_cfg(section , 'name') =='Twitchy':
            source_name = get_cfg(section , 'name')
            source_url =get_cfg(section , 'url')
            max_items = get_cfg(section , 'max_items')
            collect_entries(source_name, source_url, max_items, log_file)

# print(f"\nEntries collected. Log file: {log_file}")
