import sys
from lxml import etree

def textToList(text):
    texts = [ "* " + line.strip()  for line in text.split("\n") if line.strip() != "" ]
    text = "    \n".join(texts)
    print( text )
    #return text

def textAddNum(text,addEmptyLine=False):
    texts = [ "{}、{}".format(str(i),line) + line.strip()  for i,line in enumerate( filter(lambda x: x.strip() != "",text.split("\n")) , start=1 ) ]
    text = "    \n".join(texts) if not addEmptyLine else "    \n\n".join(texts)
    print(text)

def ulHtmlToList(text):
    html = etree.HTML(text)
    text = "    \n".join(["* " + text.strip() for text in html.xpath("//li//text()")] )
    print(text)




if __name__ == '__main__':
    pass
    #argv = sys.argv
    #eval(argv[0])(*argv[1:])
