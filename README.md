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
Now that we had all the data we needed, it was time for cleaning and transforming. The standard procedure is checking for any NaN/NA values, there weren’t any in this data set. Furthermore, there were couple of things that needed transforming, for example there was one column in the dataset which had revenue in ($), while all the other revenue columns had it in (€). To automate this process, I used my knowledge of web scraping to extract the current USD/EUR ratio and apply it to column, this way the rate of exchange is the most accurate there is and there is no need for human interaction! Code below shows a function that I used to achieve that. 
```python
exchangelink = "https://www.xe.com/currencycharts/?from=USD&to=EUR"

def getrate(exchangelink):
    r = requests.get(exchangelink)               # request page access
    soup = BeautifulSoup(r.text, 'html.parser')  # parse through html
    data = soup.findAll("td")                    # find td
    datapoint = str(data[1])                     # get the needed exchange rate
    rate = float(datapoint[4:-5])                # transform it to float
    return rate
```
Also, the first column had to be renamed to “Advertisers” to match other column names (was needed later for joining the columns together). I have also added the Placement column for each dataset. Finally, using pandas provided tools, I have concatenated all 4 datasets to provide a single dataset containing all the information and saved it as an excel file. The process was a bit manual since I had to input columns that had to be seperated before concatenating. I have added my code below, so if you have any suggestions on how to improve and automate it, feel free to message me :blush:
