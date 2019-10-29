# lofter-tag-crawler
## Setup
- Download python3.7
- Download pip for python 3
- Download libraries, run `pip install -r requirements.txt` in terminal

## Run Code
- To run search for individual primary tag:
    run `get_all_sub_tags(tag, pages, path)`
    - pages default is 100
    - path default is root of project
- To run search for all super vocal members:
    run `get_sub_tags_all_members(pages, path)`
    - pages default is 100
    - path default is a new folder of today's date under root project
