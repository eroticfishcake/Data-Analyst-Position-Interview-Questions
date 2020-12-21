# Junior Data Analyst Position Interview Questions

I have recently applied for a position of Junior Data Analyst at a company that shall remain nameless due to privacy reasons. 
I was presented with two tasks, that had to be done, within two days, in order to advance to the last stage of application.

## First task

You are provided with a Google spreadsheet that consists of 4 data sets, with 3 Placements, Impressions, Revenue split by days and advertisers. Since I don't want to expose the company's name, I have saved the dataset as an excel file, that you can find in this repository as *dataset.xlsx*

The main task is to **combine 4 datasets and create a summary table and a graph**. The table and the graph have to be able to dinamically update when the data source "dataset" updates daily with new data to eventually represent the whole month. Analyse results, provide insights and suggest how to optimize the process.

## Second task

Using Google trends, SimilarWeb, AnswerThePublic, Product Hunt, App Stores, blog posts, competitors and so on, find trends within Wellness, Fitness and Health industry, analyse them and provide the most popular and growing topics. Finally, **find two most potential topics for Wellness Diginal Products with data-driven reasoning**.

## Solutions

For the very first task I decided to use Python, since I am familiar with it's libraries used for data analysis and also Python is extremely versatile. Furthermore, prior to doing this task, I sat down and split this exercise into smaller chunks that had to be done one after the other in order to achieve the result:
- Interact with google spreadsheets and extract the provided data
- Clean the data, transform the columns where needed
- Visualize and analyse the prepared data

Then, I proceeded to create a service account in Google API that allowed me to interact with Google products using python, specifically with Google Spreadsheets. Furthermore, I have tried using already preinstalled libraries in python to retrieve data, but none of them could extract the wanted data since there were two tabs in the given spreadsheet and it would only let me get the info written in the first tab. Therefore, I installed an external library called [sheetfu](https://github.com/socialpoint-labs/sheetfu), that allowed me to switch between tabs automatically
```python
from sheetfu import SpreadsheetApp
serviceaccountfile = ".json file that you get from google when you create service account"
googleid = "google id of a wanted spreadsheet"
spreadsheet = SpreadsheetApp(serviceaccountfile).open_by_id(googleid)
sheet = spreadsheet.get_sheet_by_name(sheetname)      # access the wanted tab
data_range = sheet.get_data_range()                   # extract range where the data is
values = data_range.get_values()                      # get values
values = pd.DataFrame(data = values[8:], columns = values[7]) # put data into pandas dataframe
```
