import requests
import bs4
import re
import PyInquirer

class Base(object):
    def __init__(self):
        self.session = self._build_session()
        self.directRules = {
            "_fembed": re.compile(r"https://layarkacaxxi.icu/f/[^>]+"),
            "_zippyshare": re.compile(r"https://www\d+.zippyshare.com/v/[^/]+/file.html")
        }
        self.re = re
        self.logging = None

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        session.headers[
            "User-Agent"] = "Mozilla/5.0 (Linux; Android 7.0; 5060 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
        return session

    def soup(self, raw):
        text = raw.text if hasattr(raw, "text") else raw
        return bs4.BeautifulSoup(text, "html.parser")

    def extract_direct_url(self, url):
        for title, pattern in self.directRules.items():
            if pattern.match(url):
                print(f"Mengekstrak {title[1:]}: {url}")
                func = getattr(self, title)
                result = func(url)
                key = self.choice(result.keys())
                return result[key]
        return url

    def choice(self, choices, msg=None):
        choices = list(choices)
        if len(choices) == 0:
            sys.exit("pilihan kosong")

        if len(choices) == 1:
            return choices[0]

        questions = [
            {
                "type": "list",
                "name": "js",
                "message": msg or "pilih:",
                "choices": [f"{k1} (direct)" if isinstance(k1, str) and self.directRules.get(f"_{k1.lower()}") else k1 for k1 in choices]
            }
        ]

        output = PyInquirer.prompt(questions)["js"]
        return re.sub(r" \(direct\)$", "", output)

    """
    Extractor
    """

    def _zippyshare(self, url):
        raw = self.session.get(url)
        res = re.search(r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', raw.text)
        if res is not None:
            res = res.groupdict()
            return {
              "": re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) + \
                  res["i"] + str(eval(res["t"])) + res["f"]}
        return {"": url}

    def _fembed(self, url):
        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = requests.head(f).headers.get("Location", f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result

