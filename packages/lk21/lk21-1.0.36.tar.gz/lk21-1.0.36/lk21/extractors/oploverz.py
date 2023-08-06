from . import Base

class oploverz(Base):
    host = "https://www.oploverz.in"
    desc = "Anime, OnGoing"

    def extract(self, id, rextract=False):
        id = self.re.sub(r"^https?://[^/]+/", "", id)
        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if (ep_list := soup.find(class_="episodelist")):
            d = {}
            for li in ep_list.findAll("li"):
                a = li.find("a")
                d[a.text.strip()] = a.attrs["href"]
            key = self.choice(d.keys())
            return self.extract(d[key], rextract=True)

        elif not rextract and (all_eps := soup.find(class_="btn-full-eps")):
            ch = self.choice(["Lanjut", all_eps.text])
            if ch != "Lanjut":
                return self.extract(all_eps.attrs["href"])

        if (ddl := soup.find(class_="soraddl")):
            d = {}
            for p in ddl.findAll("p"):
                if (ttl := p.find(class_="sorattl")):
                    result = {}
                    for a in p.findAll("a"):
                        result[a.text] = a.attrs["href"]
                    d[ttl.text] = result
            return d

    def search(self, query, page=1):
        raw = self.session.get(f"{self.host}/page/{page}/",
           params={"q": query})
        soup = self.soup(raw)

        for dtl in soup.findAll("div", class_="dtl"):
            a = dtl.find("a")
            yield {
                "title": a.text,
                "id": self.re.sub(r"^https?://[^/]+/", "", a.attrs["href"]),
                "release": dtl.findAll("span")[1].text
            }
            break
