# ner

SDK to access API of Ner service

This program is SDK of Ner service API.  

It can handle one sentence or simple text file by self-hosted NER service or Stanford NER service (http://nlp.stanford.edu:8080/ner/process). 

## Installation
```bash
pip install pyner
```
## Usage
```text
usage: ner.py [-h] [--nertype NERTYPE] [--classifier CLASSIFIER]
              [--endpoint ENDPOINT] [--sentence SENTENCE] [--path PATH]

Process one sentence and simple textfile by remote self-NER service or
Stanford NER one.

optional arguments:
  -h, --help            show this help message and exit
  --nertype NERTYPE     NER service type,0:self-NER(defualt),1:Stanford-NER
  --classifier CLASSIFIER
                        classifier code of Stanford NER service,including
                        7class, 4class, 3class, distsim
  --endpoint ENDPOINT   Endpoint of self-NER service,ignored when Stanford-NER
                        type
  --sentence SENTENCE   Sentence to process
  --path PATH           Path file to process
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
$ python ner.py --nertype stanford --sentence 'hello, chongqing, intel, IBM, Tecent. Bill Gates said.' --classifier 7class
{'LOC': ['chongqing'],
 'ORG': ['intel', 'IBM', 'Tecent'],
 'PER': ['Gates']}
```
