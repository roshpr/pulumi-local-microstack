"""An AWS Python Pulumi program"""

import pulumi
from pulumi import StackReference
from resources.compute import Compute
import logging as log

stack_ref = StackReference(f"organization/networkstack/stage")
subnet_id = stack_ref.require_output('subnet_id')
vpc_id = stack_ref.require_output('vpc_id')
log.info('Subnet id from networkstack: {}'.format(subnet_id))
comp = Compute(vpc_id, subnet_id)
sg = comp.create_security_group()
server = comp.create_instance(sg)

pulumi.export("public_ip", server.public_ip)
pulumi.export("public_dns", server.public_dns)