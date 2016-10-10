from xml.etree import ElementTree
import re
import jieba
import jieba.posseg as pseg

jieba.load_userdict("dict.txt")

#读roo
read_root = ElementTree.parse(r"爬虫.xml")
persons = read_root.getiterator("person")

#写roo
write_root =ElementTree.Element("documents")

for person in persons:
    refers = set()
    xml_doc = ElementTree.SubElement(write_root, "doc")
    name = person.find("name").text
    name = re.sub(r'（.*）', '', str(name))
    dis = person.find("dis").text
    refers.add(name)
    #将去掉小括号的名字放到doc的name属性中
    xml_doc.set("name", name)
    #s删除作品名
    text = re.sub(r'《.*》', '', str(dis))
    words = pseg.cut(text)
    try:
        for w in words:
            if len(w.word) == 1:
                continue
            if str(w.flag) == "nr":
                refers.add(w.word)
    except:
        pass
    #去除本人的名字
    refers.remove(name)
    for refer in refers:
        xml_refer = ElementTree.SubElement(xml_doc, "refer")
        xml_refer.text = refer


tree = ElementTree.ElementTree(write_root)
f = open('命名实体识别.xml', 'wb')
tree.write(f)
f.close()



