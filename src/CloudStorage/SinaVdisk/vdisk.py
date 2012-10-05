import argparse

parser=argparse.ArgumentParser(description="Use command line to control vdisk")

group=parser.add_mutually_exclusive_group()
group.add_argument("--upload","-U",help="upload a file")
group.add_argument("--delete","-D",help="delete a file")
group.add_argument("--query","-Q",help="query file by key word")

args=parser.parse_args()

if args.upload:
    print args.upload
elif args.delete:
    print args.delete
elif args.query:
    print args.query
else:
    pass
