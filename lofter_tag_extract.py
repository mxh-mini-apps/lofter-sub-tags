# 跑之前要先用下面这行代码安装library
# 在cmd terminal跑: pip install requests beautifulsoup4

import os
import os.path
import datetime
import requests
from bs4 import BeautifulSoup


def get_primary_tag_html(primary_tag, page):
    url = f"http://lofter.com/tag/{primary_tag}?page={page}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    return soup


def extract_secondary_tags(soup, freq_dict):
    sys_tags = ['发布', '加黑', '移动', '编辑', '删除', '转载', '分享', '推荐', '喜欢', '热度', '评论']
    raw_tags = soup.findAll("span", {"class": "opti"})
    dict_keys = freq_dict.keys()
    for tag in raw_tags:
        if tag and tag != "" and tag.text[:2] not in sys_tags:
            tag_text = tag.text.replace("\xa0", " ")
            if tag_text not in dict_keys:
                freq_dict.update({tag_text: 1})
            else:
                freq_dict[tag_text] = freq_dict[tag_text] + 1


def find_all_secondary_tags(primary_tag, pages):
    all_secondary_tags = {}
    for i in range(1, pages + 1):
        print(f'extracting page: {i}')
        soup = get_primary_tag_html(primary_tag, i)
        extract_secondary_tags(soup, all_secondary_tags)
    return all_secondary_tags


def get_tag_freq(freqs):
    sorted_freqs = sorted(freqs.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_freqs


def write_to_csv(tag, pages, freqs, path):
    with open(os.path.join(path, f"{tag}_{pages}_sub_tags.csv"), "w") as f:
        for k, v in freqs:
            f.write(f"{k},{v}\n")


# 主要 run 这个就好
def get_all_sub_tags(tag, pages, path=""):
    sub_tags = find_all_secondary_tags(tag, pages)
    freqs = get_tag_freq(sub_tags)
    write_to_csv(tag, pages, freqs, path)
    print(f"done for {tag}")


today = datetime.datetime.today().strftime("%Y-%m-%d")
today_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), today)


def get_sub_tags_all_members(pages=100, path=today_path):
    if not os.path.exists(path):
        os.makedirs(path)
    with open("members.txt", "r") as members:
        for m in members:
            get_all_sub_tags(m.strip(), pages, path)
    print("all done")
