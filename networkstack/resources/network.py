from resources import *
import pulumi_aws as aws
import logging as log

class Network:
    def __init__(self, cidr='10.0.0.0/16'):
        log.info('Network initialized')
        self.cidr = cidr

    def create_vpc(self):
        vpc = aws.ec2.Vpc(name,
              cidr_block=self.cidr,  # Example CIDR block
              enable_dns_support=True,
              enable_dns_hostnames=True,
              tags={'Name': '{}-vpc'.format(name)}
        )
        # Creating an Internet Gateway for the VPC

        igw = aws.ec2.InternetGateway('igw',
              vpc_id=vpc.id,
              tags={'Name': name}
        )
        return vpc, igw

    def create_subnet(self, vpc):
        # Creating a public Subnet
        public_subnet = aws.ec2.Subnet('{0}-public-subnet'.format(name),
            cidr_block='10.0.1.0/24',  # Example CIDR block for public subnet
            vpc_id=vpc.id,
            map_public_ip_on_launch=True,  # Enable auto-assign public IP
            availability_zone='{}a'.format(region),  # Example availability zone
            tags={'Name': '{}-public-subnet'.format(name)}
        )
        return public_subnet

    def create_route_table(self, vpc, igw, public_subnet):
        # Creating a Route Table
        route_table = aws.ec2.RouteTable('route-table',
            vpc_id=vpc.id,
            routes=[
                aws.ec2.RouteTableRouteArgs(  # Local route for VPC traffic
                    cidr_block=vpc.cidr_block,
                    gateway_id='local'
                ),
                aws.ec2.RouteTableRouteArgs(  # Default route via Internet Gateway
                    cidr_block='0.0.0.0/0',
                    gateway_id=igw.id
                )
            ],
            tags={'Name': '{}-route-table'.format(name)}
        )

        # Associate the Route Table with the Subnet
        route_table_association = aws.ec2.RouteTableAssociation('route-table-association',
            route_table_id=route_table.id,
            subnet_id=public_subnet.id
        )
        return route_table

