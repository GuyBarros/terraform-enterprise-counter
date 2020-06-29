#!/usr/bin/env python
#this is a simple Organization, Workspaces and run counter for Terraform Enterprise
import json
import requests
import os
import pprint
pp = pprint.PrettyPrinter()

TFE_ADDR =  os.environ.get('TFE_ADDR', 'https://app.terraform.io')
TFE_API_TOKEN =  os.environ.get('TFE_API_TOKEN', '')


headers = {
    'Content-Type': 'application/vnd.api+json',
    'Authorization': f"Bearer {TFE_API_TOKEN}"  
    }

def getOrgCount():
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    # pp.pprint(f"Response: {resp.json()}")
    todo_item = resp.json()['data']
    return len(todo_item)    
    

def getOrganisations():
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    return [ item['id'] for item in todo_item ]

def getOrgObj():
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    return [ item['id'] for item in todo_item ]    

def getWorkspaceInfo(organisation):
    resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    # pp.pprint(f"Response: {todo_item}")
    for item in todo_item:
         pp.pprint(f"Found Org: {item['attributes']['name']}")
    # return [ item['id'] for item in todo_item ]

def getWorkspaceCount(organisation):
    resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    return len(todo_item)
    #pp.pprint(f"Workspace count for {organisation}: {len(todo_item)}")

def getRuns(workspace_id):
    # http://app.terraform.io/api/v2/workspaces/ws-6LvLRx7uFoDD7Znf/runs
    resp = requests.get(TFE_ADDR+f'/api/v2/workspaces/{workspace_id}/runs', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    pp.pprint(f"Run count for {workspace_id}: {len(todo_item)}")

#Main just has the calls to the above methods, comment out as needed
def main():
    totalWorkspaces = 0
    orgs = getOrganisations()
    # info = {[{
    #    name: EMEA_SE_PLAYGROUND 
    #    runs: 0,
    #    count: 0,
    #    workspaces: []
    #    },]
    # }
        for org in orgs:
       totalWorkspaces += getWorkspaceCount(org)
       pp.pprint(f"Workspace count for {org}: {getWorkspaceCount(org)}")
   
    totalOrgs = getOrgCount()
    pp.pprint(f"Total Organisation count: {totalOrgs} ")
    pp.pprint(f"Total Workspace count: {totalWorkspaces} ")



if __name__ == '__main__':
    main()
