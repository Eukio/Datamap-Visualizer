# Datamap Visualizer
## A web application used to help the Daikin Controls Testing Team visualize key value data of datamaps with Flask using Python.
The Controls Testing Portal allows users to login, view, and modify thermostat datamaps stored inside the cloud. The search feature that is used to find specified variables within the datamap only allows users to search for one variable at a time. Therefore, my task was to design a user-friendly UI that can help display information of multiple datamap variables at the same time to help the testing team efficiently and simultaneously observe necessary datamap values without needing to repeatedly type into the search bar.
I created a Datamap Visualizer- A web application used to help the Daikin Controls Testing Team visualize key value data of datamaps with Flask using Python.
- Each thermostat has a datamap, which is JSON file that has key value pairs
- Input takes a nested JSON file in array format, separating grouped variables by columns to improve organization
- Outputs an excel file and table of the data
- User can manually refresh the displayed datamap or set a timer for an auto refresh to fetch updated data from the cloud

## Example JSON input array format:
>{
>  "col_1": [
>    "statDKNnumber",
>    "P1P2ForcedFanOnUnitNumber",
>    "schedWedPart5hsp",
>    "schedWedPart6hsp"
>  ],
>  "col_2": [
>    "sysFault4Date",
>    "Enphase2SolarNow",
>    "schedSunPart2Label",
>    "fault19Level"
>  ],
>  "col_3": [
>    "rfCoprocHostTxPackets",
>    "fault22Date",
>    "ctAHMode"
>  ]
>}

## Link to Daikin Testing Portal: https://d3ap1eii0jng13.cloudfront.net/#/ 

## To Run Locally
> cd .\venv\  
> cd .\Scripts\ 
> .\activate   
> $env:FLASK_APP="main.py"   
> flask --debug run //In root project folder     

## Make exe:
//exe located within the dist folder in repo
> pyinstaller --onefile `
>  --name datamap_visualizer `
>  --add-data "website/static;website/static" `
>  --add-data "website/templates;website/templates" `
>  --add-data "website/datamaps;website/datamaps" `
>  --add-data "website/data;website/data" `
>  main.py
