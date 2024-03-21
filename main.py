from Screping import log_message,timesnownews,chroniclejournal,DB
import json
import pandas as pd
import pyodbc
import time
def main():
        try:
                start=time.time()
                #input from json
                with open('config.json') as config_file:
                    data = json.load(config_file)
                URLS=data['URL']
                
                
                cursor,connection=DB()
                Final_Dataframe=pd.DataFrame()

                for URL in URLS:
                    MediaName=str(URL.split('/')[2]).split('.')[1]
                    df=eval(MediaName)(URL)
                    log_message(f"EXEC :{MediaName} function for URL {URL} executed Successfully!\n",0)
                    Final_Dataframe=pd.concat([Final_Dataframe,df],ignore_index=True)

        except NameError as e:
                print("No matching media name to 'chroniclejournal' or 'timesnownews'\n")
                log_message("ERROR: No matching media name to 'chroniclejournal' or 'timesnownews'\n",1)
                
                

        finally:
                Final_Dataframe.to_csv("Screped_data.txt",sep='\n')
                results=cursor.execute('select * from [dbo].[SCRAPED_DATA]')
                for result in results:
                        print(result)
                connection.commit()
                connection.close()
                log_message("EXEC : Data saved successfully in Database.\n",0)
                end=time.time()

                log_message(f"Time Required :{(end-start)}\n\n",0)
                print("Scraping done Successfully!")
       
if __name__ == '__main__':
    main()
