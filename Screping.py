from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import logging
import json
import pyodbc


def DB():
        server='ATISL416'
        database='Scraped'
        username='ATISL416\\Shivam_Dandavate'
        password=''

        conn=pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_connection=yes')
        csr=conn.cursor()

        return csr,conn


def log_message(message: str, level: int):
    """
    This method logs success/failure messages in logger file

    Args:
        message (str): message to log
        level (int): severity level (error=1, info=0)
    """
    # Configuring basic logging settings
    logging.basicConfig(filename='logger.log',
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO)

    # Logging based on severity level
    if level == 1:
        logging.error(message)
    elif level == 0:
        logging.info(message)
    
def timesnownews(URL: str):
        '''
        This method scrapes data based on the given search string from Google search engine

        Args:
            URL(str)   :    Link of the article from BusinessWorld media to scrap.
            
        Returns:
            df : DataFrame of Title and Discription of article given in URL.
            
        '''
        try:
                description=[]
                response=requests.get(URL)
                soup=bs(response.text,'html.parser')
                title=str(soup.title.text)
                #print(soup.prettify())
                cur,con=DB()
                for div in soup.find_all('div',class_='_1884'):
                        description.append(div.text)
                Dataframe=pd.DataFrame({"URL":['URL : '+URL+'\n\n'],"Title":['TITLE : '+title+'\n\n'],"Description":['DESCRIPTION : '+str(''.join(description))+'\n\n']})
                cur.execute(''' insert into [dbo].[SCRAPED_DATA] values(?,?,?)''',URL,title,str(''.join(description)))
                con.commit()
                con.close()
                return Dataframe
                
        except Exception as e:
                log_message("ERROR in timesnownews: "+str(e),1)
        


def chroniclejournal(URL: str):
        '''
        This method scrapes data based on the given search string from Google search engine

        Args:
            URL(str)  :  Link of the article from TheChronicleJournal media to scrap.
            
        Returns:
            df  :  DataFrame of Title and Discription of article given in URL.
            
        '''
        try:
                response=requests.get(URL)
                soup=bs(response.text,'html.parser')
                cur,con=DB()
                
                title=str(soup.title.text)
                response=requests.get(URL)
                for div in soup.find_all('div',class_='asset-content subscriber-premium'):
                        description=div.p.text

                Dataframe=pd.DataFrame({"URL":['URL : '+URL+'\n\n'],"Title":['TITLE : '+title+'\n\n'],"Description":['DESCRIPTION : '+description+'\n\n']})

                cur.execute(''' insert into [dbo].[SCRAPED_DATA] values(?,?,?)''',URL,title,description)
                con.commit()
                con.close()
                return Dataframe
        except Exception as e:
                log_message("ERROR in chroniclejournal: "+str(e),1)











    
