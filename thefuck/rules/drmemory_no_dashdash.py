from thefuck.specific.sudo import sudo_support


@sudo_support
def match(command):
    return (
        "drmemory" in command.script
        and len(command.script.split()) >= 2
        and "Usage: drmemory [options] --" in command.output
    )


@sudo_support
def get_new_command(command):
    return(
        command.script.split()[0]
        + " -- "
        + " ".join(command.script.split()[1:])
    )
