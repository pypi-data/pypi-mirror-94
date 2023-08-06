#!/data/data/com.termux/files/usr/bin/python
import json
import re
import argparse
import json
import sys
import PyInquirer

import logging
import importlib
import glob
import os

from shutil import get_terminal_size
from urllib.parse import urlparse

basedir = os.path.join(os.path.dirname(__file__), "extractors")
for file in glob.glob(f"{basedir}/*.py"):
    filename = os.path.basename(file)
    if not filename.startswith("__"):
        importlib.import_module(f"lk21.extractors.{filename[:-3]}")
from .extractors import Base

logging.basicConfig(format="%(message)s", level=logging.INFO)

class lk21(Base):
    desc = "Film, Movie (default)"
    host = "http://149.56.24.226/"

    def extract(self, id: str):
        raw = self.session.post("http://dl.sharemydrive.xyz/verifying.php",
                                headers={
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                    "Accept": "*/*",
                                    "X-Requested-With": "XMLHttpRequest"
                                },
                                params={"slug": id},
                                data={"slug": id}
                                )
        soup = self.soup(raw)
        tb = soup.find("tbody")

        result = {}
        for tr in tb.findAll("tr"):
            title = tr.find("strong").text
            result[title] = {}
            for td in tr.findAll("td")[1:]:
                if (a := td.a):
                    result[title][a.attrs["class"][-1].split("-")[-1]] = a.attrs["href"]
        return result

    def search(self, title: str, page=1):
        if page > 1:
            return
        raw = self.session.get(self.host,
                               params={"s": title})

        soup = self.soup(raw)
        for item in soup.findAll(class_="search-item"):
            try:
                a = item.a
                extra = {"genre": [], "star": [], "country": [],
                         "size": [""], "quality": [""], "year": [""]}
                for tag in item.find(class_="cat-links").findAll("a"):
                    name, it = re.findall(r"/([^/]+)/([^/]+)", str(tag))[0]
                    extra[name].insert(0, it)

                for p in filter(lambda x: x.strong is not None, item.findAll("p")):
                    np, vl = re.findall(r"^([^:]+):\s+(.+)", p.text.strip())[0]
                    np = "star" if np == "Bintang" else "director" if np == "Sutradara" else np
                    extra[np] = re.split(r"\s*,\s*", vl) if "," in vl else vl

                extra["id"] = re.search(
                    r"\w/([^/]+)", a.attrs["href"]).group(1)
                result = {
                    "title": (item.find("h2").text or a.img.attrs["alt"]).strip(),
                }
                result.update(extra)
                yield result

            except Exception as e:
                logging.info("missing: %s" % e)


def parse_range(raw):
    r = re.findall(r"([^>]*)\s*:\s*([^>]*)", raw)
    if not r or re.search(r"^\s*:\s*$", raw):
        if raw.isdigit():
            yield int(raw)
        else:
            yield from map(int, re.split(r"\s*,\s*", raw))
    else:
        start, end = [
            [int(x) for x in re.split(r"\s*,\s*", i) if x] for i in r[0]]
        if len(start) > 1:
            yield from start[:-1]
        else:
            start = [1]
        if end:
            start, end = start[-1], end[0] + 1
            assert start < end
            yield from range(start, end)
        else:
            if re.search(r":\s*$", raw):
                n = start[-1]
                while True:
                    yield n
                    n += 1
        if isinstance(end, list):
            yield from end[1:]

def title(text, rtn=False):
    r = f" [\x1b[92m{text}\x1b[0m]"
    if rtn:
        return r
    logging.info(r)


def main():
    global extractor

    extractors = {
        obj.__name__: obj for obj in Base.__subclasses__() if obj
    }

    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=get_terminal_size().lines))
    parser.add_argument("query", metavar="query", nargs="*", help="kueri, judul")
    parser.add_argument("-p", metavar="page", dest="page",
                        help=("halaman situs, contoh penggunaan:\n"
                              "  - 1,2,3\n"
                              "  - 1:2, 2:8\n"
                              "  - 1,2,3:8\n"
                              "  - default halaman pertama\n"
                              "    dan seterusnya"), type=str, default="1:")
    parser.add_argument("-i", "--information", dest="info", action="store_true", help="cetak informasi dari item yang dipilih")
    parser.add_argument("-c", "--copy", metavar="command",
        help=("salin url ke papan klip\n"
              "contoh: termux-clipboard-set {}\n\n"
              "        wajib ada {} karena akan ditimpa\n"
              "        dengan url yang dipilih"))

    extractor_group = parser.add_argument_group("Daftar Situs",
       description=(
         f"pilih salah satu dari ke-{len(extractors)} situs berikut:"
       ))
    extractor = extractor_group.add_mutually_exclusive_group()
    for egn, kls in extractors.items():
        netloc = urlparse(kls.host).netloc
        extractor.add_argument(f"--{egn}", action="store_true",
                            help=f"{netloc}: {kls.desc}")
    args = parser.parse_args()

    if not args.query or (args.copy and "{}" not in args.copy):
        parser.print_help()
        sys.exit(0)

    extractor = extractors["lk21"]
    for egn, kls in extractors.items():
        if args.__dict__[egn]:
            extractor = kls
            break
    extractor = extractor()
    extractor.logging = logging
    query = " ".join(args.query)

    id = False
    nextPage = True
    Range = parse_range(args.page)
    netloc = urlparse(extractor.host).netloc
    try:
        page = Range.__next__()
        cache = {page: list(extractor.search(query, page=page))}
        while not id:
            logging.info(
                f"Mencari {query!r} -> {netloc}:{page}/{len(cache)}")
            logging.info(
                f"Total item saat ini: {sum(len(v) for v in cache.values())}")
            if not cache[page]:
                exit("Not Found")

            if len(cache[page]) == 1:
                response = f"1. " + cache[page][0]["title"]
            else:
                response = extractor.choice([f"{n}. {i['title']}" for n, i in enumerate(
                    cache[page], start=1)] + [PyInquirer.Separator(), "00. Back", "01. Next", "02. Exit"])
            pgs = list(cache.keys())
            index = pgs.index(page)
            if response.endswith("Exit"):
                break
            elif response.endswith("Back"):
                print("\x1b[3A\x1b[K", end="")
                if index > 0 and len(pgs) > 1:
                    page = pgs[index - 1]
            elif response.endswith("Next") and nextPage is True:
                if index >= len(pgs) - 1:
                    try:
                        page = Range.__next__()
                        if len(res := list(extractor.search(query, page=page))) > 0:
                            cache[page] = res
                    except StopIteration:
                        pass
                else:
                    page = pgs[index + 1]
                if nextPage:
                    print("\x1b[3A\x1b[K", end="")
            else:
                for r in cache[page]:
                    if r.get("title") == re.sub(r"^\d+\. ", "", response):
                        if args.info:
                            logging.info(f"\n [\x1b[92m{r.pop('title')}\x1b[0m]")
                            for k, v in r.items():
                                logging.info(f"   {k}: {', '.join(filter(lambda x: x, v)) if isinstance(v, list) else v}")
                            logging.info()

                        id = r["id"]
                        break
        if id:
            logging.info(f"Mengekstrak link unduhan: {id}")
            result = extractor.extract(id)
            while any(isinstance(v, dict) for v in result.values()):
                key = extractor.choice(result.keys())
                result = result[key]
            key1 = extractor.choice(result.keys())
            url = extractor.extract_direct_url(result[key1])

            if args.copy:
                logging.info(f"Menyetel papan klip: {url}")
                os.system(args.copy.format(url))
            else:
                logging.info("")
                title("Url Dipilih")
                logging.info(f"\n{url}\n")
        else:
            logging.info("\x1b[2C")

    except StopIteration:
        if not id:
            logging.info("\x1b[2C")

