# 跑之前要先用下面这行代码安装library
# 在cmd terminal跑: pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
from itertools import groupby


def get_primary_tag_html(primary_tag, page):
    url = f"http://lofter.com/tag/{primary_tag}?page={page}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    return soup


def extract_secondary_tags(soup):
    sys_tags = ['发布', '加黑', '移动', '编辑', '删除', '转载', '分享', '推荐', '喜欢', '热度', '评论']
    raw_tags = soup.findAll("span", {"class": "opti"})
    clean_tags = []
    for tag in raw_tags:
        if tag and tag != "":
            clean_tags.append(tag.text) if tag.text[:2] not in sys_tags else None
    return clean_tags


def find_all_secondary_tags(primary_tag, pages):
    all_secondary_tags = []
    for i in range(1, pages + 1):
        print(f'extracting page: {i}')
        soup = get_primary_tag_html(primary_tag, i)
        page_tags = extract_secondary_tags(soup)
        all_secondary_tags = all_secondary_tags + page_tags
    return all_secondary_tags


def get_tag_freq(tags):
    tags.sort()
    freqs = {key.replace("\xa0", " "): len(list(group)) for key, group in groupby(tags)}
    sorted_freqs = sorted(freqs.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_freqs


def write_to_csv(tag, pages, freqs):
    with open(f"{tag}_{pages}_sub_tags.csv","w") as f:
        for k, v in freqs:
            f.write(f"{k},{v}\n")


# 主要 run 这个就好
def get_all_sub_tags(tag, pages):
    sub_tags = find_all_secondary_tags(tag, pages)
    freqs = get_tag_freq(sub_tags)
    write_to_csv(tag, pages, freqs)
    print("done")
