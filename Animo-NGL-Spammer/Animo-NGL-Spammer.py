# Created by Animo?? | https://github.com/ANiMOOOOO
# Don't be a skid and give some credit if use, thx
# Thats about it ily qt have fun <3
import json, random, time, httpx, sys, os
from concurrent.futures import ThreadPoolExecutor
import threading
from msg import randomQuestions
from colorama import Fore, Style
from time import strftime, gmtime


sent, errored = 0, 0


class Console:
    @staticmethod
    def get_time() -> str:
        return time.strftime("%H:%M:%S", time.gmtime())

    @staticmethod
    def logger(*content: tuple, status: bool) -> None:
        lock = threading.Lock()
        time = Console.get_time()

        green = "[" + Fore.GREEN + Style.BRIGHT + "+" + Style.RESET_ALL + "] "
        red = "[" + Fore.RED + Style.BRIGHT + "-" + Style.RESET_ALL + "] "
        yellow = "[" + Fore.YELLOW + Style.BRIGHT + "!" + Style.RESET_ALL + "] "
        with lock:
            if status == "g":
                sys.stdout.write(
                    f'{Fore.YELLOW}[{time}]{Style.RESET_ALL}{green}{" ".join(content)}\n'
                )
            elif status == "r":
                sys.stdout.write(
                    f'{Fore.YELLOW}[{time}]{Style.RESET_ALL}{red}{" ".join(content)}\n'
                )
            elif status == "y":
                sys.stdout.write(
                    f'{Fore.YELLOW}[{time}]{Style.RESET_ALL}{yellow}{" ".join(content)}\n'
                )

    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")


def main(username, message, deviceid, proxy, proxystatus):
    global errored
    global sent

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
    }

    
    if proxystatus == True:
        client = httpx.Client(headers=headers, proxies=proxy)

    else:
        client = httpx.Client(headers=headers)

    try:
        
        postresp = client.post(
            f"https://ngl.link/api/submit",
            data={
                "username": username,
                "question": message,
                "deviceId": deviceid,
            }, 
        )
        if postresp.status_code == 200:
            sent += 1
            Console.logger(
                f"Sent {message} to victim, Sent {sent} messages, Errored {errored} messages",
                status="g",
            )

        elif postresp.status_code == 404:
            Console.logger(f"User {username} does not exist", status="r")
            exit()
        elif postresp.status_code == 429:
            Console.logger(f"User {username} is rate limited", status="r")
        else:
            Console.logger(postresp.status_code, status="r")

    except Exception as e:
        errored += 1
        Console.logger(f"Error: {e}", status="y")
        main(username, messages(), deviceid(), proxy())


def messages():
    return random.choice(randomQuestions)


def proxy():
    return "http://" + random.choice(list(open("proxy.txt")))


def deviceid():
    return "".join(
        random.choice("0123456789abcdefghijklmnopqrstuvwxyz-") for i in range(36)
    )


def handler():
    print("""
             █████╗ ███╗   ██╗██╗███╗   ███╗ ██████╗ ██████╗ ██████╗ 
            ██╔══██╗████╗  ██║██║████╗ ████║██╔═══██╗╚════██╗╚════██╗
            ███████║██╔██╗ ██║██║██╔████╔██║██║   ██║  ▄███╔╝  ▄███╔╝
            ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██║   ██║  ▀▀══╝   ▀▀══╝ 
            ██║  ██║██║ ╚████║██║██║ ╚═╝ ██║╚██████╔╝  ██╗     ██╗   
            ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝ ╚═════╝   ╚═╝     ╚═╝ 
    """
        
        + "\n $ Made by https://github.com/ANiMOOOOO"
        + "\n $ Star the repository on github if you like it!"
        + "\n $ If you would like to send random questions or use proxies just edit them in config.json to true."

        + Style.RESET_ALL
    )

    username = str(input("\n Animo?? ~ Username : "))
    threadcount = int(input("\n Animo?? ~ Amount: "))
    with open("config.json") as config:
        data = json.load(config)
        proxystatus = data["proxy"]
        messagestatus = data["random_messages"]
        delay = data["delay"]
    if messagestatus == True:
        with ThreadPoolExecutor(max_workers=threadcount) as executor:
            for x in range(threadcount):
                executor.submit(
                    main, username, messages(), deviceid(), proxy(), proxystatus
                )
    else:
        message = str(input("\n Animo?? ~ Message: "))
        with ThreadPoolExecutor(max_workers=threadcount) as executor:
            for x in range(threadcount):
                executor.submit(
                    main, username, message, deviceid(), proxy(), proxystatus
                )
                time.sleep(delay)

    Console.logger(f"Sent {sent} messages to {username}.", status="g")


if __name__ == "__main__":
    handler()
