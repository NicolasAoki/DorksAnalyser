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
    #    res recebe a requisicao pro google
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    #pprint.pprint(res['searchInformation']['totalResults'])
    #    se nao houver resultados daquela busca
    #    retorna vazio
    if(res['searchInformation']['totalResults'] == '0'):
        return ''
    else:
        #   se houver resultados da busca
        #   retorna o array de todos itens
        return res['items']

#pega os campos necessarios dentro da resposta da api
def result_gcs(results):
    for result in results:
        #pprint.pprint(result)
        # $link recebe o endereco encontrado
        link = result['link']
        print(link)

def argumentosPermitidos():
    asci = """ 
    ____             __           ______
   / __ \____  _____/ /_______   / ____/___ ________  __
  / / / / __ \/ ___/ //_/ ___/  / __/ / __ `/ ___/ / / /
 / /_/ / /_/ / /  / ,< (__  )  / /___/ /_/ (__  ) /_/ /
/_____/\____/_/  /_/|_/____/  /_____/\__,_/____/\__, /
                                               /____/"""
    print(asci)
    print("Modo de usar: exemplo.com ajuda[-h] , busca[-s] \n FalhaSql[-q] , inurl[-u] , filetype[-f]")

#utiliza $sqldorks
def SqlDork(site):
    #    faz a interecao do site
    #    em cada item da array de Dork armazenada
    for sqldork in sqldorks:
        query = site +" "+ sqldork
        #    printa a query montada
        #    site + query
        print(query)
        result = result_gcs(google_search(query, api_key, cse_id, num=1))
        #    $result printa None
        #    caso esteja vazio
        print(result)

def main():
    try:
        #     $args pega parametros a partir da segunda string
        opts, args = getopt.getopt(sys.argv[2:], "hosdq")
        site = sys.argv[1]
        site = "inurl:"+site
        if(site == '-h' or 'help' or '-help'):
            argumentosPermitidos()
    except getopt.GetoptError as err:
        #     printa erro "option -X not recognized"
        print(str(err))
        argumentosPermitidos()
        sys.exit(2)
    #   interacao entre os parametros encontrados
    #   vindos do input do usuario
    for o, a in opts:
        if o in ("-s"):
            #    $site input de busca do usuario
            #    $apikey chave necessaria para fazer requisicao ao google
            #    $cse_id Mecanismo de busca customizado criado previamente na API do google
            #    $num sao os numeros de resultados
            result_gcs(google_search(site, api_key, cse_id, num=1))
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