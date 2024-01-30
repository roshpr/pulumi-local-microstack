from resources import *
import pulumi_aws as aws
import logging as log


class NetowrkSecurity:
    def __init__(self):
        log.info('Initialized network security')

    def create_acl(self, vpc):
        # Creating a Network ACL
        network_acl = aws.ec2.NetworkAcl('network-acl',
                     vpc_id=vpc.id,
                     tags={'Name': '{}-network-acl'.format(name)}
        )
        return network_acl


    def create_eip(self):
        # Creating a NAT Gateway
        nat_eip = aws.ec2.Eip('nat-eip',
                  vpc=True  # Allocate the EIP in the VPC
        )
        return nat_eip


    def create_natgw(self, public_subnet, nat_eip):
        nat_gateway = aws.ec2.NatGateway('nat-gateway',
                     subnet_id=public_subnet.id,  # Placing NAT Gateway in the public subnet
                     allocation_id=nat_eip.id,
                     tags={'Name': '{}-nat-gateway'.format(name)}
        )
        return nat_gateway


