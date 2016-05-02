from bs4 import BeautifulSoup
import requests
import sys, os

base_url = "http://jandan.net/ooxx/page-%d#comments"

start_page = 1500
stop_page = 1970

def main():
    for index in xrange(start_page, stop_page):
        
        # make a directory for each page
        dir_name = 'dir_' + str(index) 
        os.mkdir(dir_name, 0744)

        
        url = base_url % (index)
       
        print '[%d] Visiting  %s' % (index, url)
        request = requests.get(url)

        # parse html
        html = BeautifulSoup(request.text, "html.parser")
        divs = html.find_all('div', attrs={'class': 'text'})

        for div in divs:

            # there is only one single <img> tag in each div
            img = div.find_all('img')[0]
            
            # check if the img has 'src' attr
            if img.has_attr('src'):
                src = img['src']
            else:
                continue
            
            # make a file name using last 24 chars of img src
            filename = '%s/%s' % (dir_name, src[-24:])

            # download the image
            print '[%d] Downloading %s to %s' % (index, src, filename)
            with open(filename, 'wb') as jpg:
                jpg.write(requests.get(src, stream=True).content)


def int_check(arg):
    if int(arg) in xrange(1500, 1970):
        return True
    return False

def print_usage():
    print 'usage:\npython jandan.py [start_page] [stop_page]'
    sys.exit(0)

if __name__ == '__main__':

    argv_len = len(sys.argv)

    if argv_len == 1:
        main()

    elif argv_len == 3:
        args = sys.argv[1:]
        
        if int_check(args[0]) and int_check(args[1]):
            if args[0] <= args[1]:
                start_page = int(args[0])
                stop_page = int(args[1])
            else:
                start_page = int(args[1])
                stop_page = int(args[0])
        
            main()
        else:
            print_usage()

    else:
        print_usage()
