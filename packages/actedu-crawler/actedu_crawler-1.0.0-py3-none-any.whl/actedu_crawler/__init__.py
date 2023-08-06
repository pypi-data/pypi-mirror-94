import argparse, sys, os, re, subprocess
from requests import get
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description='Crawl documents on ACT Government websites.', usage='actedu_crawler -u [URL] -o [OUTPUT DIR]')
    parser.add_argument('-u', dest='url', type=str, help='Input URL.')
    parser.add_argument('-o', dest='output_dir', type=str, help='Output directory for downloaded content.')
    args = parser.parse_args()

    if(not args.output_dir):
        sys.exit('Output directory (-o) is required.')
    
    if(not args.url):
        sys.exit('URL (-u) is required.')
    
    if(not os.path.isdir(args.output_dir)):
        try:
            os.mkdir(args.output_dir)
        except:
            sys.exit(f'Could not create directory "{args.output_dir}"')
    
    if(re.match(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[act.edu.au]|[act.gov.au]\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)', args.url)): # Adapted this from https://stackoverflow.com/a/3809435
        parsed_url = 'http://' + re.search(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[act.edu.au]', args.url).group(0) + 'u/sitesearch?mode=results&current_result_page=1&results_per_page=9999999999&queries_keyword_query='
        print(f'Querying {parsed_url}...')
        doclist = BeautifulSoup(get(parsed_url).text, 'lxml').find('div', {'id': 'content_div_141185'}).find_all('div')[1:]
        print(f'Found {len(doclist)} documents...')
    
        if sys.platform == 'win32':
            cmd = 'aria2c.exe'
        else:
            cmd = 'aria2c'
        
        for doc in doclist:
            subprocess.run([cmd, doc.find("a")["href"], '-d', args.output_dir])
    else:
        sys.exit('Please enter a valid URL.')