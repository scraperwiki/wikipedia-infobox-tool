import requests
import sys
import os

def get_query():
   query = "http://en.wikipedia.org/w/api.php?action=opensearch&search=" + sys.argv[1] + "&limit=100&namespace=14&format=json"
   x = requests.get(query)
   return x.text

def access_file():
   try:
       os.remove('categories.json')
       write_file()
       exit()
   except (IOError, OSError):
       write_file()
       exit()

def write_file():
    f = open('categories.json', 'w+')
    f.write(get_query())
    f.close

def main():
    access_file()
  
if __name__ == '__main__': 
    main()
