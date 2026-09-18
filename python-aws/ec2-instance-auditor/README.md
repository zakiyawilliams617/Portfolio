# EC2 Instance Auditor

A Python CLI tool that audits an AWS account's EC2 instances for common governance issues: missing required tags, idle running instances, and long-stopped instances that may be candidates for termination.

Built as a foundational AWS automation project to practice boto3, IAM, EC2, and CloudWatch and to solve a real, common problem: untagged and idle resources quietly driving up cloud costs.

## What It Does

| Check | Description |
|---|---|
| **Tag Compliance** | Flags any instance missing required tags (`Name`, `Environment`, `Owner`) |
| **Idle Detection** | Queries CloudWatch for average CPU utilization over the last 14 days and flags running instances averaging below 5% CPU |
| **Stopped Instance Review** | Flags any stopped instance for review/termination (stopped instances can still incur EBS storage costs) |
| **Reporting** | Outputs a clean console report and a CSV file (`ec2_audit_report.csv`) for sharing or further analysis |

## Example Output

```
i-080acfd4a694413e9 | stopped - review for termination | Environment, Owner
i-017af1061a8bf32b2 | idle - average CPU below 5% | Name, Environment, Owner
```

## How It Works

1. Calls `describe_instances()` to pull every EC2 instance in the account
2. For each instance, checks its tags against a required tags list
3. For running instances, queries CloudWatch's `CPUUtilization` metric (14 day window, daily) and flags anything averaging below a 5% threshold
4. For stopped instances, flags them directly (no CPU data to check)
5. Writes a combined status + tag report to both the console and a CSV file

## Tech Used

- **boto3** — AWS SDK for Python (EC2 and CloudWatch clients)
- **AWS IAM** — CLI authentication via access keys
- **AWS CloudWatch** — CPU utilization metrics
- Python's built in `csv` module for report export

## Setup

```bash
# Clone this repo, then:
cd ec2-instance-auditor

python3 -m venv venv
source venv/bin/activate
pip install boto3

# Requires AWS CLI configured with valid credentials:
aws configure

python3 ec2_auditor.py
```

Running the script generates `ec2_audit_report.csv` in the same folder (not committed to this repo, since it reflects live account data).

## Notes

This was built in stages, using pseudocode before each part of the logic, see `pseudocode.md` for the full design process, including edge cases handled along the way (instances with no tags at all, launched instances with no CloudWatch data yet, avoiding stale variable bugs when branching on instance state).

## Possible Extensions

- Auto remediation (stop confirmed idle instances automatically, with a dry run/safe mode)
- SNS or Slack notification on flagged findings
- Configurable required tags list and idle threshold via commandline flags