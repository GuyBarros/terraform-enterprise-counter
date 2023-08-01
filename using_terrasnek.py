import os
from terrasnek.api import TFC as TFP
import pprint
import pandas
pp = pprint.PrettyPrinter()
# do `pip install terrasnek` before running this script

TFE_TOKEN = os.getenv("TFE_TOKEN", None)
TFE_URL = os.getenv("TFE_URL", "https://app.terraform.io")  # ex: https://app.terraform.io

api = TFP(TFE_TOKEN, url=TFE_URL)

orgs = api.orgs.list()['data']
print (f"Found {len(orgs)} Organizations")

total_rum = 0
total_workspaces = 0
result = []
for org in orgs:
    org_workspaces_count = 0
    api.set_org(org['id'])
    print (f".: looking up Organization {org['id']}",)
    all_workspaces = api.workspaces.list_all()['data']
    org_workspaces_count += len (all_workspaces)
    total_workspaces += org_workspaces_count
    print (f"Found {org_workspaces_count} Workspaces")
    result.append(dict(Organization_id = org['id'], Workspaces = all_workspaces, Workspace_count = org_workspaces_count ))
    rum = 0
    for workspace in all_workspaces:
        # to add details per workspace
        #runs = api.runs.list_all(workspace['id'])['data']
        #print(workspace['attributes']['name'], workspace['attributes']['resource-count'])
        rum += int(workspace['attributes']['resource-count'])

    print(f"RUM for org {org['id']}: {rum}")
    total_rum += rum


print("\n")
data = pandas.DataFrame(result)
pp.pprint(data[['Organization_id','Workspace_count']])
print(f"Total number of Organizations: {len(orgs)}")
print(f"Total number of Workspace: {total_workspaces}")
print(f"Total number of RUMs: {total_rum}")
