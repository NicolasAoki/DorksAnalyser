from googleapiclient.discovery import build
import getopt, sys

api_key = "AIzaSyD4ePQSrWHZCsVRfuf1goOPgzFB9gJbhMM"
cse_id = "017305337282449250408:jxmfygjffvs"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def result_gcs(results):
    for result in results:
        #pprint.pprint(result)
        title = result['title']
        #link = result['formattedUrl']
        #dis = result['snippet']
        print (title)
        #print (link)
        #print (dis)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[2:], "ho:v", ["help", "output="])
        site = sys.argv[1]
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            results = google_search(site, api_key, cse_id, num=3)
            result_gcs(results)
        elif o in ("-h", "--help"):
            print(site)
            print("teste")
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    # ...

if __name__ == "__main__":
    main()