import os
import msvcrt
from rich import print as pr

def get_choice(choices):
    def print_choices(selected_index):
        for idx, choice in enumerate(choices):
            prefix = "> " if idx == selected_index else "  "
            print(f"{prefix}{choice}")

    selected_index = 0
    start_line = None

    while True:
        if start_line is None:
            start_line = os.get_terminal_size().lines - len(choices) - 1
        else:
            for _ in range(len(choices)):
                print("\033[F\033[K", end='')  # Move cursor up and clear the line
        
        print_choices(selected_index)
        
        key = msvcrt.getch()
        if key == b'\xe0':  # Arrow keys start with special character
            key = msvcrt.getch()
            if key == b'H':  # Up arrow
                if selected_index > 0:
                    selected_index -= 1
            elif key == b'P':  # Down arrow
                if selected_index < len(choices) - 1:
                    selected_index += 1
        elif key == b'\r':  # Enter key
            break

    for _ in range(len(choices)):
        print("\033[F\033[K", end='')  # Move cursor up and clear the line

    return choices[selected_index]

# def main():
    # choices = ["Option 1", "Option 2", "Option 3", "Option 4"]
    # selected_choice = get_choice(choices)
    # print(f"You selected: {selected_choice}")
    # choices = ["Option 1", "Option 2", "Option 3", "Option 4"]
    # selected_choice = get_choice(choices)
    # print(f"You selected: {selected_choice}")


def get_choices_with_checkboxes(msg, choices):
    selected_indices = set()

    pr(f"[[yellow]?[/yellow]] {msg}")
    
    def print_choices(selected_index):
        for idx, choice in enumerate(choices):
            prefix = "> " if idx == selected_index else "  "
            checkbox = "[X]" if idx in selected_indices else "[ ]"
            print(f"{prefix}{checkbox} {choice}")

    selected_index = 0
    start_line = None

    while True:
        if start_line is None:
            start_line = os.get_terminal_size().lines - len(choices) - 1
        else:
            for _ in range(len(choices)):
                print("\033[F\033[K", end='')  # Move cursor up and clear the line
        
        print_choices(selected_index)
        
        key = msvcrt.getch()
        if key == b'\xe0':  # Arrow keys start with special character
            key = msvcrt.getch()
            if key == b'H':  # Up arrow
                if selected_index > 0:
                    selected_index -= 1
            elif key == b'P':  # Down arrow
                if selected_index < len(choices) - 1:
                    selected_index += 1
        elif key == b' ':  # Spacebar to toggle selection
            if selected_index in selected_indices:
                selected_indices.remove(selected_index)
            else:
                selected_indices.add(selected_index)
        elif key == b'\r':  # Enter key
            break

    for _ in range(len(choices)):
        print("\033[F\033[K", end='')  # Move cursor up and clear the line
    if selected_indices:
        pr("    " + "\t".join([f"[yellow]{choices[idx]}[/yellow]" for idx in selected_indices]))
        return [choices[idx] for idx in selected_indices]
    else:
        print("    []")
        return []

# Example usage
# choices = ["Option 1", "Option 2", "Option 3", "Option 4"]
# selected = get_choices_with_checkboxes(choices)
# print(f"You selected: {selected}")