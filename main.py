#############################
 # @author René Lachmann
 # @email herr.rene.richter@gmail.com
 # @create date 2024-06-11 14:43:40
 # @modify date 2024-07-04 11:31:58
 # @desc [description]
############################

import argparse
from os import getcwd

from parameters import API_TOKEN, WORKSPACE_ID
from utility import get_and_store_docs


def main():
    parser = argparse.ArgumentParser(description='CLI tool for extracting all docs from a workspace.')
    parser.add_argument('-t', '--api_token', required=False, help='Your ClickUP API token. Usually in the format: "pk_yourID_tokenHash"')
    parser.add_argument('-w', '--workspace_id', required=False, help='Workspace ID')
    parser.add_argument('-u', '--user', required=False, help='User ID')
    parser.add_argument('-bp', '--base_path', required=False, help='Base Path to be used')
    parser.add_argument('-mp', '--media_path', required=False, help='Media Path to be used')
    
    
    args = parser.parse_args()
    if args.api_token is None:
        print("Using the API_TOKEN provided by local .env file.")
        args.api_token = API_TOKEN
    if args.workspace_id is None:
        print("Using the WORKSPACE_ID provided by local .env file.")
        args.workspace_id = WORKSPACE_ID
    if args.base_path is None:
        print(f"Not Base Path given, thus using the current working directory: {getcwd()}.")
        setattr(args,'base_path','/Users/tanoshimi/Downloads/testme')#getcwd())
    if args.media_path is None:
        media_path = 'media'
        print(f"Not Media Path given, thus using the sub-directory {media_path} of the current working directory.")
        setattr(args,'media_path',media_path)

    mstring,fname, url_path = get_and_store_docs(args.api_token,args.workspace_id,args.base_path,args.media_path, True,True,False)

if __name__ == '__main__':
    main()
    print("🤩Thank you for crawling your docs with this app.🤩")
