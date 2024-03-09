import os
from jinja2 import Environment, FileSystemLoader
import re

def create_html_page(log_file):
    # Check if the log file exists
    if not os.path.exists(log_file):
        print(f"File not found: {log_file}")
        return

    # Extract the base name (without extension) from the log file
    base_name = os.path.splitext(os.path.basename(log_file))[0]

    # Read the content of the log file
    with open(log_file, 'r') as file:
        log_content = file.read()

    # Split the log content into individual entries
    entries = extract_entries(log_content)

    for idx, entry in enumerate(entries, start=1):
        # Validate if any attribute is missing
        if not all(attr in entry for attr in ['title', 'published', 'description', 'link']):
            print(f"Skipping entry {idx} in file {log_file}: Missing attributes.")
            continue

        # Create HTML page using Jinja2 template
        template_env = Environment(loader=FileSystemLoader(os.path.abspath('.')))
        template = template_env.get_template('template.html')

        # Render the template with entry attributes
        html_content = template.render(
            title=entry['title'],
            published=entry['published'],
            description=entry['description'],
            link=entry['link'],
            link_to_other=[f'{base_name}.html']
        )

        # Save the HTML page
        output_directory = os.path.join('output', 'docs')
        os.makedirs(output_directory, exist_ok=True)
        output_file = os.path.join(output_directory, f'{base_name}.html')
        with open(output_file, 'a+') as output:
            output.write(html_content)

        print(f"HTML page created: {output_file}")

    # Create an index page
    create_index_page(base_name, entries)

def extract_entries(content):
    pattern = re.compile(r'title:\s*\[(.*?)\],\s*published:\s*\[(.*?)\],\s*description:\s*\[(.*?)\],\s*link:\s*\[(.*?)\]')
    matches = pattern.findall(content)
    
    entries = []
    for match in matches:
        entries.append({
            'title': match[0],
            'published': match[1],
            'description': match[2],
            'link': match[3]
        })

    return entries

def create_index_page(base_name, entries):
    # Create HTML page using Jinja2 template for index
    template_env = Environment(loader=FileSystemLoader(os.path.abspath('.')))
    template = template_env.get_template('template.html')

    # Render the template with entries and base_name
    html_content = template.render(
        base_name=base_name,
        entries=entries
    )

    # Save the HTML index page
    output_file = os.path.join('docs', f'{base_name}_index.html')
    with open(output_file, 'w') as output:
        output.write(html_content)

    print(f"HTML index page created: {output_file}")

if __name__ == "__main__":
    # Search for log files with the ".log" extension in the 'docs' directory
    log_files = [file for file in os.listdir('docs') if file.endswith('.log')]

    # Loop through each log file
    for log_file in log_files:
        create_html_page(os.path.join('docs', log_file))
