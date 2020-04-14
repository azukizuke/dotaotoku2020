import requests
import time

def get_url(url, timeout=300, retry_time=10):
    headers = {
        "User-Agent": ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0)"
                       "Gecko/20100101 Firefox/47.0"),
    }

    print("url request : ", end="")
    print(url)
    while True:
        try:
            r = requests.get(url, headers=headers,timeout=(timeout,timeout))
            return(r.json())
        except Exception as e:
            print("Unexpectedf error")
            print(e)
            time.sleep(retry_time)
            retry_time * retry_time

if __name__ == "__main__":
    pass
