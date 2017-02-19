from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import json
import requests

# # This restores the same behavior as before.
# context = ssl._create_unverified_context()
# urllib.urlopen("https://no-valid-cert", context=context)
#
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
#
# url='https://www.meetup.com'
# # html=urlopen(url, context=ctx).read()
#
# from urllib.request import Request, urlopen
#
# req = Request(url, headers={'User-Agent': 'Chrome'})
# webpage = urlopen(req).read()
# sp = BeautifulSoup(html, 'html.parser')
# print (sp)
def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = params)
    prepped = req.prepare()
    return prepped.url

BASE_URL2= "https://api.meetup.com/find/groups"
m_param={}
m_param["zip"]=48502
m_param['key']='71584565545fb2045795d5c2e3a6d'
m_param['radius']=2
full_url = requestURL(BASE_URL2,m_param)

m_response = requests.get(full_url) #
zzz=json.loads(m_response.text)[0]


class Event():
    def __init__(self, each_post={}):
        if 'name' in each_post:
            self.name=each_post['name']
        else:
            self.name=''

        if 'yes_rsvp_count' in each_post:
            self.rsvp=each_post['yes_rsvp_count']
        else:
            self.rsvp=''

        if 'venue' in each_post:
            self.venue_name=each_post['venue']['name']
        else:
            self.venue_name=''

        if 'venue' in each_post:
            self.lat=each_post['venue']['lat']
        else:
            self.lat=''

        if 'venue' in each_post:
            self.lon=each_post['venue']['lon']
        else:
            self.lon=''

        if 'city' in each_post:
            self.city=each_post['venue']['city']
        else:
            self.city=''


    def location(self):
        return (self.lat, self.lon)


ist=[]
for n in range(1):
    base_url='https://api.meetup.com/The-Flint-Area-Innovation-Entrepreneurship-Meetup-Group/events?&key=71584565545fb2045795d5c2e3a6d&group&offset='+str(n)+'&page=200'
    k_param={}
    k_param['status']='past'
    k_param['desc']='True'

    full_url = requestURL(base_url,k_param)
    m_response = requests.get(full_url) #
    zzz=json.loads(m_response.text)
    # print (zzz)
    for i in zzz:
        ist.append(Event(i))
# print (ist)
#not overlapped instance list
a=[]
for i in ist:
    if i not in a:
        a.append(i)

event_name={}
for i in a:
    if i.name not in event_name:
        event_name[i.name]=1
    else:
        event_name[i.name]=event_name[i.name]+1
# print ((event_name.keys()))

rsvp=[]
lat=[]
lon=[]
venue=[]
for i in a:
    rsvp.append(i.rsvp)
    lat.append(i.lat)
    lon.append(i.lon)
    venue.append(i.venue_name)


rec =open('flint.csv','w')
rec.write("{},{},{},{},{}\n".format('group','latitude','longitude','num_rsvp','location'))

tup=zip(event_name.keys(),lat,lon,rsvp,venue)

for tu in tup:
    rec.write("{},{},{},{},{}\n".format(*tu))
rec.close()

class Member():
    def __init__(self, each_post={}):
        if 'name' in each_post:
            self.name=each_post['name']
        else:
            self.name=''

        if 'city' in each_post:
            self.city=each_post['city']
        else:
            self.city=''

        if 'lon' in each_post:
            self.lon=each_post['lon']
        else:
            self.lon=''

        if 'lat' in each_post:
            self.lat=each_post['lat']
        else:
            self.lat=''

#all members
member=[]
for n in range(5):
    m_response = requests.get('https://api.meetup.com/2/members?&key=71584565545fb2045795d5c2e3a6d&group_urlname=The-Flint-Area-Innovation-Entrepreneurship-Meetup-Group&offset='+str(n)+'&page=200')
    zzz=json.loads(m_response.text)
    # print (zzz)
    # for i in [i['name'] for i in zzz['results']]:
    #     if i not in memberChecking:
    #         memberChecking.append(i)
    for i in zzz['results']:
        member.append(Member(i))
# print (ist)
#not overlapped instance list
b=[]
for i in member:
    if i not in b:
        b.append(i)

lat=[]
lon=[]
name=[]
city=[]
for i in b:
    lat.append(i.lat)
    lon.append(i.lon)
    city.append(i.city)
    name.append(i.name)
rec =open('member.csv','w')
rec.write("{},{},{},{}\n".format('name','city','latitude','longitude'))

tup=zip(name, city, lat, lon)

for tu in tup:
    rec.write("{},{},{},{}\n".format(*tu))
rec.close()






#active attendee
# m_response = requests.get('https://api.meetup.com/2/members?&key=71584565545fb2045795d5c2e3a6d&group_urlname=The-Flint-Area-Innovation-Entrepreneurship-Meetup-Group&offset=2&page=200')
#
# zzz=json.loads(m_response.text)
#
# print (len(zzz['results']))
