import requests
from lxml import etree

def get_title_and_page(baseurl):
    html = url_retry(baseurl)
    selector = etree.HTML(html)
    title = selector.xpath('/html/head/title/text()')[0]
    page = selector.xpath('//span[@class="pages"]/text()')[0]
    return title.replace(" | Briefing Amazon Knowledge",""), page.replace("Page 1 of ", "")

def get_subpages(url, counter):
    html = url_retry(url)
    selector = etree.HTML(html)
    link = selector.xpath('//*[@id="post-content"]/div[1]/p[1]/text()')
    question = ' '.join(link).strip()
    choiceA = selector.xpath('//*[@id="post-content"]/div[1]/p[2]//text()')
    choiceA = " " + " ".join(choiceA).strip()
    choices = selector.xpath('//*[@id="post-content"]/div[1]/p[position() > 2]//text()')
    choices = " ".join(choices).strip().split("\n")
    choices[0] = " " + choices[0]
    choices.insert(0,choiceA)
    answers = selector.xpath('//*[@id="post-content"]//p[@class="rightAnswer"]/text()')
    answers = " ".join(answers).strip().strip("\n")
    blockquote = selector.xpath('//*[@id="post-content"]/div[1]/blockquote//text()')
    blockquote = " ".join(blockquote).strip()
    try:
        with open("/Users/MK/Desktop/briefmenow-crawler/Questions/" + title + ".txt", "a") as f:
            f.write("Question" + str(counter) + ": " + question.encode("utf-8") + '\n')
            for x in choices:
                f.write(x.encode("utf-8") + "\n")
            f.write("answers: " + answers.encode("utf-8") + '\n')
            f.write(blockquote.encode("utf-8") + '\n')
            f.write('\n')
    except Exception,e:
        print(question + '\n' + e.message)

def url_retry(url,num_retries=5):
    try:
        request = requests.get(url,timeout=60)
        request.raise_for_status()
        html = request.content
    except Exception,e:
        print "!!!!!!!!!"
        print e.message
        if num_retries>0:
            print "=====Retry Remains===== " + str(num_retries)
            return url_retry(url,num_retries-1)
    return html

if __name__ == '__main__':
    page = 1
    counter = 0
    baseurl = 'https://www.briefmenow.org/amazon/category/exam-aws-devops-aws-certified-devops-engineer/'
    title, maxpage = get_title_and_page(baseurl)
    print "max page number is " + maxpage
    print "exam title is " + title
    while page <= int(maxpage):
        print ("page number is: " + str(page))
        counter = 10 * (page - 1)# 10 questions on each page
        url = baseurl + '/page/%s/'%(page)
        html = url_retry(url)
        selector = etree.HTML(html)
        subpages = selector.xpath('//article/header/h2/a//@href')
        for u in subpages:
            counter += 1
            get_subpages(u, counter)
            print "question number is: %s" %counter
        page += 1       
    print "done"