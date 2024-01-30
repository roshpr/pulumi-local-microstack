import pulumi
# fetch config values
config = pulumi.Config('computestack')
name = config.require('name')
instancetype = config.require('instancetype')
keyname = config.require('key_name')

aws_config = pulumi.Config('aws');
region = aws_config.require('region');