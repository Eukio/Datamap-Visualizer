# Datamap Visualizer
## Displays selected datamap variables using a nested .json input. Able to output CSV files and pull datamaps from the cloud.

Link: https://d3ap1eii0jng13.cloudfront.net/#/ 
 $env:FLASK_APP="main.py"      
Make exe:
pyinstaller --onefile `
>>   --name datamap_visualizer `
>>   --add-data "website/static;website/static" `
>>   --add-data "website/templates;website/templates" `
>>   main.py
