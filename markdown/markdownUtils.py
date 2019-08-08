import sys
from lxml import etree

def textToList(text):
    texts = [ "* " + line.strip()  for line in text.split("\n")]
    text = "    \n".join(texts)
    print( text )
    #return text

def ulHtmlToList(text):
    html = etree.HTML(text)
    text = "    \n".join(["* " + text.strip() for text in html.xpath("//li//text()")] )
    print(text)




if __name__ == '__main__':
    pass
    #argv = sys.argv
    #eval(argv[0])(*argv[1:])
