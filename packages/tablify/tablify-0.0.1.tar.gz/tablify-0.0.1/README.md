
# tablify
######  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://github.com/your/your-project/blob/master/LICENSE)
> Convert data structure into html table

tablify is package used to convert python data  structures to html or clean tabular design. Thanks for checking it out.


### Requirements
- Python 3.x

### Example 

    import sys
    from tablify.parser.parse import pyobj
    
    dict_example = {'Total_Matches': ['200', '127', '102'],\
        'Player Name': ['M.S Dhoni', 'Virendra Sehwag', 'Shikhar Dhawan'],\
        'Sixes': ['280.', '210', '126']}
    
    pyobj = pyobj()
    htmltext = pyobj.dictToHTMLTable(dict_example)
    print(htmltext)

