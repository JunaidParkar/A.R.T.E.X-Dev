from bs4 import BeautifulSoup
import os
import json

class ArtexPacker:

    def __init__(self, config_path='config.json', service_dir=None) -> None:
        self.services = ["gsap.js", "chart.js", "anime.js", "CREngine.js", "cursor.js", "dkit.js"]
        self.all_files = []
        self.service_dir = service_dir or r"C:\Users\verix\Documents\xampp\htdocs\artex try\Common"
        self.service_paths = self._build_service_paths()

        with open(config_path, "r") as json_file:
            self.config = json.load(json_file)

    def _build_service_paths(self):
        """Build a dictionary of service files and their paths."""
        service_paths = {}
        for root, dirs, files in os.walk(self.service_dir):
            for service in self.services:
                if service in files:
                    service_paths[service] = os.path.join(root, service)
        return service_paths

    def list_all_files(self):
        """List all files in directories specified in the config."""
        for cf in self.config.get("includeDir", []):
            for root, dirs, files in os.walk(os.path.join(os.getcwd(), cf)):
                for file in files:
                    self.all_files.append(os.path.join(root, file))
        self.all_files.append(os.path.join(os.getcwd(), "index.html"))

    def get_html_files(self):
        """Process all HTML files."""
        for file in self.all_files:
            if file.endswith(".html"):
                self.update_html_script_src(file)

    def update_html_script_src(self, html_file):
        """Update the src attribute of script tags in the HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            script_tags = soup.find_all('script')
            for script_tag in script_tags:
                src = script_tag.get('src', '')
                if any(src.endswith(service) for service in self.services):
                    for service, og_path in self.service_paths.items():
                        if src.endswith(service):
                            path_to_replace = os.path.relpath(og_path, os.path.dirname(html_file))
                            script_tag['src'] = path_to_replace
                            break

            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            print(f"Updated script src in {html_file}")

        except Exception as e:
            print(f"Error updating {html_file}: {e}")

    def pack(self):
        """Run the packing process."""
        self.list_all_files()
        self.get_html_files()

# Example usage
a = ArtexPacker()
a.pack()
