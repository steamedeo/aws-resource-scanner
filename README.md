# AWS Resource Scanner

A Python script to scan and list AWS resources by region and globally, using a specified AWS profile.

## Features

- Scans all AWS regions or a specific list of regions.
- Retrieves resources from EC2, RDS, DynamoDB, Lambda, and more.
- Fetches global resources like S3 buckets, IAM users, and Route 53 hosted zones.
- Outputs results in a structured JSON file.

## Prerequisites

1. **Install Python 3.8+**  
   Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

2. **Install AWS CLI**

   - Download and install the AWS CLI from [AWS CLI official documentation](https://aws.amazon.com/cli/).
   - Verify the installation:
     ```bash
     aws --version
     ```
     You should see a version number, e.g., `aws-cli/2.x.x`.

3. **Configure AWS CLI**

   - Set up your AWS CLI with profiles:
     ```bash
     aws configure --profile <profile-name>
     ```
   - Provide your access key, secret key, default region, and output format when prompted.

4. **Install Dependencies**
   - Install the `boto3` library using pip:
     ```bash
     pip install boto3
     ```

## Installation

```bash
git clone https://github.com/yourusername/aws-resource-scanner.git
cd aws-resource-scanner
pip install -r requirements.txt
```

## Usage

- Scan all regions

```bash
python aws-scanner.py <aws-profile-name>
```

- Scan specific regions

```bash
python aws-scanner.py <aws-profile-name> --regions us-east-1 eu-west-1
```

## Output

The script saves a JSON file named aws_resources.json with details of the resources grouped by region.

## License

This project is licensed under the MIT License.
