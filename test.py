from requests import get as get_page
from BeautifulSoup import BeautifulSoup

urls = ('http://directemployersfoundation.org',
        'http://arinc.com',
        'http://ibm.jobs',
        'http://usatoday.com',
        'http://fark.com',
        )

def get_meta_data(url):
    """Returns a dict containing html document data"""
    r={}
    soup = BeautifulSoup(get_page(url).content)
    r["title"] = soup.head.title.text or ""
    info = soup.head.findAll("meta", attrs={"name":"description"})
    r["descrtiption"] = None    for i in info:
        r["description"]=info[0]['content']
    return r
        

for u in urls:
    site_info = get_meta_data(u)
    print u,site_info['title'],site_info['description']
