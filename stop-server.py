import boto3
import sys

def main():
    if len(sys.argv) < 2:
        print('You must provide the instance ID to stop')
        print('\t {} <instanceID>'.format(sys.argv[0]))
        sys.exit(1)

    instance_id = sys.argv[1]
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    instance.stop()
    print('Stopping {}...'.format(instance_id))
    
    instance.wait_until_stopped()
    print('Stopped {}...'.format(instance_id))

if __name__ == '__main__':
    main()
