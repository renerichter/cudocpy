#import json
# from cGPT4o
import os
import re
import shutil
import time

import markdownify
import requests

from parameters import BASE_URL_v2, BASE_URL_v3


def get_team_ids(api_token,verbose=True):
    url = BASE_URL_v2 + 'team'
    headers = {'Authorization': api_token}
    response = requests.get(url, headers=headers)
    data = {}
    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()['teams']
        # Print the team IDs and names
        if verbose:
            for team in data:
                print(f"Team ID: {team['id']}, Team Name: {team['name']}")
    else:
        print(f"Failed to get teams: {response.status_code}")
        print(response.json())
    return data

def get_space_ids(api_token,team_id):
    url = BASE_URL_v2 +"team/" + team_id + "/space"
    query = {"archived": "false"}
    headers = {"Authorization": api_token}
    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    spaces = [{'id':space['id'],'name':space['name']} for space in data['spaces']]
    return spaces

def get_docs_list(api_token,space_id):
    url = BASE_URL_v3+"workspaces/" + space_id + "/docs"
    #url = BASE_URL_v2 + f"space/{space_id}/doc"
    query = {}
    headers = {"Authorization": api_token}
    response = requests.get(url, headers=headers,params=query)
    data = response.json()['docs']
    return data

def get_pages_info(api_token,workspace_id,doc_id):
    url = BASE_URL_v3+"workspaces/" + workspace_id + "/docs/" + doc_id + "/pageListing"
    query = {"max_page_depth": "-1"}
    headers = {"Authorization": api_token}
    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    return data

def get_pages(api_token,workspace_id,doc_id):
    url = BASE_URL_v3+"workspaces/" + workspace_id + "/docs/" + doc_id + "/pages"
    query = {"max_page_depth": "-1","content_format": "text/md"}
    headers = {"Authorization": api_token}
    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    return data

def get_page_content(api_token,workspace_id,doc_id,page_id):
    url = "https://api.clickup.com/api/v3/workspaces/" + workspace_id + "/docs/" + doc_id + "/pages/" + page_id
    query = {"content_format": "text/md"}
    headers = {"Authorization": api_token}
    response = requests.get(url, headers=headers, params=query)
    data = response.json()
    return data


def save_doc_as_markdown(doc, folder_path):
    doc_content = markdownify.markdownify(doc['content'], heading_style="ATX")
    doc_path = os.path.join(folder_path, f"{doc['name']}.md")
    with open(doc_path, 'w', encoding='utf-8') as file:
        file.write(doc_content)
    
def remove_directory(base_path):
    if os.path.exists(base_path):
        shutil.rmtree(base_path)
    else:
        print(f"The directory {base_path} does not exist.")

def init(base_path,media_path,clear_base=False):
    if clear_base:
        remove_directory(base_path)
        os.makedirs(base_path)
    os.chdir(base_path)
    os.makedirs(media_path,exist_ok=True)
    filename = []
    url_to_local_path = []
    modified_string = []
    return modified_string,filename,url_to_local_path,

def download_and_replace_urls(input_string, storage_path, verbose=False):
    # Regular expression to find URLs
    url_pattern = re.compile(r'https://t\d+\.p\.clickup-attachments\.com/[^)]+')
    
    # Find all URLs in the input string
    urls = url_pattern.findall(input_string)
    
    url_to_local_path = []
    modified_string = input_string
    
    for i, url in enumerate(urls):
        # Generate a new file name using the current system time
        base_name = time.strftime("%Y%m%d%H%M%S")
        file_extension = url.split('.')[-1]
        local_file_name = f"{base_name}.{file_extension}"
        local_file_path = os.path.join(storage_path, local_file_name)

        # Check if the file already exists and modify the name if necessary
        counter = 1
        while os.path.exists(local_file_path):
            local_file_name = f"{base_name}_{counter:03d}.{file_extension}"
            local_file_path = os.path.join(storage_path, local_file_name)
            counter += 1
        
        # Download the file
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_file_path, 'wb') as file:
                file.write(response.content)
            
            # Replace URL in the string with the local file path
            modified_string = modified_string.replace(url, local_file_path)
            url_to_local_path.append((url, local_file_path))
        else:
            print(f"Failed to download {url}")
    if verbose: print("DOWNLOAD: files for urls downloaded, renamed and stored.")
    return modified_string, url_to_local_path

def construct_filename(page,filename_prefix='',verbose=False):
    # Generate the filename
    # Remove non-standard UTF-8 characters and replace spaces with underscores
    name_cleaned = re.sub(r'[^\w\s]', '', page['name'])  # Remove non-alphanumeric characters
    name_cleaned = re.sub(r'\s+', '_', name_cleaned)      # Replace spaces with underscores
    
    filename = filename_prefix+f"{name_cleaned}.md"
    if verbose: print(f"CREATE: Filename is {filename}.")
    return filename

def create_markdown_string(page,verbose=False):
    # Create the meta-value section
    meta_values = [
        'id', 'doc_id', 'workspace_id', 'name', 'date_created',
        'date_updated', 'creator_id', 'date_edited','edited_by'
    ]
    meta_section = "---\n"+"\n".join([f"{key}: {page[key]}" for key in meta_values if key in page])+"\n---\n"

    # Prepare the content section
    content_section = page['content']

    # Create the full markdown string
    markdown_string = f"{meta_section}\n\n\n{content_section}"
    
    if verbose: print(f"CREATE: Markdown string created.")

    return markdown_string

def store_markdown(text,file_path,verbose=False):
    with open(file_path,"w",encoding="utf-8") as f:
        f.write(text)
    if verbose: print(f"STORE: into file {file_path} done.")

def traverse_pages(page,media_path,filename_prefix='',modified_string=[],filename=[],url_to_local_path=[], verbose=False,overwrite_existing=False):
    filename_new = construct_filename(page,filename_prefix,verbose)

    # only create new file if not existing or if overwriting is ok
    if not os.path.exists(filename_new) or overwrite_existing:
        # format page['content'] to markdown with meta info in the beginning
        markdown_string = create_markdown_string(page,verbose)
        # download, replace and store the files
        modified_string_new, url_to_local_path_new=download_and_replace_urls(markdown_string,media_path,verbose)
        # save markdown
        store_markdown(modified_string_new,filename_new,verbose)

        # add new contents to list for analysis
        filename.append(filename_new)
        url_to_local_path.append(url_to_local_path_new)
        modified_string.append(modified_string_new)

    # anyways traverse subpages
    if 'pages' in page: 
        for k,subpage in enumerate(page['pages']):
            print(f"----->({k}/{len(page['pages'])}): Sub-Page traversal started.")
            modified_string,filename,url_to_local_path=traverse_pages(subpage,media_path,f"{filename_new[:-3]}-{k}-",modified_string,filename,url_to_local_path,verbose,overwrite_existing)
    if verbose: 
        if not os.path.exists(filename_new) or overwrite_existing: print(f"TRAVERSE: of page {page['name']} done.")
        else: print("Path exists and shall not be overwritten.")
    return modified_string, filename, url_to_local_path


def get_and_store_docs(api_token,workspace_id,base_path,media_path, clear_base=False,verbose=False,overwrite_existing=False):
    mstring,fname,url_path = init(base_path,media_path,clear_base)
    docs_list = get_docs_list(api_token,workspace_id)
    if verbose: print(f"START: travelsal of {workspace_id=} with {len(docs_list)} docs started.")
    for i,doc in enumerate(docs_list):
        pages=get_pages(api_token,workspace_id,doc['id'])
        if verbose: print(f"-->({i}/{len(docs_list)}): Doc traversal started.")
        for j,page in enumerate(pages):
            if verbose: print(f"---->({j}/{len(pages)}): Page traversal started.")
            mstring_new,fname_new,url_path_new = traverse_pages(page,media_path,'',mstring,fname,url_path,verbose=verbose,overwrite_existing=overwrite_existing)
            
    return mstring,fname, url_path