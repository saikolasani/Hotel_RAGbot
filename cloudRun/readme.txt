To deploy your Flask app with Cloud Run, you need to containerize it, build a Docker image, and then deploy that image to Cloud Run. Here's how you can do it:

Step1: Containerize your Flask app:
        Create a Dockerfile in the root directory of your project. Here's an example Dockerfile for your Flask app:
        # Use the official Python image as the base image
Step2: Build the Docker image:
        Open a terminal and navigate to the directory where your Dockerfile is located. Then, run the following command to build the Docker image:
        #docker build -t htlragbot-flask-app-image .
Step3: Tag the Docker image:
        Tag the Docker image with the appropriate registry name. You can use Google Container Registry (GCR) as the registry. Replace [PROJECT_ID] with your Google Cloud project ID and [REGION] with the desired region:
        #docker tag my-flask-app-image gcr.io/[PROJECT_ID]/my-flask-app-image:latest
Step4: Authenticate to your project
        -gcloud auth login
        -gcloud config set project PROJECT_ID
Step5: Push the Docker image to the container registry:
        #docker push gcr.io/[PROJECT_ID]/my-flask-app-image:latest
Step6: Deploy the Docker image to Cloud Run
        #gcloud run deploy my-flask-app \
            --image gcr.io/[PROJECT_ID]/my-flask-app-image:latest \
            --platform managed \
            --region [REGION] \
            --allow-unauthenticated




