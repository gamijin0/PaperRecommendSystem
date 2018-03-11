import requests
from bs4 import BeautifulSoup as bs
from db_session import session, Venue
import sys
sys.path.append("..")

RANK_PAGE_ID = [
    "2903028135780", "2903028135856", "2903940690850", "2903028135775",
    "2903940690081", "2903940690325", "2903940690854", "2903940690839",
    "2903940690320", "2903940690316"
]
RANK_PAGE_BASE_URL = "http://history.ccf.org.cn/sites/ccf/biaodan.jsp?contentId="

if (__name__ == "__main__"):
    for ID in RANK_PAGE_ID:
        print(ID)
        page = requests.get(RANK_PAGE_BASE_URL + ID)
        BS = bs(page.content, "lxml")
        divs_lei = BS.find_all("div", {"class": "lei"})
        for div in divs_lei:
            big_rank = "D"
            if ("A" in div.text):
                big_rank = "A"
            elif ("B" in div.text):
                big_rank = "B"
            elif ("C" in div.text):
                big_rank = "C"
            else:
                continue
            table = div.next_sibling.next_sibling
            rows = table.find_all("tr")
            for row in rows[1:]:
                tds = row.find_all("td")
                data = [x.text.strip() for x in tds]
                new_venue = Venue()
                new_venue.small_rank = int(data[0])
                new_venue.abb = data[1]
                new_venue.name = data[2]
                new_venue.publishing_house = data[3]
                new_venue.url = data[4]
                new_venue.big_rank = big_rank
                try:
                    session.add(new_venue)
                    # print("Add: [%s:%s]" % (new_venue.abb,str(new_venue.big_rank)+str(new_venue.small_rank)))
                    session.commit()
                except Exception as e:
                    session.rollback()
                    print(e)
