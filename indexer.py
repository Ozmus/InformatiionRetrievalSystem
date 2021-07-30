"""
http://gurmezin.com/python-ile-zemberek-kutuphanesini-kullanmak/
https://www.geeksforgeeks.org/create-inverted-index-for-file-using-python/
"""
import json
import jpype

#with open("webPages.json", "r", encoding="utf-8") as file:
    #webPages = json.load(file)

#Noktalama isaretlerinin atilmasi
#nok = '''!‡()|-–—[]{};:'"\, ’<>./?@#$%^&*_~'''
"""
for i in range(0, len(webPages)):
    for char in webPages[i]["body"]:
        if char in nok:
            webPages[i]["body"] = webPages[i]["body"].replace(char, " ")
"""
# JVM başlat C:\Users\Ahmet\PycharmProjects\InformationRetrievalSystem\zemberek-tr-2.1.jar\zemberek-tr-2.1.jar
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
#Çözümlenecek örnek kelimeleri belirle
#kelimeler = ["merhabalaştık","dalgalarının","habercisi","tırmalamışsa"]
kelimeler = ["iştahlı","iştahsız","süreğen","sergüzeşt"]
for kelime in kelimeler:
    if kelime.strip()>'':
        yanit = zemberek.kelimeCozumle(kelime)
        if yanit:
            print("{}".format(yanit[0]))
        else:
            print("{} ÇÖZÜMLENEMEDİ".format(kelime))
#JVM kapat
jpype.shutdownJVM()