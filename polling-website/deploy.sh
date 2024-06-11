#!/bin/bash

# Variables
RESOURCE_GROUP="MyResourceGroup"
LOCATION="eastus"
POSTGRES_SERVER_NAME="mydemoserver"
POSTGRES_DB_NAME="polling_db"
POSTGRES_ADMIN_USER="myadmin"
POSTGRES_ADMIN_PASSWORD="mypassword"
APP_SERVICE_PLAN="MyAppServicePlan"
WEB_APP_NAME="MyWebAppName"
STORAGE_ACCOUNT_NAME="mystorageaccount"
STORAGE_CONTAINER_NAME="uploads"

# Login to Azure
az login

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create PostgreSQL Server
az postgres server create \
    --resource-group $RESOURCE_GROUP \
    --name $POSTGRES_SERVER_NAME \
    --location $LOCATION \
    --admin-user $POSTGRES_ADMIN_USER \
    --admin-password $POSTGRES_ADMIN_PASSWORD \
    --sku-name B_Gen5_1

# Configure PostgreSQL Server Firewall to allow Azure services and local IP
az postgres server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --server $POSTGRES_SERVER_NAME \
    --name AllowAzureIPs \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0

az postgres server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --server $POSTGRES_SERVER_NAME \
    --name AllowLocalIP \
    --start-ip-address YOUR_LOCAL_IP \
    --end-ip-address YOUR_LOCAL_IP

# Create PostgreSQL Database
az postgres db create \
    --resource-group $RESOURCE_GROUP \
    --server-name $POSTGRES_SERVER_NAME \
    --name $POSTGRES_DB_NAME

# Create App Service Plan
az appservice plan create \
    --name $APP_SERVICE_PLAN \
    --resource-group $RESOURCE_GROUP \
    --sku FREE

# Create Web App
az webapp create \
    --resource-group $RESOURCE_GROUP \
    --plan $APP_SERVICE_PLAN \
    --name $WEB_APP_NAME \
    --runtime "PYTHON:3.8"

# Create Storage Account
az storage account create \
    --name $STORAGE_ACCOUNT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku Standard_LRS

# Create Storage Container
az storage container create \
    --account-name $STORAGE_ACCOUNT_NAME \
    --name $STORAGE_CONTAINER_NAME

# Get Storage Account Connection String
STORAGE_CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query connectionString --output tsv)

# Set Environment Variables for Web App
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $WEB_APP_NAME \
    --settings SECRET_KEY='your_secret_key' \
                DB_HOST="${POSTGRES_SERVER_NAME}.postgres.database.azure.com" \
                DB_PORT='5432' \
                DB_NAME=$POSTGRES_DB_NAME \
                DB_USER="${POSTGRES_ADMIN_USER}@${POSTGRES_SERVER_NAME}" \
                DB_PASSWORD=$POSTGRES_ADMIN_PASSWORD \
                AZURE_STORAGE_CONNECTION_STRING=$STORAGE_CONNECTION_STRING

# Deploy code to Azure (assumes you have set up local git and committed your changes)
git init
git add .
git commit -m "Initial commit"
az webapp deployment source config-local-git --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query url --output tsv
git remote add azure $(az webapp deployment source config-local-git --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query url --output tsv)
git push azure master
