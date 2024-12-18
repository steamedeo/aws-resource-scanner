import boto3
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class DateTimeEncoder(json.JSONEncoder):
    """ Custom JSON encoder for datetime objects. """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def get_aws_resources_by_region(region, session):
    """ Retrieves AWS resources for a specific region. """
    resources = {}
    try:
        ec2_client = session.client('ec2', region_name=region)
        resources['ec2'] = {
            'instances': ec2_client.describe_instances()['Reservations'],
            'volumes': ec2_client.describe_volumes()['Volumes'],
            'subnets': ec2_client.describe_subnets()['Subnets'],
            'security_groups': ec2_client.describe_security_groups()['SecurityGroups'],
            'vpcs': ec2_client.describe_vpcs()['Vpcs'],
            'internet_gateways': ec2_client.describe_internet_gateways()['InternetGateways'],
        }

        rds_client = session.client('rds', region_name=region)
        resources['rds'] = {'instances': rds_client.describe_db_instances()[
            'DBInstances']}

        dynamodb_client = session.client('dynamodb', region_name=region)
        resources['dynamodb'] = {'tables': dynamodb_client.list_tables()[
            'TableNames']}

        lambda_client = session.client('lambda', region_name=region)
        resources['lambda'] = {'functions': lambda_client.list_functions()[
            'Functions']}

        elbv2_client = session.client('elbv2', region_name=region)
        resources['elbv2'] = {'load_balancers': elbv2_client.describe_load_balancers()[
            'LoadBalancers']}

        apigateway_client = session.client('apigateway', region_name=region)
        resources['apigateway'] = {'rest_apis': apigateway_client.get_rest_apis()[
            'items']}
    except Exception as e:
        print(f"Error retrieving resources in {region}: {e}")
    return resources


def get_global_resources(session):
    """ Retrieves global AWS resources. """
    global_resources = {}
    try:
        s3_client = session.client('s3')
        global_resources['s3'] = {
            'buckets': s3_client.list_buckets()['Buckets']}

        iam_client = session.client('iam')
        global_resources['iam'] = {'users': iam_client.list_users()['Users']}

        route53_client = session.client('route53')
        global_resources['route53'] = {
            'hosted_zones': route53_client.list_hosted_zones()['HostedZones']}
    except Exception as e:
        print(f"Error retrieving global resources: {e}")
    return global_resources


def main(profile_name, regions=None):
    session = boto3.Session(profile_name=profile_name)

    # Fetch all regions if none are provided
    if not regions:
        regions = [region['RegionName']
                   for region in session.client('ec2').describe_regions()['Regions']]
        print(f"No specific regions provided. Scanning all regions: {regions}")

    resources_by_region = {}

    # Fetch resources in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(
            get_aws_resources_by_region, region, session): region for region in regions}
        for future in as_completed(futures):
            region = futures[future]
            try:
                resources_by_region[region] = future.result()
            except Exception as e:
                print(f"Error retrieving resources for {region}: {e}")

    # Fetch global resources
    global_resources = get_global_resources(session)

    # Add global resources to the output
    resources_by_region['global'] = global_resources

    # Save resources to JSON
    with open('aws_resources.json', 'w') as f:
        json.dump(resources_by_region, f, indent=4, cls=DateTimeEncoder)

    print("AWS resources grouped by region saved to aws_resources.json")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AWS Resources Scanner")
    parser.add_argument(
        "profile_name", help="AWS profile name to use for scanning")
    parser.add_argument(
        "--regions", nargs="*", help="List of AWS regions to scan (optional). Defaults to all regions."
    )

    args = parser.parse_args()

    main(args.profile_name, args.regions)
