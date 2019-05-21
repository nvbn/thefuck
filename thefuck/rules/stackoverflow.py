from urllib import parse
import requests
import sys
import colorama
from thefuck.conf import settings

is_post_match = True
priority = 9500



def match(command):
    return bool(command.output)


def get_new_command(command):
    return 'Try Stack Overflow'


def post_match(fc,output):
    num_of_result = 3;
    # make sure the output is not too long
    output = output[0:100]
    search_query = "{} {}".format(fc, output)
    sq_encoded = parse.quote_plus(search_query)
    url = "https://api.stackexchange.com/2.2/search/advanced?pagesize={}&order=desc&sort=votes&q={}&accepted=True&site=stackoverflow".format(num_of_result,sq_encoded)
    response = requests.get(url)
    display_list = []
    if response:
        response_json = response.json()
        for i in response_json["items"]:
            display_list.append({"title":i["title"], "link":i["link"], "tags":i["tags"]})
    stackoverflow(display_list)

    # import pdb; pdb.set_trace(); # BREAKPOINT
    return True


def stackoverflow(display_list):
    if not display_list:
        sys.stdout.write(u"{col}No fuck is found.{reset} \n".format(col=color(colorama.Fore.RED), reset=color(colorama.Style.RESET_ALL)))
    for i, msg in enumerate(display_list):
        sys.stdout.write(
            u'{title_col}{i}. Post Title:{title} \n'
            u'Post Tags: {tags} \n'
            u'{url_col}URL: {url}\n\n'
            .format(
                title_col=color(colorama.Fore.GREEN),
                url_col=color(colorama.Fore.RED),
                title=msg["title"],
                tags=msg["tags"],
                url=msg["link"],
                i=i+1,
                reset=color(colorama.Style.RESET_ALL)
        ))



def color(color_):
    """Utility for ability to disabling colored output."""
    if settings.no_colors:
        return ''
    else:
        return color_
