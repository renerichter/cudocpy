#############################
 # @author René Lachmann
 # @email herr.rene.richter@gmail.com
 # @create date 2024-07-04 10:18:02
 # @modify date 2024-07-04 10:27:23
 # @desc [description]
############################

from os import getenv as ge

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
API_TOKEN = ge('API_TOKEN')
WORKSPACE_ID=ge("WORKSPACE_ID")

# Base URL for ClickUp API
BASE_URL_v2 = 'https://api.clickup.com/api/v2/'
BASE_URL_v3 = 'https://api.clickup.com/api/v3/'