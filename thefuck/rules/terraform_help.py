#
# $ terraform destory
#
# Terraform has no command named "destory". Did you mean "destroy"?
#
# $ fuck
# terraform destroy [enter/↑/↓/ctrl+c]
#
import re
from thefuck.utils import for_app

REGEX = (
    r"Terraform has no command named \".+?\"\. "
    r"Did you mean \"(?P<suggestion>.+)\"\?"
)


@for_app("terraform")
def match(command) -> bool:
    return (
        "Terraform has no command named" in command.output
        and "Did you mean" in command.output
    )


def get_new_command(command) -> str | list[str]:
    matches = re.search(REGEX, command.output)
    if matches:
        return f"""terraform {matches.groupdict().get("suggestion", "")}"""
    else:
        return ""


enabled_by_default = True
