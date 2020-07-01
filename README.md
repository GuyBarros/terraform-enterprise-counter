# terraform-enterprise-counter
A simple project to count Organizations, Workspaces and Runs.

## set up
This project requires two environment variables to run: TFE_ADDR and TFE_TOKEN.

```bash
export TFE_ADDR=https://app.terraform.io
export TFE_API_TOKEN=hunter2
```

## how it works
this project will use the api token to list all the Organizations it has access to. then, it will list all the workspaces in each org and count the runs for each workspace. this all goes into a dict list and is then sent to pandas as a Dataframe.

 due to the simplicity of the code it should be fairly simple to extend the code to your necessities.

## output

an example output of the project:

```bash
                            name  workspace_count  total_runs
0                 andygrifdemo                   2          24
3         emea-se-playground-2019               20         243
4            example-organization               12         158
6                       GuyBarros                5           0
7              Hashicorp-neh-Demo               20         135
8           hc-emea-sentinel-demo                8          47
11                    rgustso                    6          58
12                   RogerBe                    20         242
13                      rusty-pro               15         148
15                  SNOW-se-demos               20          58
16                  TaimurKOrg                   2          14
'Total workspaces count: 167'
'Total runs count: 1503'
```
note: I've omitted some customer facing organizations so the sums wont add up.


