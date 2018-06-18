import pprint

from googleapiclient.discovery import build
import getopt, sys

api_key = "AIzaSyD4ePQSrWHZCsVRfuf1goOPgzFB9gJbhMM"
cse_id = "017305337282449250408:jxmfygjffvs"

sqldorks = ('intext:"supplied argument is not a valid MySQL result resource" OR intext:"You have an error in your SQL syntax"',
            'intext:"Warning: mysql_connect(): Access denied for user: \'*@*" "on line"',
            'intext:"PostgreSQL query failed: ERROR: parser: parse error" OR intext:"supplied argument is not a valid PostgreSQL result',
            'intext:"Syntax error" OR intext:"GetArray()" OR intext:"FetchRow()"')

#realiza a busca com o termo passado por parametro
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    #pprint.pprint(res['searchInformation']['totalResults'])
    if(res['searchInformation']['totalResults'] == '0'):
        return ''
    else:
        return res['items']

#pega os campos necessarios dentro da resposta da api
def result_gcs(results):
    for result in results:
        #pprint.pprint(result)
        title = result['title']
        link = result['link']
        #dis = result['snippet']
        #print (title)
        print(link)
        #print (dis)

def argumentosPermitidos():
    asci = """    ____             __           ______
   / __ \____  _____/ /_______   / ____/___ ________  __
  / / / / __ \/ ___/ //_/ ___/  / __/ / __ `/ ___/ / / /
 / /_/ / /_/ / /  / ,< (__  )  / /___/ /_/ (__  ) /_/ /
/_____/\____/_/  /_/|_/____/  /_____/\__,_/____/\__, /
                                               /____/"""
    print(asci)
    print("Modo de usar: exemplo.com ajuda[-h] , busca[-s] \n sql[-q] , inurl[-u] , filetype[-f]")

#utiliza $sqldorks
def SqlDork(site):
    for sqldork in sqldorks:
        query = site +" "+ sqldork
        print (query)
        result = result_gcs(google_search(query, api_key, cse_id, num=1))
        if(result == 0):
            print("Nao foi obtido resultado utilizando SqlDorks")
        else:
            print(result)

def main():
    try:
        # $args pega parametros a partir da segunda string
        opts, args = getopt.getopt(sys.argv[2:], "hosdq")
        site = sys.argv[1]
        site = "inurl:"+site
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # "option -a not recognized"
        argumentosPermitidos()
        sys.exit(2)
    for o, a in opts:
        if o in ("-s"):
            #site = "site:"+site
            result_gcs(google_search(site, api_key, cse_id, num=1)) # num sao os numeros de resultados
        elif o in ("-h"):
            argumentosPermitidos()
            sys.exit()
        elif o in ("-d"):
            print("teste")
        elif o in ("-o"):
            print("teste")
        elif o in ("-q"):
            SqlDork(site)
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()