import jpype
import json
import math

"""
http://www.google.com/search?as_eq=wikipedia&q=%22Koronavir%C3%BCs%22&num=50&source=lnt&tbs=lr:lang_1tr&lr=lang_tr
"""

with open("webPages.json", "r", encoding="utf-8") as file:
    webPages = json.load(file)
with open("invertedList.json", "r", encoding="utf-8") as file:
    invertedList = json.load(file)

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

def findWebPages(query):
    #Remove punctuations
    nok = '''!‡()|-–—[]{};:'"\, ’<>./?@#$%^&*_~'''
    for char in query:
        if char in nok:
            query.replace(char, " ")

    #Tokenize Query
    tokenizedQuery = []
    for word in query.split():
        if word.strip() > '':
            yanit = zemberek.kelimeCozumle(word)
            if yanit:
                word = "{}".format(yanit[0]).split("Kok: ")[1].split()[0]
            tokenizedQuery.append(word.lower())

    #Calculate idf scores of query words
    idft = {}
    for word in tokenizedQuery:
        try:
            idft[word] = math.log10(len(webPages) / len(invertedList[word]))
        except:
            continue

    #Calculate page scores
    scores = {}
    for word in tokenizedQuery:
        try:
            for doc in invertedList[word].keys():
                try:
                    scores[doc] += (1 + math.log10(invertedList[word][doc])) * idft[word]
                except:
                    scores[doc] = (1 + math.log10(invertedList[word][doc])) * idft[word]
        except:
            continue

    #Sort Pages
    sortedScores = sorted(scores.items(), key=lambda x:x[1], reverse=True)
    """
       # BM25
       def totalTermsInDoc(docId):
           response = 0
           numOfTerms = 0
           for word in invertedList:
               try:
                   numOfTerms += 1
                   response += invertedList[word][docId]
               except:
                   continue
           return (response, (response / numOfTerms))


       BM25Scores = {}
       for word in tokenizedQuery:
           try:
               for doc in invertedList[word].keys():
                   try:
                       L = totalTermsInDoc(doc)
                       BM25Scores[doc] += (invertedList[word][doc] / (1.5 * L[0] / L[1] + invertedList[word][doc] + 0.5 )) * math.log10( (len(webPages) - len(invertedList[word]) + 0.5) / (len(invertedList[word]) + 0.5) )
                   except:
                       BM25Scores[doc] = (invertedList[word][doc] / (1.5 * L[0] / L[1] + invertedList[word][doc] + 0.5 )) * math.log10( (len(webPages) - len(invertedList[word]) + 0.5) / (len(invertedList[word]) + 0.5) )

           except:
               continue

       print("BM25 Scores:")
       print(BM25Scores)
       sortedBM25 = sorted(BM25Scores.items(), key=lambda x:x[1], reverse=True)

       with open("BM25.json", "w", encoding="utf-8") as file:
           json.dump(sortedBM25, file, ensure_ascii=False, indent=4)

       """

    return sortedScores

while True:
    choice = input("1. Sorgu girme\n2. Çıkış\n Seçiminiz: ")
    try:
        choiceInt = int(choice)
        if(choiceInt == 1):
            query = input("Bir sorgu giriniz: ")
            sortedScores = findWebPages(query)
            if(len(sortedScores) <= 0):
                sortedScores = findWebPages("Koronavirüs")
            for docID in sortedScores:
                print(webPages[int(docID[0])]["url"])
        elif(choiceInt == 2):
            print("İyi günler dileriz.")
            break;
        else:
            print("Geçersiz seçenek. 1 veya 2 yi seçiniz.")
    except:
        print("Geçersiz seçenek. 1 veya 2 yi seçiniz.")

# JVM kapat
jpype.shutdownJVM()
