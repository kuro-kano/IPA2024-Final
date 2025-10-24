"""Module to format and validate Webex command inputs."""


def format_check(command):
    """Check command format for non-MOTD commands."""
    valid_commands = (
        "create",
        "delete",
        "enable",
        "disable",
        "status",
        "gigabit_status",
        "showrun",
        "motd",
    )

    if len(command) == 2:
        # Case: only "/<id> <something>"
        if "." in command[1] and all(part.isdigit() for part in command[1].split(".")):
            return "Error: Command not found."
        elif command[1] in valid_commands:
            return "Error: No IP specified."
        else:
            return "Error: Invalid command format."

    elif len(command) == 3:
        # Case: "/<id> <cmd> <ip>" or "/<id> <ip> <cmd>"
        if command[1] in valid_commands and "." in command[2]:
            return (command[2], command[1])
        elif "." in command[1] and command[2] in valid_commands:
            return (command[1], command[2])
        else:
            return "Error: Invalid command format."

    # Longer inputs (like MOTD with text) are handled in ipa2024_final.py
    return "Error: Invalid command format."
