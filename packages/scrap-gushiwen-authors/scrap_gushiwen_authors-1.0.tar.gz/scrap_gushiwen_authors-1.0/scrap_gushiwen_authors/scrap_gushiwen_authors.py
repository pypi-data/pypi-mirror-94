import requests, bs4


def get_author(poem):
    url = "https://so.gushiwen.org/authors/"
    aaa = requests.get(url)
    aaa = bs4.BeautifulSoup(aaa.content, features="html.parser")
    ps = aaa.find_all(name="div", attrs={"class": "cont"})
    author = ""

    for i in ps:
        if poem in i.text:
            author = i.find("p").text.strip()

    if author != "":
        return author
    else:
        raise Exception("Poem does not exist.")


p = input()
a = get_author(p)
print(a)
