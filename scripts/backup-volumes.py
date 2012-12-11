#!/usr/bin/env python
# Copyright (c) 2012 Steffen Opel http://opelbrothers.net/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from botocross.ec2 import *
from pprint import pprint
import argparse
import boto
import boto.ec2
import botocross as bc
import logging

# configure command line argument parsing
parser = argparse.ArgumentParser(description='Backup EBS volumes in all/some available EC2 regions',
                                 parents=[bc.build_region_parser(), bc.build_filter_parser('EBS volume'), bc.build_common_parser()])
parser.add_argument("-d", "--description", help="A description for the EBS snapshot [default: <provided>]")
parser.add_argument("-br", "--backup_retention", type=int, default=1, help="The number of backups to retain (correlated via backup_set). [default: 1]")
parser.add_argument("-bs", "--backup_set", default=DEFAULT_BACKUP_SET, help="A backup set name (determines retention correlation). [default: 'default']")
parser.add_argument("-ns", "--no_origin_safeguard", action="store_true", help="Allow deletion of snapshots originating from other tools. [default: False]")
args = parser.parse_args()

# process common command line arguments
log = logging.getLogger('botocross')
bc.configure_logging(log, args.log_level)
credentials = bc.parse_credentials(args)
regions = bc.filter_regions(boto.ec2.regions(), args.region)
filter = bc.build_filter(args.filter, args.exclude)
log.info(args.resource_ids)

# execute business logic
log.info("Backing up EBS volumes:")

backup_set = args.backup_set if args.backup_set else DEFAULT_BACKUP_SET
log.debug(backup_set)

for region in regions:
    try:
        ec2 = boto.connect_ec2(region=region, **credentials)
        volumes = ec2.get_all_volumes(volume_ids=args.resource_ids, filters=filter['filters'])
        if filter['excludes']:
            exclusions = ec2.get_all_volumes(filters=filter['excludes'])
            volumes = bc.filter_list_by_attribute(volumes, exclusions, 'id')
        print region.name + ": " + str(len(volumes)) + " volumes"
        snapshots = create_snapshots(ec2, volumes, backup_set, args.description)
        # TODO: add support for 'awaiting' the smapshot creation result, once available.
        volume_ids = [volume.id for volume in volumes]
        expire_snapshots(ec2, volume_ids, backup_set, args.backup_retention, args.no_origin_safeguard)
    except boto.exception.BotoServerError, e:
        log.error(e.error_message)