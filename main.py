from googlesearch import search
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from rich import print


def save_pdf(content: bytes, filename: str, path: str) -> None:
    with open(f"{path}{filename}", "wb") as f:
        f.write(content)

def get_links(query: str, results: int = 10, delay: int = 2) -> list[str]:
    dork = f"{query} filetype: pdf"
    return [
        l for l in search(dork, tld="co.in", num=results, stop=results, pause=delay)
    ]

def get_bytes(links: list[str]) -> list[bytes]:
    contents = []
    for link in links:
        try:
            r = requests.get(link, timeout=1)
            contype = r.headers["content-type"]
            print(f"{link} {contype}")
            if "pdf" in contype:
                contents.append(r.content)
        except:
            pass
    return contents


def get_info(contents: list[bytes]) -> list[dict]:
    infos = []
    for content in contents:
        try:
            stream = BytesIO(content)
            reader = PdfReader(stream)
            meta = {
                "title": reader.metadata.title or "Unknown",
                "author": reader.metadata.author or "Unknown",
                "pages": len(reader.pages),
            }
            infos.append(meta)
        except:
            with Exception as e:
                print(e)
    return infos


def main():
    book = input("Book name: ")
    links = get_links(query=book, results=10)
    bites = get_bytes(links)
    infos = get_info(bites)
    for index, info in enumerate(infos):
        print(f"{index}.")
        for k, v in info.items():
            print(f"{k}: {v}")
        print("\n")

    choose = int(input("Choose a pdf: "))
    content = bites[choose]
    choosed_name = infos[choose]["title"]
    save_pdf(content, f"{choosed_name}.pdf", "./")


main()