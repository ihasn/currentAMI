""" This is a test
"""

import currentAMItoCF
from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template
import troposphere.ec2 as ec2

TEST = currentAMItoCF.main()
AMI = TEST[1]
REGION = TEST[0]
TEMPLATE = Template()
KEYNAME_PARAM = TEMPLATE.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

TEMPLATE.add_mapping('RegionMap', {
    currentAMItoCF.NAME_TO_REGION[REGION]: {"HVM64": AMI}
})

EC2_INSTANCE = TEMPLATE.add_resource(ec2.Instance(
    "Ec2Instance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t1.micro",
    KeyName=Ref(KEYNAME_PARAM),
    SecurityGroups=["default"],
    UserData=Base64("80")
))

TEMPLATE.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(EC2_INSTANCE),
    ),
    Output(
        "AZ",
        Description="Availability Zone of the newly created EC2 instance",
        Value=GetAtt(EC2_INSTANCE, "AvailabilityZone"),
    ),
    Output(
        "PublicIP",
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(EC2_INSTANCE, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the newly created EC2 instance",
        Value=GetAtt(EC2_INSTANCE, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(EC2_INSTANCE, "PublicDnsName"),
    ),
    Output(
        "PrivateDNS",
        Description="Private DNSName of the newly created EC2 instance",
        Value=GetAtt(EC2_INSTANCE, "PrivateDnsName"),
    ),
])

print TEMPLATE.to_json()
