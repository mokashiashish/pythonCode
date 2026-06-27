#!/usr/bin/env python3
"""Fetch multiple RSS feeds in parallel and write extracted items to output_RSS.txt

Requirements handled:
- Load given RSS URLs
- Fetch in parallel using ThreadPoolExecutor
- Parse XML and extract item title/link/description
- Handle errors: network, missing/empty XML, no items
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import xml.etree.ElementTree as ET
import socket

URLS = [
    "http://feeds.abcnews.com/abcnews/usheadlines",
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://www.cbsnews.com/latest/rss/main",
]

OUTFILE = "output_RSS.txt"


def fetch_url(url, timeout=10):
    req = Request(url, headers={"User-Agent": "rss-parallel/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            if not data:
                return None, "empty-response"
            return data, None
    except HTTPError as e:
        return None, f"http-error: {e.code} {e.reason}"
    except URLError as e:
        return None, f"url-error: {e.reason}"
    except socket.timeout:
        return None, "timeout"
    except Exception as e:
        return None, f"other-error: {e}"


def parse_rss(xml_bytes):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        return None, f"parse-error: {e}"

    # Support common RSS structures: <rss><channel><item> or <feed><entry>
    items = []
    # RSS2
    for item in root.findall('.//item'):
        title = item.findtext('title') or ''
        link = item.findtext('link') or ''
        desc = item.findtext('description') or ''
        items.append({'title': title.strip(), 'link': link.strip(), 'description': desc.strip()})
    # Atom
    if not items:
        for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
            title = entry.findtext('{http://www.w3.org/2005/Atom}title') or ''
            link_el = entry.find('{http://www.w3.org/2005/Atom}link')
            link = link_el.get('href') if link_el is not None else ''
            summary = entry.findtext('{http://www.w3.org/2005/Atom}summary') or entry.findtext('{http://www.w3.org/2005/Atom}content') or ''
            items.append({'title': title.strip(), 'link': link.strip(), 'description': summary.strip()})

    if not items:
        return [], None
    return items, None


def process_feed(url):
    data, err = fetch_url(url)
    if err:
        return {'url': url, 'error': err, 'items': None}
    if data is None:
        return {'url': url, 'error': 'no-data', 'items': None}

    items, perr = parse_rss(data)
    if perr:
        return {'url': url, 'error': perr, 'items': None}
    if items is None:
        return {'url': url, 'error': 'no-rss-structure', 'items': None}
    if len(items) == 0:
        return {'url': url, 'error': 'empty-rss', 'items': []}

    return {'url': url, 'error': None, 'items': items}


def write_output(results, outfile=OUTFILE):
    with open(outfile, 'w', encoding='utf-8') as f:
        for res in results:
            f.write(f"Feed: {res['url']}\n")
            if res.get('error'):
                f.write(f"Error: {res['error']}\n\n")
                continue
            items = res.get('items') or []
            for i, it in enumerate(items, 1):
                f.write(f"{i}. {it.get('title','(no title)')}\n")
                if it.get('link'):
                    f.write(f"   Link: {it['link']}\n")
                if it.get('description'):
                    # keep description single-line-ish
                    desc = ' '.join(it['description'].split())
                    f.write(f"   Desc: {desc}\n")
            f.write('\n')


def main(urls=URLS, max_workers=5):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(process_feed, u): u for u in urls}
        for fut in as_completed(futures):
            try:
                res = fut.result()
            except Exception as e:
                res = {'url': futures[fut], 'error': f'worker-exception: {e}', 'items': None}
            results.append(res)

    write_output(results)
    return results


if __name__ == '__main__':
    import sys
    try:
        res = main()
        print(f"Wrote output to {OUTFILE}")
        sys.exit(0)
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(2)
