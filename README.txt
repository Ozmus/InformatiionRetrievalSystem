install JPype1, BeautifulSoup, requests package

In pageRetrieval.py(line 16-17) and indexer.py(line 13-14) files update paths according to your jvm.dll file and zemberek-tum-2.0.jar file's location
jpype.startJVM("C:\\Program Files\\Java\\jdk-11.0.1\\bin\\server\\jvm.dll",
         "-Djava.class.path=C:\\Users\\Ahmet\\PycharmProjects\\InformationRetrievalSystem\\zemberek-tum-2.0.jar", "-ea")
         
start crawler.py. It may take long time to finish. It writes data to webPages.json file. Writing process occurs once cumulatively after 2500 pages.
start indexer.py. It may take minutes to finish. It writes inverted list to invertedList.json file.
start pageRetrieval.py. You can enjoy with program. 
