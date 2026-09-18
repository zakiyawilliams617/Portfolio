# EC2 Instance Auditor — Pseudocode & Notes

## Stage 1: List all EC2 instances
1. Import the boto3 library
2. Create an EC2 client (this is how we talk to AWS's EC2 API)
3. Call describe_instances() to get all instance data from AWS
   -> this returns a big nested structure: a list of "Reservations",
      and each Reservation contains a list of "Instances"

4. FOR each reservation IN the list of reservations:
     FOR each instance IN that reservation's list of instances:
         - get the instance's ID
         - get the instance's state (e.g. "running", "stopped")
         - get the instance's tags (or None, if it has no tags)
         - print the ID, state, and tags

**Code mapping:**

| Pseudocode line | Actual code |
|---|---|
| Import boto3 | `import boto3` |
| Create EC2 client | `ec2 = boto3.client('ec2')` |
| Call describe_instances() | `response = ec2.describe_instances()` |
| FOR each reservation | `for reservation in response['Reservations']:` |
| FOR each instance | `for instance in reservation['Instances']:` |
| get instance ID | `instance_id = instance['InstanceId']` |
| get state | `state = instance['State']['Name']` |
| get tags | `tags = instance.get('Tags')` |
| print | `print(instance_id, state, tags)` |

**Key learning:** if an instance has no tags, the `Tags` key doesn't exist
on the dict at all — `.get('Tags')` returns `None`. Using `instance['Tags']`
directly would throw a `KeyError` on any untagged instance.

## Stage 2: Flag missing required tags
**Note:** in a real AWS account, there will be more instances way more, with more standardized tag sets likely enforced by policy. Common tags(environment, ownwer/team, project/costcenter, name, application, managedby). However, an unmanaged AWS account like mine is a realistic starting point to introduce tagging but will need to updated. 
For each instance we already found in Stage 1:

1. Define REQUIRED_TAGS = ['Name', 'Environment', 'Owner']
2. For each instance:
   - If tags is None, treat it as an empty list
   - Build existing_keys: loop through tags, pull out each tag's 'Key', append to a list
   - Build missing_tags: loop through REQUIRED_TAGS, check if each one is NOT in existing_keys,
     if so, append it to missing_tags
   - Print instance_id and missing_tags

**Key learning:** the `in` / `not in` operators check membership in a list —
`x in my_list` is True if x exists anywhere in my_list.

## Stage 3: Idle Detection via CloudWatch

**Note:** all 8 of my instances are currently stopped. The CloudWatch metrics like CPU utilization only works for instances that are running. A stopped instance won't produce any metrics. I have to think through how to ensure this idle detection is still useful. 
        - running instances: will check CloudWatch for average CPU usage based on a set timeframe, then flag as idle if below a set threshold 
        - stopped instacnces: flagged as stopped, review for termination. A stopped instance is a cost and governane concern (might have an EBS volume attached racking up storage costs).

For each instance:
  IF state == 'running':
      - query CloudWatch for average CPUUtilization over the last N days
      - IF average CPU is below threshold (e.g. 5%):
          - flag as "idle"
  ELIF state == 'stopped':
      - flag as "stopped — review for termination"

## Stage 4: Reporting

For each instance:
  1. Determine a "status" string based on state:
     - if stopped -> status = "stopped - review for termination"
     - if running and idle -> status = "idle - average CPU below 5%"
     - if running and active -> status = "active - X% average CPU"
     - if running with no CloudWatch data yet -> status = "running - no data yet"

  2. Build a "missing_tags" summary string:
     - if missing_tags list is empty -> "No missing tags"
     - if missing_tags list has items -> "Missing tags: Name, Environment, Owner" (comma-joined)

  3. Print one combined line: instance_id | status | tag summary
