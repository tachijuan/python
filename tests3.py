import boto
import boto.s3.connection

ak = 'c3BlY3RyYQ=='
sk = 'bjQpZe2b'

c = boto.connect_s3(aws_access_key_id = ak, aws_secret_access_key = sk, host = '10.10.1.237',
                    is_secure=False, calling_format = boto.s3.connection.OrdinaryCallingFormat())

print c

for b in c.get_all_buckets():
    print "%s\t%s" % (b.name,b.creation_date)

