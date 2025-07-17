import sys
import os
import msvcrt
import yaml
from core.instruction_reference import InstructionReference
from colorama import init, Fore, Style

init()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    print("\n[Press enter to return]", end="", flush=True)
    while True:
        char = msvcrt.getwch()
        if char == "\r":
            break


def get_input(prompt="> ", initial_key=None):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    chars = []
    if initial_key:
        chars.append(initial_key)
        sys.stdout.write(initial_key)
        sys.stdout.flush()
    while True:
        char = msvcrt.getwch()
        if char == "\r":
            break
        elif char == "\b":
            if chars:
                chars.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        else:
            chars.append(char)
            sys.stdout.write(char)
            sys.stdout.flush()
    return ''.join(chars)

def draw_boxed_header(mode, identity, width=40):
    cli_title = "ADLER CLI"
    identity_name = identity.replace(".yaml", "").upper()
    mode_name = mode.upper()
    profile = f"{identity_name}-{mode_name}"
    header_label = f"PROFILE: {profile}"
    
    padded_cli = cli_title.center(width)
    padded_profile = header_label.center(width)

    print("┌" + "─" * width + "┐")
    print("│" + padded_cli + "│")
    print("│" + Fore.CYAN + padded_profile + Style.RESET_ALL + "│")
    print("└" + "─" * width + "┘")

def print_menu():
    print()
    print(Fore.LIGHTBLACK_EX + " 1." + Style.RESET_ALL + " View Identity Rules")
    print(Fore.LIGHTBLACK_EX + " 2." + Style.RESET_ALL + " View Mode Rules")
    print(Fore.LIGHTBLACK_EX + " 3." + Style.RESET_ALL + " Switch Mode")
    print(Fore.LIGHTBLACK_EX + " 4." + Style.RESET_ALL + " Switch Identity")
    print(Fore.LIGHTBLACK_EX + " 5." + Style.RESET_ALL + " Rebuild Manifest")
    print(Fore.LIGHTBLACK_EX + " 6." + Style.RESET_ALL + " Exit")

def handle_choice(choice, mode, identity, manifest, ref):
    if choice == "1":
        clear_screen()
        identities = manifest.get("identities", {})
        identity_data = identities.get(identity, {})

        print(f"\n--- {identity} ---\n")
        if isinstance(identity_data, dict):
            print(yaml.dump(identity_data, sort_keys=False))
        else:
            print(identity_data)
        pause()
    elif choice == "2":
        clear_screen()
        draw_boxed_header(mode, identity)
        print()
        mode_file = mode + ".md"
        content = manifest.get("modes", {}).get(mode_file)
        if content:
            print(content)
        else:
            print(f"No rule file found for mode '{mode}'")
        pause()
    elif choice == "3":
        clear_screen()
        draw_boxed_header(mode, identity)
        print("\nUse ↑/↓ to navigate modes. Enter to select.\n")

        available_modes = [k.replace(".md", "") for k in manifest.get("modes", {}).keys()]
        if not available_modes:
            print("No available modes found.")
            pause()
            return mode, identity

        index = 0
        while True:
            # Inside while True loop:
            print("\033[H\033[J", end="")  # Flicker-free clear
            draw_boxed_header(mode, identity)
            print("\nSelect Mode:\n")
            for i, m in enumerate(available_modes):
                prefix = Fore.CYAN + ">" if i == index else " "
                suffix = Style.RESET_ALL + " <" if i == index else ""
                print(f"  {prefix} {m} {suffix}")
            print("\nUse ↑/↓ arrows, Enter to confirm.")

            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    index = (index - 1) % len(available_modes)
                elif key == b'P':
                    index = (index + 1) % len(available_modes)
            elif key == b'\r':
                return available_modes[index], identity

    elif choice == "4":
        clear_screen()
        draw_boxed_header(mode, identity)
        print("\nUse ↑/↓ to navigate identities. Enter to select.\n")

        available_identities = list(manifest.get("identities", {}).keys())
        if not available_identities:
            print("No identity files found.")
            pause()
            return mode, identity

        index = 0
        while True:
            # Inside while True loop:
            print("\033[H\033[J", end="")  # Flicker-free clear
            draw_boxed_header(mode, identity)
            print("\nSelect Identity:\n")
            for i, ident in enumerate(available_identities):
                name = ident.replace(".yaml", "")
                prefix = Fore.YELLOW + ">" if i == index else " "
                suffix = Style.RESET_ALL + " <" if i == index else ""
                print(f"  {prefix} {name} {suffix}")
            print("\nUse ↑/↓ arrows, Enter to confirm.")

            key = msvcrt.getch()
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    index = (index - 1) % len(available_identities)
                elif key == b'P':
                    index = (index + 1) % len(available_identities)
            elif key == b'\r':
                return mode, available_identities[index]

    elif choice == "5":
        clear_screen()
        draw_boxed_header(mode, identity)
        print("")
        manifest = ref.build_manifest(mode, identity)
        print("Instruction manifest rebuilt.")

        pause()
        return mode, identity, manifest
    elif choice == "6":
        clear_screen()
        print("Exited Adler CLI.")
        sys.exit()
    return mode, identity

def main():
    ref = InstructionReference()
    current_mode = "default"
    current_identity = "adler"
    manifest = ref.build_manifest(current_mode, current_identity)

    while True:
        clear_screen()
        draw_boxed_header(current_mode, current_identity)
        print_menu()
        choice = get_input("> ").strip()
        result = handle_choice(choice, current_mode, current_identity, manifest, ref)

        # Handle possible manifest rebuild (returns 3-tuple)
        if isinstance(result, tuple) and len(result) == 3:
            current_mode, current_identity, manifest = result
        elif isinstance(result, tuple):
            current_mode, current_identity = result

if __name__ == "__main__":
    main()
