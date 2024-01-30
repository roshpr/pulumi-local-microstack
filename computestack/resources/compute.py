from resources import *
import pulumi_aws as aws
import logging as log


class Compute:
    def __init__(self, vpc_id, subnet_id):
        log.info('Compute initialized')
        self.subnet_id = subnet_id
        self.vpc_id = vpc_id

    def create_security_group(self):
        group = aws.ec2.SecurityGroup(
            "web-secgrp",
            description="Enable HTTP access",
            vpc_id=self.vpc_id,
            ingress=[
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=80,
                    to_port=80,
                    cidr_blocks=["0.0.0.0/0"],
                ),
                aws.ec2.SecurityGroupIngressArgs(
                    protocol="tcp",
                    from_port=22,
                    to_port=22,
                    cidr_blocks=["0.0.0.0/0"],
                )
            ],
        )
        return group

    def create_instance(self, group):
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["amazon"],
            filters=[
                aws.ec2.GetAmiFilterArgs(
                    name="name",
                    values=["amzn2-ami-hvm-*"]
                )
            ],
        )
        user_data = """
        #!/bin/bash
        echo "Hello, World!" > index.html
        nohup python -m SimpleHTTPServer 80 &
        """

        server = aws.ec2.Instance(
            "web-server-www",
            instance_type=instancetype,
            vpc_security_group_ids=[group.id],
            subnet_id=self.subnet_id,
            user_data=user_data,
            ami=ami.id,
            key_name=keyname,
            tags={
                "Name": "{}-instance".format(name),  # A friendly name for the EC2 instance
            }
        )
        return server

