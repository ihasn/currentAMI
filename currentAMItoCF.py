import urllib2
from bs4 import BeautifulSoup
import sys

reload(sys)
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


def get_current_AMI_info():
    url = "https://aws.amazon.com/amazon-linux-ami/"
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    tables = soup.findChild('table')
    rows = tables.findChildren(['th', 'tr'])
    return rows


def find_current_AMI(rows, REGIONS, VIRTLAYER, user_request):
    user_region_request = user_request[0]
    user_virtlayer_request = user_request[1]
    region_count = 0
    virt_count = 0
    x = 0
    for row in rows:
        cells = row.findChildren('td')
        if str(cells) == '[]':
            pass
        else:
            for cell in cells:
                value = cell.string
                if str(value) == 'None':
                    REGION = REGIONS[region_count]
                elif str(value) == 'AWS Marketplace':
                    pass
                elif "ami" in value:
                    if virt_count == 0:
                        VIRTLAYER['HVM (SSD) EBS-Backed 64-bit'] = value
                    elif virt_count == 1:
                        VIRTLAYER['HVM Instance Store 64-bit'] = value
                    elif virt_count == 2:
                        VIRTLAYER['PV EBS-Backed 64-bit'] = value
                    elif virt_count == 3:
                        VIRTLAYER['PV Instance Store 64-bit'] = value
                    virt_count += 1
                    if REGION == user_region_request:
                        x = 1
                else:
                    pass
            region_count += 1
            virt_count = 0
            if x == 1:
                break

def user_lookup(REGIONS, VIRTLAYER):
    region = raw_input('Region: ')
    if region in REGIONS:
        virt_type = raw_input('Virt Type: ')
        if virt_type in VIRTLAYER:
            return region, virt_type
        else:
            print "Not Valid VirtLayer"
            main()
    else:
        print "Not Valid Region"
        main()


def discover_current_AMI(user_request, VIRTLAYER):
    region = user_request[0]
    virt_type = user_request[1]
    return region, VIRTLAYER[virt_type]


def main():
    user_request = user_lookup(REGIONS, VIRTLAYER)
    rows = get_current_AMI_info()
    find_current_AMI(rows, REGIONS, VIRTLAYER, user_request)
    region_ami = discover_current_AMI(user_request, VIRTLAYER)
    return region_ami


if __name__ == "__main__":
    main()