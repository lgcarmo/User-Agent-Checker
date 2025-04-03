import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

init(autoreset=True)

def format_result(idx, code, lines, words, chars, payload):
    # Define cor com base no código
    if 200 <= code < 300:
        color = Fore.GREEN
    elif 300 <= code < 400:
        color = Fore.YELLOW
    elif code >= 400:
        color = Fore.RED
    else:
        color = Fore.WHITE

    return f"{idx:09d}:   {color}{code:<10}{Style.RESET_ALL} {lines:<7} {words:<9} {chars:<10} \"{payload.strip()}\""

def check_user_agent(idx, user_agent, url, custom_headers, proxy, filters):
    headers = {'User-Agent': user_agent.strip()}
    headers.update(custom_headers)
    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=5, proxies=proxies)
        code = response.status_code
        text = response.text
    except requests.RequestException:
        code = 0
        text = ""

    lines = len(text.splitlines())
    words = len(text.split())
    chars = len(text)

    # Excluir valores se estiverem nos filtros
    if code in filters['code']:
        return
    if lines in filters['lines']:
        return
    if words in filters['words']:
        return
    if chars in filters['chars']:
        return

    print(format_result(idx, code, lines, words, chars, user_agent))

def parse_custom_headers(header_list):
    headers = {}
    for header in header_list:
        if ':' in header:
            key, value = header.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def parse_exclusion_list(arg_list):
    if not arg_list:
        return set()
    result = set()
    for item in arg_list.split(","):
        item = item.strip()
        if item.isdigit():
            result.add(int(item))
    return result

def main():
    parser = argparse.ArgumentParser(description="User-Agent HTTP Status Checker (wfuzz-style with filters)")
    parser.add_argument("url", help="Target URL to test")
    parser.add_argument("list", help="File containing user-agent list")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads")
    parser.add_argument("--proxy", help="HTTP/HTTPS proxy (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--header", action="append", default=[], help="Custom headers (use multiple --header options if needed)")

    # Filtros de exclusão múltipla
    parser.add_argument("--code", help="Exclude specific status codes (e.g. 403,404)")
    parser.add_argument("--lines", help="Exclude responses with these line counts (e.g. 5,10)")
    parser.add_argument("--words", help="Exclude responses with these word counts (e.g. 100,200)")
    parser.add_argument("--chars", help="Exclude responses with these character counts (e.g. 50,75)")

    args = parser.parse_args()

    filters = {
        'code': parse_exclusion_list(args.code),
        'lines': parse_exclusion_list(args.lines),
        'words': parse_exclusion_list(args.words),
        'chars': parse_exclusion_list(args.chars),
    }

    custom_headers = parse_custom_headers(args.header)

    with open(args.list, "r") as f:
        user_agents = f.readlines()

    print("=" * 69)
    print("ID           Response   Lines    Word       Chars       Payload")
    print("=" * 69)

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for idx, user_agent in enumerate(user_agents, start=1):
            executor.submit(check_user_agent, idx, user_agent, args.url, custom_headers, args.proxy, filters)

if __name__ == "__main__":
    main()
