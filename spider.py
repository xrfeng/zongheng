import requests
from bs4 import BeautifulSoup
from multiprocessing import Process

def get_soup(url):
    resp = requests.get(url).content
    soup = BeautifulSoup(resp,'lxml')
    return soup

def parse_chapters(soup):
    chapter_list = []
    chapters = soup.select('td.chapterBean > a')
    for chapter in chapters:
        chapter_url = chapter['href']
        chapter_title = chapter.get_text()
        chapter_list.append((chapter_title,chapter_url))
    return chapter_list

def parse_content(soup):
    contents = []
    mark_ps = soup.select('div#readerFs > p')
    for p in mark_ps:
        content = p.get_text()
        contents.append(content)
    return contents

def save_chapter(i):
    title = i[0]
    soup = get_soup(i[1])
    contents = parse_content(soup)
    filename = './sjchangan/%s.txt'% title
    with open(filename,'a',encoding='utf-8')as f:
        f.write(title)
        f.write('\n\n')
        for c in contents:
            f.write(c)
            f.write('\n')

def main(chapter_list):
    # base_url = 'http://book.zongheng.com/showchapter/431658.html'
    # base_url = 'http://book.zongheng.com/showchapter/563219.html'
    # soup = get_soup(base_url)
    # chapter_list = parse_chapters(soup)
    for i in chapter_list:
        save_chapter(i)
        print(i[0],'saved')

if __name__ == '__main__':
    base_url = 'http://book.zongheng.com/showchapter/563219.html'
    soup = get_soup(base_url)
    chapter_list = parse_chapters(soup)
    # print(chapter_list)

    # 1. single process
    main(chapter_list)

    # 2. multiprocessing process
    # no problem
    # p = Process(target=main, args=(chapter_list,))
    # p.start()
    # p.join()
