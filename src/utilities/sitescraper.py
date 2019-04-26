import urllib3

from threading import Thread
from . import constants
from bs4 import BeautifulSoup


HTTP = urllib3.PoolManager()


def retrieve_articles():
    articles = []

    for page in range(constants.NEWS_PAGE_START, constants.NEWS_PAGE_END + 1):
        news_url = constants.NEWS_ENDPOINT + str(page)

        response = HTTP.request('GET', news_url,
                                timeout=constants.TIMEOUT_SECONDS)

        # TODO: Handle response failure

        soup = BeautifulSoup(response.data, 'html.parser')
        main_content = soup.find('div', attrs={'class': 'td-ss-main-content'})
        article_blocks = main_content.find_all(
            'div', attrs={'class': 'td-block-span6'})

        if article_blocks:
            for article_block in article_blocks:
                article = {}
                threads = []

                # Retrieve the article image URL
                threads.append(
                    Thread(target=extract_article_image_and_title, args=(article_block, article)))
                # Retrieve the title link
                threads.append(Thread(
                    target=extract_title_link_and_meta_content, args=(article_block, article)))
                # Retrieve the article category
                threads.append(Thread(target=extract_article_category,
                                      args=(article_block, article)))

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                articles.append(article)

    return articles


def extract_article_image_and_title(article_block, article):
    print('A')
    article_thumb = article_block.find(
        'div', attrs={'class': 'td-module-thumb'})
    image_url = article_thumb.find('img')['src']
    print('Found image link: {}'.format(image_url))
    title = article_thumb.find('img')['title']
    print('Found title: {}'.format(title))

    article['image_url'] = image_url
    article['title'] = title

    article_link = article_block.find('a')['href']
    print('DAWG: {}'.format(article_link))
    print(type(article_link))

    threadBoi = Thread(target=get_article_meta_content,
                       args=(article_link, article))
    threadBoi.start()
    threadBoi.join()
    print("DONE WITH BOI")


def extract_title_link_and_meta_content(article_block, article):
    print('B')
    article_header = article_block.find(
        'h3', attrs={'class': 'entry-title td-module-title'})
    title_link = article_header.find('a', href=True)['href']
    print('Found link: {}'.format(title_link))

    # meta_content = get_article_meta_content(title_link)
    # print('Found meta content: {}'.format(meta_content))
    # print("GOT META KNIGHT")

    article['title_link'] = title_link
    print("DONE WITH B")


def extract_article_category(article_block, article):
    print('C')
    article_div = article_block.find(
        'div', attrs={'class': 'td-module-meta-info'})
    category = article_div.find('a').text
    print('Found category: {}'.format(category))

    article['category'] = category
    print("DONE WITH C")


def get_article_meta_content(article_link, article):
    response = HTTP.request('GET', article_link,
                            timeout=constants.TIMEOUT_SECONDS)
    soup = BeautifulSoup(response.data, 'html.parser')

    meta = soup.find('meta', attrs={'name': 'description'})

    article['meta_content'] = meta['content']
