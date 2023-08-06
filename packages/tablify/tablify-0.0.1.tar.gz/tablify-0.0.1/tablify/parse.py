from tablify.core.html import HTML
from pandas import DataFrame
import ast

class pyobj():
    
    def dictToHTMLTable(self, dict : dict) -> str:
        #print(dict.keys())
        html = HTML(Header = dict.keys(),
                    tableStyles={'margin': '3px'},
                    trStyles={'background-color': '#7cc3a97d'},
                    thStyles={ 'color': 'white'})
        for i, row in enumerate(zip(*dict.values())):
            if i%2 == 0:
                BGC = 'aliceblue'
            else:
                BGC = '#c2d4e4'
            html.addRow(row, trStyles={'background-color' : BGC},\
                tdStyles={'padding': '1rem'})
        return html

    def dfToHTMLTable(self, df : DataFrame) -> str:
        parseddf = ast.literal_eval(df.to_json(orient='split'))
        #print(parseddf)
        html = HTML(Header = parseddf["columns"],
                    tableStyles={'margin': '3px'},
                    trStyles={'background-color': '#7cc3a97d'},
                    thStyles={ 'color': 'white'})
        for i, row in enumerate(parseddf["data"]):
            if i%2 == 0:
                BGC = 'aliceblue'
            else:
                BGC = '#c2d4e4'
            html.addRow(row, trStyles={'background-color' : BGC},\
                tdStyles={'padding': '1rem'})
        return html

