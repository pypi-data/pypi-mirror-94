# -*- coding: utf-8 -*-
from os import sep
from numpy.core.multiarray import datetime_as_string
import requests
import math
import pandas as pd
import json
from datetime import datetime as dt
from datetime import timedelta
import urllib.parse

class Client(object):
    def __init__(self, parameters_file):
        """
        Make client for z-info extract. 
        You can provide a parameter file name.
        If no parameter file name is supplied it will generate a template

        Parameters
        ----------
        parameters_file: str
            Parameter file name
        """
        if not parameters_file:
            parameters = {
                "username":"",
                "password":"",
                "file_name":"",
                "file_format":".csv or .feather",
                "seperate_files":"True or False",
                "input_file":"csv file for tagNr's",
                "startdate":"YYYY-MM-DD",
                "enddate":"YYYY-MM-DD",
                "periode":"",
                "pandas_freq":"",
                "interval":"10",
                "waterschapnummer":"",
                "spcid":""}
            with open('parameters.json', 'w') as fp:
                json.dump(parameters, fp, indent=2)
        else: 
            self.set_parameters(parameters_file)


    def set_parameters(self, parameters_file):
        """
        Set parameters for client

        Parameters
        ----------
        parameters_file: filename to json (without .json) containing parameters
            Parameters for client

        """
        with open(f'{parameters_file}.json') as file:
            parameters = json.load(file)
        self.__username = parameters["username"]
        self.__password = parameters["password"]
        self.file_name = parameters["file_name"]
        self.file_format = parameters["file_format"]
        self.input_file_name = parameters["input_file"]
        self.seperate_files = json.loads(parameters["seperate_files"].lower())
        self.startdate = parameters["startdate"]
        self.enddate = parameters["enddate"]
        self.periode = parameters["periode"]
        self.pandas_freq = parameters["pandas_freq"]
        self.interval = int(parameters["interval"])
        self.waterschapnummer = parameters["waterschapnummer"]
        self.spcid = parameters["spcid"]
        
    def __get_zinfo_token(self):
        """
        Get bearer token for access to the Z-info webservice

        Parameters
        ----------
        username: str
            Username for Z-info (no need for admin rights)
        password: str
            Password for Z-info

        Returns
        -------
        result: str
            Access token in string format
        """

        token_url = "https://webservice.z-info.nl/WSR/zi_wsr.svc/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
                'grant_type': 'password',
                'username': self.__username,
                'password': self.__password
                }
        
        r=requests.post(token_url, headers = headers, data = data)

        r.encoding = "utf-8"
        access_token = r.text # Dictionary in text format

        bearer = json.loads(access_token)['access_token']
        
        return bearer

    def __get_zinfo_data(self, my_token, my_url):
        """
        Retrieve data for a single URL using the Z-info webservice and save it locally

        Parameters
        ----------
        my_token: str
            Access token for Z-info webservice, retrieved using get_bearer_token
        my_url: str
            URL for Z-info web-service
            
        Returns
        -------
        df: pd df
            Data in pandas dataframe
        """
        my_string = {'Authorization': 'Bearer ' + my_token}

        r = requests.get(my_url, headers = my_string)
        
        df = r.json()
        df = df["waarden"]
        return df

    def __date_range(self):
        #TODO check same day
        """
        Split a date range specified by a start date (start) and an end date (end). Splits the date range
        in intervals of interval

        Parameters
        ----------
        start: str
            startdate (yyyy-mm-dd)
        end: str
            enddate (yyyy-mm-dd)
        intv: num
            Number of intervals
            
        Returns
        -------
        dates_splits: list of lists
            A list with intv number of date ranges. Date range specified in str format, in separate list.
        """
        min_difference = 10000*pd.Timedelta(self.periode)
        start = dt.strptime(self.startdate,"%Y-%m-%d")
        end = dt.strptime(self.enddate,"%Y-%m-%d") 
        difference = end-start
        intv = 1
        for intv in range(1,math.ceil(difference.days/min_difference.days)):
            if difference/intv < min_difference:
                break
        diff = (end  - start ) / intv
 
        ranges = [(start + diff * i).strftime("%Y-%m-%d") for i in range(intv)]
        ranges.append(end.strftime("%Y-%m-%d"))
        date_splits = [[ranges[i],ranges[i+1]] for i in range(intv)]
            
        return date_splits

    def __make_url(self, startdate, enddate, tagnr, wbm):
        """ 
        Create a URL for z-info 
        
        Parameters
        ----------
        waterschapnummer: str
            id number waterschap
        startdate: str
            startdate (yyyy-mm-dd)
        enddate: str
            enddate (yyyy-mm-dd)
        tagnr: str
            tag number for sensor
        wbm: str
            aggregate function
        periode: 
            aggregate time unit

        Returns
        -------
        URL: str
            endpoint for z-info api
        """
        return rf'https://webservice.z-info.nl/WSR/zi_wsr.svc/JSON/NL.{self.waterschapnummer}/?spcid={self.spcid}&vraag=$begindatum$={startdate};$einddatum$={enddate};$tagnr$={urllib.parse.quote(tagnr, safe="")};$wbm$={wbm};$periode$={self.periode}'

    def construct_dataframe(self):
        """
        construct a dataframe for given parameters
        
        Returns
        -------
        export_dataframe: DataFrame
            Dataframe containing z-info data
        """ 
        
        input_file = pd.read_csv(f'{self.input_file_name}.csv', sep=',')
        if self.seperate_files:
            export_dataframe = {}
        else:
            export_dataframe = pd.DataFrame()
        date_splits = self.__date_range()
        for i,tagnr in enumerate(input_file['tagnr']):
            name = input_file.loc[i,'name']
            print(f'Getting data for {name}')
            tag_dataframe = pd.DataFrame()
            for date_split in date_splits:
                token = self.__get_zinfo_token()
                URL = self.__make_url(date_split[0], date_split[1], tagnr, input_file.loc[i,'wbm'])
                tag_dataframe = tag_dataframe.append(self.__get_zinfo_data(token, URL), ignore_index=True)
            if self.seperate_files:
                export_dataframe[name] = tag_dataframe
            else:
                if i == 0:
                    export_dataframe['tijdstip'] = pd.date_range(start = self.startdate, end = self.enddate, freq = self.pandas_freq)
                if tag_dataframe.empty:
                    print(f"no data for {name}")
                else:
                    tag_dataframe = tag_dataframe.reset_index(drop=True)
                    tag_dataframe = tag_dataframe.iloc[:,[0,2]].rename(columns={"dem":"tijdstip", "hstWaarde":name})
                    tag_dataframe['tijdstip'] = pd.to_datetime(tag_dataframe['tijdstip'])
                    export_dataframe = pd.merge(export_dataframe, tag_dataframe, how="left", on = ['tijdstip'])
        return export_dataframe