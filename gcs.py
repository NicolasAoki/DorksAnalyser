import pprint

from googleapiclient.discovery import build
import getopt, sys

api_key = "AIzaSyD4ePQSrWHZCsVRfuf1goOPgzFB9gJbhMM"
cse_id = "017305337282449250408:jxmfygjffvs"

#http://fotohungarika.c3.hu/foto.php?mid=20&fi=1&l=1
sqldorks = ('intext:"supplied argument is not a valid MySQL result resource" OR intext:"You have an error in your SQL syntax"',
            'intext:"PostgreSQL query failed: ERROR: parser: parse error" OR intext:"supplied argument is not a valid PostgreSQL result',
            'intext:"Syntax error" OR intext:"GetArray()" OR intext:"FetchRow()"')

#http://www.unopar.br/portal/
#http://ftp.unicamp.br/pub/
#http://www.lideranca.com.br/programas/
#http://45.120.114.222/ftp/HDD2/Hindi%20Movies/
filedorks = ('intitle:"Index of" OR "Index of /backup"',
             'inurl:admin.php OR inurl:administrator.php OR inurl:cms.php ',
             '"# phpMyAdmin MySQL-Dump" "# Dumping data for table" "INSERT INTO" -"the" ext:sql ',
             'file:crossdomain ext:xml')

securityDorks = ('intext: passwords filetype: txt',
                 'intext: account details filetype: txt',
                 'config.php',
                 'ext:sql intext:@gmail.com intext:password',
                 'intext:(insert|set) ext:mysql',
                 'intext:(select|set) ext:mysql',
                 ' +(,user,|,login,) INSERT ext:sql',
                 '/index.php?id=')

indexOf = ('Index of /backup',
           'Index of /mail',
           'Index of /password',
           'Index of” / “chat/logs')

#realiza a busca com o termo passado por parametro
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    #    res recebe a requisicao pro google
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
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
        #pprint.pprint(result) #mostra todos resultado da requisicao
        # $link recebe o endereco encontrado
        link = result['link']
        print(link)

def argumentosPermitidos():
    asci = """     ____             __           ___                __                    
   / __ \____  _____/ /_______   /   |  ____  ____ _/ /_  __________  _____
  / / / / __ \/ ___/ //_/ ___/  / /| | / __ \/ __ `/ / / / / ___/ _ \/ ___/
 / /_/ / /_/ / /  / ,< (__  )  / ___ |/ / / / /_/ / / /_/ (__  )  __/ /    
/_____/\____/_/  /_/|_/____/  /_/  |_/_/ /_/\__,_/_/\__, /____/\___/_/     
                                                   /____/                  
"""
    print(asci)
    print("Modo de usar: exemplo.com ajuda[-h] , busca[-s] \n FalhaSql[-q] , FileDorks[-f], intextDorks[-i], diretorioDorks[-d]")

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

def FileDork(site):
    #    faz a interecao do site
    #    em cada item da array de Dork armazenada
    for filedork in filedorks:
        query = site +" "+ filedork
        #    printa a query montada
        #    site + query
        print(query)
        result = result_gcs(google_search(query, api_key, cse_id, num=1))
        #    $result printa None
        #    caso esteja vazio
        print(result)

def SecurityDorks(site):
    #    faz a interecao do site
    #    em cada item da array de Dork armazenada
    for securityDork in securityDorks:
        query = site +" "+ securityDork
        #    printa a query montada
        #    site + query
        print(query)
        result = result_gcs(google_search(query, api_key, cse_id, num=1))
        #    $result printa None
        #    caso esteja vazio
        print(result)

def DiretorioDorks(site):
    #    faz a interecao do site
    #    em cada item da array de Dork armazenada
    for index in indexOf:
        query = site +" "+ index
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
        opts, args = getopt.getopt(sys.argv[2:], "hsfqid")
        site = sys.argv[1]
        site = "inurl:"+site
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
        elif o in ("-f"):
            FileDork(site)
        elif o in ("-i"):
            SecurityDorks(site)
        elif o in ("-q"):
            SqlDork(site)
        elif o in ("-d"):
            DiretorioDorks(site)
        else:
            assert False, "unhandled option"

if __name__ == "__main__":
    main()