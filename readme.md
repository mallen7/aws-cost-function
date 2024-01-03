# aws-cost-function
This is the unpackaged version of this function for further development.

## To package

### Create a Virtual Environment:

- Run python3 -m venv mylambdaenv to create a virtual environment.
- Activate the environment:
On Linux/macOS: source mylambdaenv/bin/activate
On Windows: mylambdaenv\Scripts\activate

### Install Dependencies:

Inside the virtual environment, install the required libraries: pip install boto3 requests.
Prepare Your Package:

- Deactivate the virtual environment (deactivate).
-  Navigate to the virtual environment's lib directory (mylambdaenv/lib/python3.x/site-packages/).
- Copy all the contents from this folder (except your script) to a new folder, e.g., lambda_package.
- Place your main.py script inside the lambda_package folder.

### Create a ZIP Archive:

- Zip the contents of lambda_package, not the folder itself.
    On Linux/macOS: zip -r ../my_lambda_function.zip . (run inside lambda_package folder).
    On Windows: You can use a file archiver like 7-Zip.

## Upload the ZIP to AWS Lambda

### Open AWS Management Console:

### Create a New Lambda Function:

- Click on "Create function".
- Choose "Author from scratch".
- Enter the function name.
- Choose the runtime as Python 3.x.
- Set the role with the necessary permissions (for AWS Cost Explorer and Secrets Manager).
- Upload Your ZIP File:

In the "Function code" section, choose "Upload a .zip file" from the "Code entry type" dropdown.
Upload the ZIP file you created.

### Set the Handler:

Make sure the handler is set to main.lambda_handler (assuming your function is named lambda_handler in main.py).


## Test the Lambda Function

### Configure a Test Event:

- In the AWS Lambda console, navigate to your function.
- Click on "Test" near the top of the page.
- Configure a new test event – you can use the default template since your script does not rely on the event object.
- Invoke the Function:

- Click "Test" to invoke your Lambda function with the test event.
- Review the Results:

After the function execution, you will see the execution result and the function logs.
Check for any errors and ensure that the function is executing as expected.
