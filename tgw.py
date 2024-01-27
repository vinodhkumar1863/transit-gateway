import boto3

# Create VPCs
ec2 = boto3.resource('ec2')

# Create VPC 1
vpc1 = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc1_id = vpc1.id

# Create VPC 2
vpc2 = ec2.create_vpc(CidrBlock='10.2.0.0/16')
vpc2_id = vpc2.id

# Create VPC 3
vpc3 = ec2.create_vpc(CidrBlock='10.10.0.0/16')
vpc3_id = vpc3.id

# Enable DNS Support and Hostname for VPCs
vpc1.modify_attribute(EnableDnsSupport={'Value': True})
vpc1.modify_attribute(EnableDnsHostnames={'Value': True})

vpc2.modify_attribute(EnableDnsSupport={'Value': True})
vpc2.modify_attributet(EnableDnsHostnames={'Value': True})

vpc3.modify_attribute(EnableDnsSupport={'Value': True})
vpc3.modify_attribute(EnableDnsHostnames={'Value': True})

# Create Subnets
subnet1 = ec2.create_subnet(VpcId=vpc1_id, CidrBlock='10.0.1.0/24', AvailabilityZone='us-east-1a')
subnet2 = ec2.create_subnet(VpcId=vpc1_id, CidrBlock='10.0.2.0/24', AvailabilityZone='us-east-1b')

subnet3 = ec2.create_subnet(VpcId=vpc2_id, CidrBlock='10.2.1.0/24', AvailabilityZone='us-east-1a')
subnet4 = ec2.create_subnet(VpcId=vpc2_id, CidrBlock='10.2.2.0/24', AvailabilityZone='us-east-1b')

subnet5 = ec2.create_subnet(VpcId=vpc3_id, CidrBlock='10.10.1.0/24', AvailabilityZone='us-east-1a')
subnet6 = ec2.create_subnet(VpcId=vpc3_id, CidrBlock='10.10.2.0/24', AvailabilityZone='us-east-1b')

# Create Transit Gateway
tgw = ec2.create_transit_gateway(Description='TransitGateway')
tgw_id = tgw.id

# Attach VPCs to Transit Gateway
ec2.create_transit_gateway_vpc_attachment(TransitGatewayId=tgw_id, VpcId=vpc1_id, SubnetIds=[subnet1.id, subnet2.id])
ec2.create_transit_gateway_vpc_attachment(TransitGatewayId=tgw_id, VpcId=vpc2_id, SubnetIds=[subnet3.id, subnet4.id])
ec2.create_transit_gateway_vpc_attachment(TransitGatewayId=tgw_id, VpcId=vpc3_id, SubnetIds=[subnet5.id, subnet6.id])

# Route Tables and Routes
route_table1 = ec2.create_route_table(VpcId=vpc1_id)
route_table2 = ec2.create_route_table(VpcId=vpc2_id)
route_table3 = ec2.create_route_table(VpcId=vpc3_id)

ec2.create_transit_gateway_route(TransitGatewayRouteTableId=route_table1.id, DestinationCidrBlock='10.10.0.0/16', TransitGatewayAttachmentId=tgw_id)
ec2.create_transit_gateway_route(TransitGatewayRouteTableId=route_table2.id, DestinationCidrBlock='10.10.0.0/16', TransitGatewayAttachmentId=tgw_id)
ec2.create_transit_gateway_route(TransitGatewayRouteTableId=route_table3.id, DestinationCidrBlock='10.0.0.0/16', TransitGatewayAttachmentId=tgw_id)
ec2.create_transit_gateway_route(TransitGatewayRouteTableId=route_table3.id, DestinationCidrBlock='10.2.0.0/16', TransitGatewayAttachmentId=tgw_id)
