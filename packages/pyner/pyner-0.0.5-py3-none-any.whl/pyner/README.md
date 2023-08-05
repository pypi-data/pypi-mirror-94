# ner

SDK to access API of Ner service

This program is SDK of Ner service API.  

It can handle one sentence and simple text file in chinese. 

## Usage
```text
usage: ner.py [-h] [--endpoint ENDPOINT] [--sentence SENTENCE] [--path PATH]

Process one sentence or simple textfile in chinese by Ner service

optional arguments:
  -h, --help           show this help message and exit
  --endpoint ENDPOINT  Endpoint of Ner service, if not specified, environment 'NER_ENDPOINT' is used.
  --sentence SENTENCE  Sentence to process
  --path PATH          Path file to process
```  
  
For instance:  
```bash
$ python ner.py --endpoint http://example.com/ner/bert/normal --path test.txt --sentence '康龙化成(03759)拟续聘安永华明为2020年度境内会计师事 务所'
{'ORG': ['康龙化成', '安永华明']}
{'LOC': ['新冠', '新疆'],
 'ORG': ['华资实业',
         '明科',
         '中葡',
         '亚星',
         '厦华',
         '中房股份',
         '中房股份',
         '西域旅游',
         '西域旅游',
         '丰华股份',
         '丰华股份',
         '壳公司']}
```
