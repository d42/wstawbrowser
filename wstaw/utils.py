import string
import requests
from lxml import  etree
from io import StringIO
from os import path
from wstaw.models import Image
letters = string.digits + string.ascii_uppercase + string.ascii_lowercase
letters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
from django.core.exceptions import ObjectDoesNotExist
base = 62
last_image = 550027     # 2j5p

URL = "http://www.wstaw.org/w/{image_number}/"
#THUMBNAIL_URL = "http://wstaw.org/m/2013/10/28/138288711836_jpg_300x300_q85.jpg"
#DIRECT_URL    = "http://wstaw.org/m/2013/10/28/138288711836.jpg"
DIRECT_URL    = "http://wstaw.org{href}"
THUMBNAIL_APPEND = "_300x300_q85.jpg"



class WstawImage:

    parser = etree.HTMLParser()

    def get(self, num):
        try:
            image = Image.objects.get(image_number=num)
            return image
        except ObjectDoesNotExist:
            num_b62 = self.encode(num)

            r = requests.get(URL.format(image_number=num_b62))
            root = etree.parse(StringIO(r.text), self.parser)

            try:
                a = root.xpath('//div[@id="singlephoto"]/a')[0]
            except:
                i = Image(image_number=num,image_link='', thumbnail_link='' )
                i.save()
                return i

        href = a.attrib['href']

        url = DIRECT_URL.format(href=href)
        thumbnail_url = self.make_thumbnail_url(url)

        i = Image(image_number=num, image_link=url,thumbnail_link=thumbnail_url)
        i.save()

        return(i)

    def encode(self, num):
        enc_list = []
        if num == 0 : return '0'
        while num != 0:
            remainder = num%base
            num = num//base
            enc_list.append(
                    letters[remainder]
                    )
        return ''.join(enc_list[::-1])


    def make_thumbnail_url(self, url):
        ext = path.splitext(url)[1]
        thurl = "{}{}".format(
                url.replace(ext, ext.replace('.','_')),     # FIXME: when less tired
                THUMBNAIL_APPEND
                )   
        return thurl




Wstaw = WstawImage()



def list_split(l, n=4):
  return [l[i:i+n] for i in range(0, len(l), n)]

