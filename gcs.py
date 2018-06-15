from googleapiclient.discovery import build
import getopt, sys

api_key = "AIzaSyD4ePQSrWHZCsVRfuf1goOPgzFB9gJbhMM"
cse_id = "017305337282449250408:jxmfygjffvs"

#realiza a busca com o termo passado por parametro
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

#pega os campos necessarios dentro da resposta da api
def result_gcs(results):
    for result in results:
        #pprint.pprint(result)
        title = result['title']
        link = result['formattedUrl']
        #dis = result['snippet']
        print (title)
        print (link)
        #print (dis)

def argumentosPermitidos():
    print("Modo de usar: exemplo.com [-h] ou [-v]")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "hosd")
        site = sys.argv[1]
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # "option -a not recognized"
        argumentosPermitidos()
        sys.exit(2)
    for o, a in opts:
        if o == ("-s"):
            result_gcs(google_search(site, api_key, cse_id, num=2))
        elif o in ("-h"):
            argumentosPermitidos()
            sys.exit()
        elif o in ("-d"):
            print("teste")
        elif o in ("-o"):
            print("teste")
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()