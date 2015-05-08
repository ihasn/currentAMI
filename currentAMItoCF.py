# coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding("utf8")

NAME_TO_REGION = {
    'US East N. Virginia': 'us-east-1',
    'US West N. California': 'us-west-1',
    'US West Oregon': 'us-west-2',
    'EU Ireland': 'eu-west-1',
    'EU Frankfurt': 'eu-central-1',
    'Asia Pacific Singapore': 'ap-southeast-1',
    'Asia Pacific Sydney': 'ap-southeast-2',
    'Asia Pacific Tokyo': 'ap-northeast-1',
    'South America São Paolo': 'sa-east-1',
    'China Beijing': 'cn-north-1',
    'AWS GovCloud': 'us-gov-west-1'
}

REGION_TO_NAME = {
    'us-east-1': 'US East N. Virginia',
    'us-west-1': 'US West N. California',
    'us-west-2': 'US West Oregon',
    'eu-west-1': 'EU Ireland',
    'eu-central-1': 'EU Frankfurt',
    'ap-southeast-1': 'Asia Pacific Singapore',
    'ap-southeast-2': 'Asia Pacific Sydney',
    'ap-northeast-1': 'Asia Pacific Tokyo',
    'sa-east-1': 'South America São Paolo',
    'cn-north-1': 'China Beijing',
    'us-gov-west-1': 'AWS GovCloud'
}

REGIONS = [
    'US East N. Virginia',
    'US West N. California',
    'US West Oregon',
    'EU Ireland',
    'EU Frankfurt',
    'Asia Pacific Singapore',
    'Asia Pacific Sydney',
    'Asia Pacific Tokyo',
    'South America São Paolo',
    'China Beijing',
    'AWS GovCloud'
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

def user_lookup(NAME_TO_REGION, VIRTLAYER):
    region = raw_input('Region: ')
    if region in NAME_TO_REGION:
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
    user_request = user_lookup(NAME_TO_REGION, VIRTLAYER)
    rows = get_current_AMI_info()
    find_current_AMI(rows, REGIONS, VIRTLAYER, user_request)
    region_ami = discover_current_AMI(user_request, VIRTLAYER)
    return region_ami


if __name__ == "__main__":
    main()