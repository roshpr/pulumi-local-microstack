"""An AWS Python Pulumi program"""

import pulumi
from resources.network import Network
from resources.network_security import NetowrkSecurity

def create_network():
    nw = Network()
    vpc, igw = nw.create_vpc()
    public_subnet = nw.create_subnet(vpc)
    route_table = nw.create_route_table(vpc, igw, public_subnet)

    security = NetowrkSecurity()
    network_acl = security.create_acl(vpc)
    nat_eip = security.create_eip()
    nat_gateway = security.create_natgw(public_subnet, nat_eip)

    # Exporting the IDs of the created resources
    pulumi.export('vpc_id', vpc.id)
    pulumi.export('internet_gateway_id', igw.id)
    pulumi.export('subnet_id', public_subnet.id)
    pulumi.export('route_table_id', route_table.id)
    pulumi.export('network_acl_id', network_acl.id)
    pulumi.export('nat_gateway_id', nat_gateway.id)

create_network()