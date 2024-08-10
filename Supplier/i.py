import os, shutil, json
from rich import print
from inquirer import text
from .c import get_choices_with_checkboxes

class Initiator:
    def __init__(self, cwd) -> None:
        self.__cwd = cwd

    def __copy(self, f, t):
        try:
            shutil.copy(src=f, dst=t)
            print(f"[green italic]Building libraries at {os.path.normpath(t)}[/green italic]")
            return True
        except Exception as er:
            print("[red italic]Error: An error occured while building libraries[/red italic]")
            return False
        
    def initialize(self):
        app_name = text(message="Enter the name for your application")
        if os.path.isdir(os.path.join(self.__cwd, app_name)):
            print(f"[red italic]Error: A directory named {app_name} already exist.[/red italic]")
            return
        os.mkdir(os.path.join(self.__cwd, app_name))
        self.__cwd = os.path.join(self.__cwd, app_name)
        app_version = text(message="Enter version for your app")
        app_libraries = get_choices_with_checkboxes("Choose the library you want to integrate", ["cursor.js", "dkit.js", "CREngine.js", "anime.js", "chart.js", "gsap.js"])
        app_publisher = text(message="Enter publisher name")
        data = {
            "name": app_name,
            "version": app_version,
            "packageName": f"artex.{app_name}",
            "requiredLibraries": app_libraries,
            "publisher": app_publisher,
            "includeDir": []
        }
        with open(os.path.join(self.__cwd, "config.json"), 'w') as file:
            json.dump(data, file, indent=4)
        print("[green italic]Creating a folder library[/green italic]")
        os.mkdir(os.path.join(self.__cwd, "library"))
        lib_path = []
        for lib in app_libraries:
            for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Common")):
                for file in files:
                    if os.path.join(root, file).endswith(lib):
                        lib_path.append(os.path.join(root, file))
        for file in lib_path:
            self.__copy(f=file, t=os.path.join(self.__cwd, "library"))
        print("[green italic]Creating an assets folder.[/green italic]")
        os.mkdir(os.path.join(self.__cwd, "assets"))
        print("[green italic]Creating an src folder.[/green italic]")
        os.mkdir(os.path.join(self.__cwd, "src"))
        print("[green italic]Creating index.html.[/green italic]")
        html_data = f"""<!DOCTYPE html>\n<html lang="en">\n\n<head>\n\t<meta charset="UTF-8">\n\t<meta name="viewport" content="width=device-width, initial-scale=1.0">\n\t<title>{app_name}</title>\n</head>\n\n<body>\n\n"""
        for libr in app_libraries:
            html_data += f"\n<script src='library/{libr}' ></script>"
        html_data += """\n</body>\n\n</html>"""
        with open(os.path.join(self.__cwd, "index.html"), "w") as h:
            h.write(html_data)
        print("[green italic]Your project have been initialized. If you want to add any library later then you can use command `artex addLibrary` in your current working directory.[/green italic]")
        print("[yellow italic]Note: config.json must not be deleted.[/yellow italic]")
        print("[yellow italic]Note: index.html in root directory is your entry point.[/yellow italic]")
        print("[yellow italic]Note: All of the files you create manually like html, css or js everything should be done inside 'src' folder.[/yellow italic]")
        print("[yellow italic]Note: If you create any other folder manually in the root directory then you need to add name of that folder while build process when it will be asked.[/yellow italic]")
        print("[yellow italic]Note: All the assets of your application must be inside assets folder excluding your app icon.[/yellow italic]")
        print("[yellow italic]Note: Apps icon name should be icon.jpg.[/yellow italic]")
        print("[yellow italic]Note: Apps icon should be in root directory of project.[/yellow italic]")

    def addLibrary(self):
        pass