"""
http://gurmezin.com/python-ile-zemberek-kutuphanesini-kullanmak/
https://www.geeksforgeeks.org/create-inverted-index-for-file-using-python/
"""
import json
import jpype

with open("webPages.json", "r", encoding="utf-8") as file:
    webPages = json.load(file)

# JVM başlat
# Aşağıdaki adresleri java sürümünüze ve jar dosyasının bulunduğu klasöre göre değiştirin
jpype.startJVM("C:\\Program Files\\Java\\jdk-11.0.1\\bin\\server\\jvm.dll",
         "-Djava.class.path=C:\\Users\\Ahmet\\PycharmProjects\\InformationRetrievalSystem\\zemberek-tum-2.0.jar", "-ea")
# Türkiye Türkçesine göre çözümlemek için gerekli sınıfı hazırla
Tr = jpype.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
# tr nesnesini oluştur
tr = Tr()
# Zemberek sınıfını yükle
Zemberek = jpype.JClass("net.zemberek.erisim.Zemberek")
# zemberek nesnesini oluştur
zemberek = Zemberek(tr)

#Noktalama isaretlerinin atilmasi
nok = '''!‡()|-–—[]{};:'"\, ’<>./?@#$%^&*_~'''

for i in range(0, len(webPages)):
    for char in webPages[i]["body"]:
        if char in nok:
            webPages[i]["body"] = webPages[i]["body"].replace(char, " ")

#Kok alma işlemi ve inverted list oluşturma
invertedIndex = {}
for i in range(0, len(webPages)):
    tokenizedWebPages = webPages[i]["body"].lower().split()
    for word in tokenizedWebPages:
        if word.strip() > '':
            yanit = zemberek.kelimeCozumle(word)
            if yanit:
                word = "{}".format(yanit[0]).split("Kok: ")[1].split()[0]

        if word not in invertedIndex:
            invertedIndex[word] = {}

        if word in invertedIndex:
            try:
                invertedIndex[word][i] += 1
            except:
                invertedIndex[word][i] = 1

print(len(invertedIndex))
a =0
for i in invertedIndex.keys():
    if(a < 10):
        a +=1
        print(invertedIndex[i])

with open("invertedList.json", "w", encoding="utf-8") as file:
    json.dump(invertedIndex, file, ensure_ascii=False, indent=4)

#JVM kapat
jpype.shutdownJVM()
