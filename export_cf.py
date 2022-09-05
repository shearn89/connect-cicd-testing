# © 2022 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.

# This AWS Content is provided subject to the terms of the AWS Customer Agreement
# available at http://aws.amazon.com/agreement or other written agreement between
# Customer and either Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

import argparse # argparse is a built in python package, we add it with an import statement
import boto3 # AWS API
import botocore.exceptions # AWS API Exceptions
from botocore.config import Config

config = Config(
    retries = {
        'max_attempts': 5,
        'mode': 'adaptive'
    }
)
client = boto3.client('connect', config=config)

def list_contact_flows(**kwargs):
    """ Retrieves all contact flows from the Amazon Connect instance """
    items = {}
    print("Exporting contact flows")
    try:
        extraArgs = kwargs
        while True:
            response = client.list_contact_flows(**extraArgs)
            print (response)
            for item in response['ContactFlowSummaryList']:
                items[item['Id']] = item
            if "NextToken" in response:
                extraArgs["NextToken"] = response["NextToken"]
            else:
                break    
        print("Retrieved %d contact flows" % len(items))
        return items
    except botocore.exceptions.ClientError as error:
        raise error

if __name__=="__main__":
    print("export_cf.py - Utility to export Amazon Connect contact flows")
    # Define the parser variable to equal argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="Exports Users from Amazon Connect.")

    # Optional CLI argument is the Amazon Connect Instance ID - for testing purposes
    parser.add_argument(
        '--instance-id',
        dest="InstanceId",
        type=str,
        help="The Amazon Connect Instance ID you would like to export contact flows from",
        required=False
        )
    # This will inspect the command line, convert each argument to the appropriate type and then invoke the appropriate action.
    args = parser.parse_args()
    print("args: ", args)
    if args.InstanceId is not None:
       contact_flows = list_contact_flows(**vars(args))
       print(contact_flows)
    else:
        print("Amazon Connect Instance ID form env variables - TBC")