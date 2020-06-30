# terraform-enterprise-counter
A simple project to count Organizations, Workspaces and Runs.

## set up
This project requires two environment variables to run: TFE_ADDR and TFE_TOKEN.

```bash
export TFE_ADDR=https://app.terraform.io
export TFE_API_TOKEN=hunter2
```

## how it works
this project will use the api token to list all the Organizations it has access to. then, it will list all the workspaces in each org and count the runs for each workspace. due to the simplicity of the code it should be fairly simple to extend the code to your necessities.

## output

an example output of the project:

```bash
andygriffindemo total workspaces: 2 total runs: 24'
'emea-se-playground-2019 total workspaces: 20 total runs: 241'
'example-organization total workspaces: 12 total runs: 158'
'GuyBarros total workspaces: 5 total runs: 0'
'Hashicorp-neh-Demo total workspaces: 20 total runs: 134'
'hc-emea-sentinel-demo total workspaces: 8 total runs: 47'
'rgustafsson total workspaces: 6 total runs: 58'
'RogerBerlind total workspaces: 20 total runs: 242'
'rusty-pro total workspaces: 15 total runs: 148'
'SNOW-se-demos total workspaces: 20 total runs: 58'
'TaimurKhanOrg total workspaces: 2 total runs: 14'
'Total workspaces count: 167'
'Total runs count: 1500'
```
note: I've omitted some customer facing organizations so the sums wont add up.


