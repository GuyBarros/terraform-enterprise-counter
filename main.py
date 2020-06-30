#!/usr/bin/env python
#this is a simple Organization, Workspaces and run counter for Terraform Enterprise
import json
import requests
import os
import pprint
import pandas
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
    todo_item = resp.json()['data']
    return len(todo_item)    
    

def getOrganizations():
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    return [ item['id'] for item in todo_item ]

def getOrgObj():
    result = []
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    for item in todo_item:
         info = { 
         'name': item['id'],
         'total_runs': getRunsTotalCount(item['id']),
         'workspace_count': getWorkspaceCount(item['id']),
         'workspaces': getWorkspaceInfo(item['id'])
         }
         result.append(info)
    return result    

def getWorkspaceInfo(organisation):
    resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    return [ item['id'] for item in todo_item ]

def getWorkspaceCount(organisation):
    resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    return len(todo_item)

def getRunsCount(workspace_id):
    resp = requests.get(TFE_ADDR+f'/api/v2/workspaces/{workspace_id}/runs', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
        return ""
    todo_item = resp.json()['data']
    pp.pprint(f"Run count for {workspace_id}: {len(todo_item)}")
    return len(todo_item)

def getRunsTotalCount(organisation):
    total_runs = 0
    todo_item = getWorkspaceInfo(organisation)
    for item in todo_item:
        total_runs +=  getRunsCount(item)
    pp.pprint(f"Total runs for {organisation}: {total_runs}")    
    return total_runs     

#Main just has the calls to the above methods, comment out as needed
def main():
    result = getOrgObj()
    totalWorkspaces = 0
    totalRuns = 0
    for org in result:
    #    pp.pprint(f"{org['name']} total workspaces: {org['workspace_count']} total runs: {org['total_runs']}")
        totalWorkspaces += org['workspace_count']
        totalRuns += org['total_runs']
    data = pandas.DataFrame(result)
    pp.pprint(data)
    pp.pprint(f"Total workspaces count: {totalWorkspaces}")
    pp.pprint(f"Total runs count: {totalRuns}")

if __name__ == '__main__':
    main()
