from urllib import parse
import requests

is_post_match = True


def match(command):
    return bool(command.output)


def get_new_command(command):
    return 'Try Stack Overflow'


def post_match(fc,output):
    num_of_result = 3;
    search_query = "{} {}".format(fc, output)
    sq_encoded = parse.quote_plus(search_query)
    url = "https://api.stackexchange.com/2.2/search/advanced?pagesize={}&order=desc&sort=votes&q={}&accepted=True&site=stackoverflow".format(num_of_result,sq_encoded)
    response = requests.get(url)
    display_list = []
    if response:
        response_json = response.json()
        for i in response_json["items"]:
            item = "{} \n".format(i["title"])
            display_list.append(item)
    # print("response_json",display_list)
    # print(response_json)
    # print("title", response_json["items"][0]["title"])

    # import pdb; pdb.set_trace(); # BREAKPOINT
    return display_list