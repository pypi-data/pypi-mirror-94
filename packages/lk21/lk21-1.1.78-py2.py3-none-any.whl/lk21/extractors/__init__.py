import requests
import bs4
import re
import PyInquirer
import sys
from urllib.parse import urlparse

class Base(object):
    def __init__(self):
        self.session = self._build_session()
        self.directRules = {
            "_fembed": re.compile(r"https://layarkacaxxi.icu/f/[^>]+"),
            "_zippyshare": re.compile(r"https://www\d+.zippyshare.com/v/[^/]+/file.html")
        }
        self.re = re
        self.logging = None
        self.counter = 0

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
                self.logging.info(f"Mengekstrak {title[1:]}: {url}")
                func = getattr(self, title)
                result = func(url)

                key = self.choice(result.keys())
                return result[key]
        return url

    def getPath(self, url):
        return urlparse(url).path.strip("/")

    def _reformat(self, raw):
        if not isinstance(raw, str) or re.match(r"^\d+\.", raw):
            return raw
        else:
            self.counter += 1
            raw = re.sub(r"^\s+|\s+$", "", raw)
            if self.directRules.get("_" + raw.lower()):
                raw += " (direct)"
            return f"{self.counter}) {raw}"

    def choice(self, choices, msg=None, reset_counter=True):
        if reset_counter:
            self.counter = 0
        choices = list(choices)
        if len(choices) == 0:
            sys.exit("pilihan kosong")

        if len(choices) == 1:
            return choices[0]

        nch = {
            self._reformat(v): v for v in choices}
        questions = [
            {
                "type": "list",
                "name": "js",
                "message": msg or "pilih:",
                "choices": list(nch.keys())
            }
        ]

        output = PyInquirer.prompt(questions)["js"]
        return re.sub(r" \(direct\)$", "", nch[output])

    """
    Extractor
    """

    def _zippyshare(self, url):
        raw = self.session.get(url)
        res = re.search(
            r'href = "(?P<i>[^"]+)" \+ \((?P<t>[^>]+?)\) \+ "(?P<f>[^"]+)', raw.text)
        if res is not None:
            res = res.groupdict()
            return {
                "": re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) +
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
