# Variables
RESOURCE_GROUP="llm-hack-rg"
STORAGE_ACCOUNT="llmhackstorage$RANDOM"
FUNCTION_APP="llm-azure-hackathon"
LOCATION="northeurope"

# Create resource group
# az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account (must be globally unique)
# az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS

# Create function app
# az functionapp create \
#   --resource-group $RESOURCE_GROUP \
#   --consumption-plan-location $LOCATION \
#   --runtime python \
#   --runtime-version 3.12 \
#   --functions-version 4 \
#   --name $FUNCTION_APP \
#   --storage-account $STORAGE_ACCOUNT


# deploy the app 

# zip the app exclude git and resource.bash and .env
zip -r functionapp.zip . -x "*.git*" -x "resource.bash" -x ".env"

az functionapp deployment source config-zip \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --src functionapp.zip