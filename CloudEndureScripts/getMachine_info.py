#Fetch instance ID and Name
import requests
import os

def instanceData(args):
    url = 'http://169.254.169.254/latest/meta-data/instance-id'
    r = requests.get(url)
    with open('instanceid.txt', 'wb') as f:
        f.write(r.content) # Retrieve HTTP meta-data

    f = open("instanceid.txt", "r")
    id = f.read()
    print id

    cmd="aws ec2 describe-instances --instance-ids " + id + " --region us-east-1  --query \"Reservations[*].Instances[0].{Name:Tags[?Key=='Name']|[0].Value}\" --output text > instancename.txt"
    data = os.system(cmd)

    f = open("instancename.txt", "r")
    instance_name = f.read()
    return instance_name
