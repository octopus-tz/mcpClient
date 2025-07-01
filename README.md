# mcpClient

Instructions

Build container image
docker build -t my-lambda-hello-world .
484907496385.dkr.ecr.us-east-1.amazonaws.com/mcp
docker build -t my-image .
Tag it with the ECR repo URL:

bash
Copy
Edit
docker tag my-image:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/my-lambda-image:latest

Account ID : 484907496385
Region: us-east-1
Install aws cli https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
aws –version
aws ecr describe-repositories --repository-names my-lambda-hello-world --region us-east-1
aws ecr create-repository --repository-name my-lambda-hello-world --region us-east-1
aws ecr describe-repositories --repository-names my-lambda-hello-world --region us-east-1
{
    "repositories": [
        {
            "repositoryArn": "arn:aws:ecr:us-east-1:484907496385:repository/my-lambda-hello-world",
            "registryId": "484907496385",
            "repositoryName": "my-lambda-hello-world",
            "repositoryUri": "484907496385.dkr.ecr.us-east-1.amazonaws.com/my-lambda-hello-world",
            "createdAt": "2025-06-26T14:08:11.743000+03:00",
            "imageTagMutability": "MUTABLE",
            "imageScanningConfiguration": {
                "scanOnPush": false
            },
            "encryptionConfiguration": {
                "encryptionType": "AES256"
            }
        }
    ]
}
docker push 484907496385.dkr.ecr.us-east-1.amazonaws.com/my-lambda-hello-world:latest
Image is pushed in the repository
--provenance=false

