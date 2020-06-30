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
                             name  total_runs  workspace_count                                         workspaces
0                 andygriffindemo          24                2         [ws-jiBewknXB6XC4eL7, ws-yuoQbRT5BtS2TpbZ]
3         emea-se-playground-2019         243               20  [ws-NNPCZRmKM6AvB1uE, ws-6LvLRx7uFoDD7Znf, ws-...
4            example-organization         158               12  [ws-z16LcBbm9wSBpF54, ws-r8GQgRHNXaokQvkf, ws-...
6                       GuyB           0                5  [ws-QbbCBd1nsc4bsDtx, ws-ogi7NTCi4A8iRSXn, ws-...
7              Hashicorp-neh-Demo         135               20  [ws-puN8BKm6dXVH7Bpj, ws-5sHR9no187diLzEh, ws-...
8           hc-emea-sentinel-demo          47                8  [ws-YmntZJ3wFaoNNWMs, ws-UXUErKwGzzhgLhTE, ws-...
11                    rgustaf          58                6  [ws-Dn6fgzhkijVUkUkY, ws-j4MitE5HK1wjzMU9, ws-...
12                   RogerB         242               20  [ws-6NZERYHHkuAqAPVx, ws-gdk6qhq7NTAzmV2Q, ws-...
13                      rusty-pro         148               15  [ws-E83Vc5rCnH7M5JQi, ws-uUHkZqKDGqqgxBCL, ws-...
15                  SNOW-se-demos          58               20  [ws-Sf3VSoKyiV99oNSz, ws-yeV4xcoyBLAih77b, ws-...
16                  TaimurKOrg          14                2         [ws-yBoSn5yjEgoygKRm, ws-LSBh19R1agjdDw9n]
'Total workspaces count: 167'
'Total runs count: 1503'
```
note: I've omitted some customer facing organizations so the sums wont add up.


