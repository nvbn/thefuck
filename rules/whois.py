# -*- encoding: utf-8 -*-
from six.moves.urllib.parse import urlparse
from thefuck.utils import for_app


@for_app('whois', at_least=1)
def match(command):
    """
    What the `whois` command returns depends on the 'Whois server' it contacted
    and is not consistent through different servers. But there can be only two
    types of errors I can think of with `whois`:
        - `whois https://en.wikipedia.org/` → `whois en.wikipedia.org`;
        - `whois en.wikipedia.org` → `whois wikipedia.org`.
    So we match any `whois` command and then:
        - if there is a slash: keep only the FQDN;
        - if there is no slash but there is a point: removes the left-most
          subdomain.

    We cannot either remove all subdomains because we cannot know which part is
    the subdomains and which is the domain, consider:
        - www.google.fr → subdomain: www, domain: 'google.fr';
        - google.co.uk → subdomain: None, domain; 'google.co.uk'.
    """
    return True


def get_new_command(command):
    url = command.script_parts[1]

    if '/' in command.script:
        return 'whois ' + urlparse(url).netloc
    elif '.' in command.script:
        path = urlparse(url).path.split('.')
        return ['whois ' + '.'.join(path[n:]) for n in range(1, len(path))]
