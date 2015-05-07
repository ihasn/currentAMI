import json
import urllib2
from bs4 import BeautifulSoup
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

REGIONS = [
    "US East N. Virginia",
    "US West Oregon",
    "US West N. California",
    "EU Ireland",
    "EU Frakfurt",
    "Asia Pacific Singapore",
    "Asia Pacific Tokyo",
    "Asia Pacific Sydney",
    "South America Sao Paolo",
    "China Beijing",
    "AWS GovCloud"
]

VIRTLAYER = {'HVM (SSD) EBS-Backed 64-bit': '',
             'HVM Instance Store 64-bit': '',
             'PV EBS-Backed 64-bit': '',
             'PV Instance Store 64-bit': ''}



url = "https://aws.amazon.com/amazon-linux-ami/"
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

tables = soup.findChild('table')
rows = tables.findChildren(['th', 'tr'])

region_count = 0
virt_count = 0

for row in rows:
    cells = row.findChildren('td')
    if str(cells) == '[]':
        cells = 0
    else:
        for cell in cells:
            value = cell.string
            if str(value) == 'None':
                #print REGIONS[region_count]
                REGION = REGIONS[region_count]
            elif str(value) == 'AWS Marketplace':
                pass
            elif "ami" in value:
                if virt_count == 0:
                    VIRTLAYER['HVM (SSD) EBS-Backed 64-bit'] = value
                    #print 'HVM (SSD) EBS-Backed 64-bit' + ': ' + value
                elif virt_count == 1:
                    VIRTLAYER['HVM Instance Store 64-bit'] = value
                    #print 'HVM Instance Store 64-bit' + ': ' + value
                elif virt_count == 2:
                    VIRTLAYER['PV EBS-Backed 64-bit'] = value
                    #print 'PV EBS-Backed 64-bit' + ': ' + value
                elif virt_count == 3:
                    VIRTLAYER['PV Instance Store 64-bit'] = value
                    #print 'PV Instance Store 64-bit' + ': ' + value
                virt_count += 1
            else:
                pass
        region_count += 1
        virt_count = 0
        print json.dumps([REGION, {'HVM (SSD) EBS-Backed 64-bit': VIRTLAYER['HVM (SSD) EBS-Backed 64-bit'],
                           'HVM Instance Store 64-bit': VIRTLAYER['HVM Instance Store 64-bit'],
                           'PV EBS-Backed 64-bit': VIRTLAYER['PV EBS-Backed 64-bit'],
                           'PV Instance Store 64-bit': VIRTLAYER['PV Instance Store 64-bit']}],
                            sort_keys=True, indent=4, separators=(',', ': '))