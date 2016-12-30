import boto3
import sys

def main():
    if len(sys.argv) < 3:
        print('You must provide the instance ID to start and the hosted zone to associate')
        print('\tpython {} <instanceID> <hostedZoneId>'.format(sys.argv[0]))
        sys.exit(1)

    instance_id = sys.argv[1]
    hosted_zone_id = sys.argv[2]

    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    instance.start()
    print('Starting {}...'.format(instance_id))

    instance.wait_until_running()
    print('Started {}...'.format(instance_id))

    ip = instance.public_ip_address
    print('Associating `{}` with `backwardsgate.com`...'.format(ip))

    route_client = boto3.client('route53')
    route_client.change_resource_record_sets(
        HostedZoneId = hosted_zone_id,
        ChangeBatch = {
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': 'backwardsgate.com.',
                        'Type': 'A',
                        'ResourceRecords': [
                            {
                                'Value': ip
                            }
                        ],
                        'TTL': 300
                    }
                }
            ]
        }
    )
    print('Associated `{}` with `backwardsgate.com`...'.format(ip))

if __name__ == '__main__':
    main()
