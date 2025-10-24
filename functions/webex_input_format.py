
def format_check(command):
    """Check command format."""
    valid_commands = ["create", "delete", "enable", "disable", "status", "gigabit_status", "showrun"]
    
    if len(command) == 2:
        # Check if command[1] is an IP address (contains dots)
        if '.' in command[1] and all(part.isdigit() for part in command[1].split('.')):
            return "Error: Command not found."
        # Check if command[1] is a command
        elif command[1] in valid_commands:
            return "Error: No IP specified."
        else:
            return "Error: Invalid command format."
    elif len(command) == 3:
        # Check if command[1] is a command and command[2] is IP
        if command[1] in valid_commands and '.' in command[2]:
            return (command[2], command[1])  # Return tuple (ip, command)
        # Check if command[1] is IP and command[2] is a command (correct format)
        elif '.' in command[1] and command[2] in valid_commands:
            return (command[1], command[2])  # Return tuple (ip, command)
        else:
            return "Error: Invalid command format."
    else:
        return "Error: Invalid command format."
