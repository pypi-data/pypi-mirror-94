# actedu-crawler

Crawl ACT Education websites' searchable documents for **archival** purposes.

## Setup

Install dependencies:

```sh
pip3 install -r requirements.txt
```

Install [aria2c](http://aria2.github.io/)

## Usage

```sh
python3 -m actedu_crawler -o 'output directory' -u 'URL/domain'
```

## Notes

- This won't work on most private school sites which usually use custom WordPress sites rather than the ACT Government's default SquizMatrix setup.

- This will work on some ACT Government sites outside of the Education Directorate, but since most of them are currently being upgraded there isn't much point in writing a crawler for them, *yet*.