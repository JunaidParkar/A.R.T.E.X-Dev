import os
import shutil
import json
from rich import print
from bs4 import BeautifulSoup
from inquirer import confirm, text
from .z import zip_folder
from .c import get_choice, get_choices_with_checkboxes

class Packer:
    def __init__(self, cwd) -> None:
        self.__cwd = cwd
        self.__basic_config_cleared = True
        self.__available_libraries = []
        self.__html_lists = []
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Common")):
            for file in files:
                if os.path.join(root, file).endswith(".js"):
                    self.__available_libraries.append(file)

    def __check_basic_configurations(self):
        print("[green italic]checking config.json[/green italic]")
        if not os.path.isfile(os.path.join(self.__cwd, "config.json")):
            print("[red italic]Error: config.json is not available in your project. Kindly Re-Initialize the project carefully")
            self.__basic_config_cleared = False
            return
        
        print("[green italic]Checking icon.png.[/green italic]")
        if not os.path.isfile(os.path.join(self.__cwd, "icon.png")):
            self.__basic_config_cleared = False
            print("[red italic]Error: icon.png is not found in main directory.[red italic]")
            return
        
        print("[green italic]Checking entry point.[/green italic]")
        if not os.path.isfile(os.path.join(self.__cwd, "index.html")):
            self.__basic_config_cleared = False
            print("[red italic]Error: Entry point index.html is not found.")

        with open(os.path.join(self.__cwd, "config.json"), 'r') as j:
            cfg = json.load(j)
            j.close()
        
        print("[green italic]Checking included directory.[/green italic]")
        try:
            for f in cfg["includeDir"]:
                cl = True if os.path.isdir(os.path.join(self.__cwd, f)) else False
                if not cl:
                    print(f"[red italic]Error: {os.path.normpath(os.path.join(self.__cwd, f))} is unavailable or is invalid directory")
                    self.__basic_config_cleared = False
                    return
        except:
            self.__basic_config_cleared = False
            print("[red italic]Error: config.json is corrupted.")

        print("[green italic]Checking required libraries.[/green italic]")
        for l in cfg["requiredLibraries"]:
            if not l in self.__available_libraries:
                self.__basic_config_cleared = False
                print(f"[red italic]Error: Unknown library {l} is added in config.json")
                return
            
        print("[green italic]Checking app name.[/green italic]")
        if not cfg["name"]:
            self.__basic_config_cleared = False
            print("[red italic]Error: App name is not defined in config.json[/red italic]")
            return
        
        print("[green italic]Checking package name.[/green italic]")
        if not cfg["packageName"]:
            self.__basic_config_cleared = False
            print("[red italic]Error: App package name is not defined in config.json[/red italic]")
            return
        
        print("[green italic]Checking version.[/green italic]")
        if not cfg["version"]:
            self.__basic_config_cleared = False
            print("[red italic]Error: App version is not defined in config.json[/red italic]")
            return
        
        print("[green italic]Validating package name.[/green italic]")
        if cfg["packageName"] != f"artex.{cfg['name'].lower()}":
            self.__basic_config_cleared = False
            print(f"[red italic]Error: App package name should be artex.{cfg['name'].lower()}.[/red italic]")
            return
            
    def __list_htmls(self):
        print("[green italic]Looking for all the HTML files in project provided in config.json.[/green italic]")
        with open(os.path.join(self.__cwd, "config.json"), 'r') as j:
            cfg = json.load(j)
            j.close()
        
        self.__html_lists.append(os.path.join(self.__cwd, "index.html"))

        for p in cfg["includeDir"]:
            if p:
                for root, dirs, files in os.walk(os.path.join(self.__cwd, p)):
                    for file in files:
                        if file.endswith(".html"):
                            self.__html_lists.append(os.path.join(root, file))

    def __update_html_script_src(self):
        for file_path in self.__html_lists:
            try:
                print("[green italic]Searching for all the script src with default libraries.[/green italic]")
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')

                script_tags = soup.find_all('script')
                for script_tag in script_tags:
                    src = script_tag.get('src', '')
                    if any(src.endswith(service) for service in self.__available_libraries):
                        script_tag["src"] = os.path.normpath(os.path.join(os.path.relpath(self.__cwd, os.path.dirname(file_path)), f"../../Common/{src.split(os.path.dirname(src))[1]}"))

                print(f"[green italic]Updating the HTML at {os.path.normpath(file_path)}.[/green italic]")
                with open(file_path, 'w', encoding='utf-8') as m_file:
                    m_file.write(str(soup))
                print(f"[green italic]Updated script src in {os.path.normpath(file_path)}.[/green italic]")

            except Exception as e:
                print(f"[red italic]Error updating {os.path.normpath(file_path)}: {e}.[/red italic]")

    def __move_item(self, src, dest):
        # Check if the source path exists
        if not os.path.exists(src):
            print(f"[red italic]Error: The source path '{os.path.normpath(src)}' does not exist.[/red italic]")
        
        if os.path.isdir(src):
            # If the destination is not specified as a new directory, rename it
            if os.path.exists(dest):
                dest = os.path.join(dest, os.path.basename(src))
            print(f"[green italic]Moving {os.path.normpath(src)} to {os.path.normpath(dest)}")
            shutil.move(src, dest)
        else:
            # It's a file, move it directly
            if os.path.exists(dest) and os.path.isdir(dest):
                dest = os.path.join(dest, os.path.basename(src))
            shutil.move(src, dest)

        print(f"[green italic]Moved '{os.path.normpath(src)}' to '{os.path.normpath(dest)}' successfully.[/green italic]")

    def builder(self):
        self.__check_basic_configurations()
        if not self.__basic_config_cleared:
            return
        self.__list_htmls()
        self.__update_html_script_src()
        print("[green italic]Checking for assets folder.[/green italic]")
        if os.path.isfile(os.path.join(self.__cwd, "assets.zip")):
            os.remove(os.path.join(self.__cwd, "assets.zip"))
        if os.path.isdir(os.path.join(self.__cwd, "assets")):
            zip_folder(os.path.join(self.__cwd, "assets"), os.path.join(self.__cwd, "assets.zip"), password=b'ARTex101@5765buty6u$^&%Tguyhn675y75rt6rr53145ee67uhyi7786u875tyhy5325r')
            shutil.rmtree(os.path.join(self.__cwd, "assets"))

        if os.path.exists(os.path.join(self.__cwd, "temp")):
            shutil.rmtree(os.path.join(self.__cwd, "temp"))
            print(f"[green italic]All contents of '{os.path.join(self.__cwd, "temp")}' have been deleted.[/green italic]")
        if os.path.exists(os.path.join(self.__cwd, "dist")):
            shutil.rmtree(os.path.join(self.__cwd, "dist"))
            print(f"[green italic]All contents of '{os.path.join(self.__cwd, "dist")}' have been deleted.[/green italic]")
        
        print("[green italic]Creating dist directory.[/green italic]")
        os.mkdir(os.path.join(self.__cwd, "temp"))
        os.mkdir(os.path.join(self.__cwd, "dist"))

        print("[green italic]Reading projects.[/green italic]")
        with open(os.path.join(self.__cwd, "config.json"), 'r') as j:
            cfg = json.load(j)
            j.close()
        c = cfg["includeDir"]

        if cfg:
            for f in c:
                if f == "assets/" or f == "assets":
                    pass
                else:
                    self.__move_item(os.path.join(self.__cwd, f), os.path.join(self.__cwd, "temp"))
        self.__move_item(os.path.join(self.__cwd, "index.html"), os.path.join(self.__cwd, "temp", "index.html"))
        self.__move_item(os.path.join(self.__cwd, "config.json"), os.path.join(self.__cwd, "temp", "config.json"))
        self.__move_item(os.path.join(self.__cwd, "icon.png"), os.path.join(self.__cwd, "temp", "icon.png"))
        if os.path.isfile(os.path.join(self.__cwd, "assets.zip")):
            self.__move_item(os.path.join(self.__cwd, "assets.zip"), os.path.join(self.__cwd, "temp", "assets.zip"))
        zip_folder(os.path.join(self.__cwd, "temp"), os.path.join(self.__cwd, "dist", f'{cfg["packageName"]}.zip'), b"fn89wrehi38r38ryhd")