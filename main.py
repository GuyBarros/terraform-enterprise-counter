#!/usr/bin/env python
#this is a simple Organization, Workspaces and run counter for Terraform Enterprise
import json
import requests
import os
import pprint
import pandas
import time
from datetime import datetime
from datetime import date
from yaspin import yaspin
pp = pprint.PrettyPrinter()

TFE_ADDR =  os.environ.get('TFE_ADDR', 'https://app.terraform.io')
TFE_API_TOKEN =  os.environ.get('TFE_API_TOKEN', '')
TFE_SITE_ADMIN =  os.environ.get('TFE_SITE_ADMIN', 'false')
TFE_PAGE_COUNT =  os.environ.get('TFE_PAGE_COUNT', 100)
TFE_FILTER_START_DATE = os.environ.get('TFE_FILTER_START_DATE', '31.12.2020')
TFE_FILTER_END_DATE = os.environ.get('TFE_FILTER_END_DATE', date.today().strftime('%d.%m.%Y'))

date_start = datetime.strptime(TFE_FILTER_START_DATE, '%d.%m.%Y')
date_end = datetime.strptime(TFE_FILTER_END_DATE, '%d.%m.%Y')

headers = {
    'Content-Type': 'application/vnd.api+json',
    'Authorization': f"Bearer {TFE_API_TOKEN}"  
    }

def getOrgCount():
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while counting Organizations: {resp}")
        return ""
    todo_item = resp.json()['data']
    return len(todo_item)    
    

def getOrganizations():
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while getting Organizations: {resp}")
        return ""
    todo_item = resp.json()['data']
    return [ item['id'] for item in todo_item ]

@yaspin(text="Loading...")
def getOrgObj():
    result = []
    resp = requests.get(TFE_ADDR+'/api/v2/organizations', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while creating Org Object: {resp}")
        return ""
    todo_item = resp.json()['data']
    for item in todo_item:
         info = { 
         'name': item['id'],
         'total_runs': getRunsTotalCount(item['id']),
         'total_applies': getAppliesTotalCount(item['id']),
         'workspace_count': getWorkspaceCount(item['id']),
         'workspaces': getWorkspaceInfo(item['id'])
         }
         result.append(info)
    return result    

def getWorkspaceInfo(organisation):
    page = 1
    retorno = []
    resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces?page[size]=100&page[number]={page}', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while getting workspace info: {resp}")
        return ""
    metdata =   resp.json()['meta']['pagination']
    current_page = metdata["current-page"]
    total_pages = metdata["total-pages"]
    while page <= total_pages:
        todo_item = resp.json()['data']
        metdata =   resp.json()['meta']['pagination']
        current_page = metdata["current-page"]
        for item in todo_item:
            retorno.append(item['id'])
        page += 1
        resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces?page[size]=100&page[number]={page}', headers=headers )
    return retorno

def getWorkspaceCount(organisation):
    page = 1
    retorno = []
    resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces?page[size]=100&page[number]={page}', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while counting workspaces: {resp}")
        return ""
    metdata =   resp.json()['meta']['pagination']
    current_page = metdata["current-page"]
    total_pages = metdata["total-pages"]
    while page <= total_pages:
        todo_item = resp.json()['data']
        metdata =   resp.json()['meta']['pagination']
        current_page = metdata["current-page"]
        for item in todo_item:
            retorno.append(item['id'])
        page += 1
        resp = requests.get(TFE_ADDR+f'/api/v2/organizations/{organisation}/workspaces?page[size]=100&page[number]={page}', headers=headers )
    return len(retorno)

def getRunsCount(workspace_id):
    page = 1
    retorno = []
    resp = requests.get(TFE_ADDR+f'/api/v2/workspaces/{workspace_id}/runs?page[size]=100&page[number]={page}', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while counting runs: {resp}")
        return ""
    todo_item = resp.json()['data']
    metdata =   resp.json()['meta']['pagination']
    current_page = metdata["current-page"]
    total_pages = metdata["total-pages"]
    while page <= total_pages:
        todo_item = resp.json()['data']
        metdata =   resp.json()['meta']['pagination']
        current_page = metdata["current-page"]
        for item in todo_item:
            creation_date = datetime.strptime(item['attributes']['created-at'][:10], "%Y-%m-%d")
            if date_start < creation_date and creation_date <= date_end : retorno.append(item['id'])
        page += 1
        resp = requests.get(TFE_ADDR+f'/api/v2/workspaces/{workspace_id}/runs?page[size]=100&page[number]={page}', headers=headers )
    return len(retorno)

def getAppliesCount(workspace_id):
    page = 1
    retorno = []
    resp = requests.get(TFE_ADDR+f'/api/v2/workspaces/{workspace_id}/runs?page[size]=100&page[number]={page}', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong while counting applies: {resp}")
        return ""
    todo_item = resp.json()['data']
    metdata =   resp.json()['meta']['pagination']
    current_page = metdata["current-page"]
    total_pages = metdata["total-pages"]
    while page <= total_pages:
        todo_item = resp.json()['data']
        metdata =   resp.json()['meta']['pagination']
        current_page = metdata["current-page"]
        for item in todo_item:
            creation_date = datetime.strptime(item['attributes']['created-at'][:10], "%Y-%m-%d")
            if item['attributes']['status'] == "applied":
                if date_start < creation_date and creation_date <= date_end: retorno.append(item['id'])
        page += 1
        resp = requests.get(TFE_ADDR+f'/api/v2/workspaces/{workspace_id}/runs?page[size]=100&page[number]={page}', headers=headers )
    return len(retorno)


def getRunsTotalCount(organisation):
    total_runs = 0
    todo_item = getWorkspaceInfo(organisation)
    for item in todo_item:
        total_runs +=  getRunsCount(item)
    pp.pprint(f"Total runs for {organisation}: {total_runs}")    
    return total_runs     

def getAppliesTotalCount(organisation):
    total_applies = 0
    todo_item = getWorkspaceInfo(organisation)
    for item in todo_item:
        total_applies +=  getAppliesCount(item)
    pp.pprint(f"Total applies for {organisation}: {total_applies}")    
    return total_applies     

@yaspin(text="Loading...")
def getWorkspacesFromAdmin():
    resp = requests.get(TFE_ADDR+f'/api/v2/admin/workspaces', headers=headers )
    if resp.status_code != 200:
        # This means something went wrong.
        pp.pprint(f"something went wrong: {resp}")
    todo  = resp.json()['meta']
    todo_item = resp.json()['meta']['status-counts']
    result = []
    info = { 
      "pending": todo_item["pending"],
      "plan-queued": todo_item["plan-queued"],
      "planning": todo_item["planning"],
      "planned": todo_item["planned"],
      "confirmed": todo_item["confirmed"],
      "apply-queued": todo_item["apply-queued"],
      "applying": todo_item["applying"],
      "applied": todo_item["applied"],
      "discarded": todo_item["discarded"],
      "errored": todo_item["errored"],
      "canceled": todo_item["canceled"],
      "cost-estimating": todo_item["cost-estimating"],
      "cost-estimated": todo_item["cost-estimated"],
      "policy-checking": todo_item["policy-checking"],
      "policy-override": todo_item["policy-override"],
      "policy-checked": todo_item["policy-checked"],
      "policy-soft-failed": todo_item["policy-soft-failed"],
      "planned-and-finished": todo_item["planned-and-finished"],
      "none": todo_item["none"],
      "total": todo_item["total"]
         }
    result.append(info)
    return result    

#Main just has the calls to the above methods, comment out as needed
def main():
    if (TFE_SITE_ADMIN == 'true'):
        data = pandas.DataFrame(getWorkspacesFromAdmin())
        pp.pprint(data)
    else :
        result = getOrgObj()
        totalWorkspaces = 0
        totalRuns = 0
        totalApplies = 0
        for org in result:
            totalWorkspaces += org['workspace_count']
            totalRuns += org['total_runs']
            totalApplies += org['total_applies']
        data = pandas.DataFrame(result)
        pp.pprint(data[['name','workspace_count','total_runs','total_applies']])
        pp.pprint(f"Total workspaces count: {totalWorkspaces}")
        pp.pprint(f"Total runs count: {totalRuns}")  
        pp.pprint(f"Total applies count: {totalApplies}")  
        pp.pprint(f"from {date_start} to {date_end}")      
if __name__ == '__main__':
    main()
