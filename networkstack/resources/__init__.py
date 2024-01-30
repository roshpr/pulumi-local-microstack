import pulumi

# fetch config values
config = pulumi.Config()
name = config.require('name')

aws_config = pulumi.Config("aws");
region = aws_config.require("region");
