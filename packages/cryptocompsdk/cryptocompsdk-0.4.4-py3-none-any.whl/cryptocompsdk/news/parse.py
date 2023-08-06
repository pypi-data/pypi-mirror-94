import os
from copy import deepcopy
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Optional, Any, List, cast, Union
from urllib.parse import urlparse

import pandas as pd
import requests
from tqdm import tqdm

from cryptocompsdk.logger import logger
from cryptocompsdk.response import ResponseException, ResponseAPIBase
from cryptocompsdk.general.parse import from_int, from_none, from_union, from_float, from_str, to_float, from_bool, \
    from_dict, to_class, is_type, from_int_or_str, from_na, from_str_number, from_list, from_stringified_bool, \
    from_plain_dict


class SourceInfo:
    name: Optional[str]
    lang: Optional[str]
    img: Optional[str]

    def __init__(self, name: Optional[str], lang: Optional[str], img: Optional[str]) -> None:
        self.name = name
        self.lang = lang
        self.img = img

    @staticmethod
    def from_dict(obj: Any) -> 'SourceInfo':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        lang = from_union([from_str, from_none], obj.get("lang"))
        img = from_union([from_str, from_none], obj.get("img"))
        return SourceInfo(name, lang, img)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["lang"] = from_union([from_str, from_none], self.lang)
        result["img"] = from_union([from_str, from_none], self.img)
        return result


class NewsRecord:
    id: Optional[int]
    guid: Optional[str]
    published_on: Optional[int]
    imageurl: Optional[str]
    title: Optional[str]
    url: Optional[str]
    source: Optional[str]
    body: Optional[str]
    tags: Optional[str]
    categories: Optional[str]
    upvotes: Optional[int]
    downvotes: Optional[int]
    lang: Optional[str]
    source_info: Optional[SourceInfo]

    def __init__(self, id: Optional[int], guid: Optional[str], published_on: Optional[int], imageurl: Optional[str], title: Optional[str], url: Optional[str], source: Optional[str], body: Optional[str], tags: Optional[str], categories: Optional[str], upvotes: Optional[int], downvotes: Optional[int], lang: Optional[str], source_info: Optional[SourceInfo]) -> None:
        self.id = id
        self.guid = guid
        self.published_on = published_on
        self.imageurl = imageurl
        self.title = title
        self.url = url
        self.source = source
        self.body = body
        self.tags = tags
        self.categories = categories
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.lang = lang
        self.source_info = source_info

    @staticmethod
    def from_dict(obj: Any) -> 'NewsRecord':
        assert isinstance(obj, dict)
        id = from_union([from_none, lambda x: int(from_str(x))], obj.get("id"))
        guid = from_union([from_str, from_none], obj.get("guid"))
        published_on = from_union([from_int, from_none], obj.get("published_on"))
        imageurl = from_union([from_str, from_none], obj.get("imageurl"))
        title = from_union([from_str, from_none], obj.get("title"))
        url = from_union([from_str, from_none], obj.get("url"))
        source = from_union([from_str, from_none], obj.get("source"))
        body = from_union([from_str, from_none], obj.get("body"))
        tags = from_union([from_str, from_none], obj.get("tags"))
        categories = from_union([from_str, from_none], obj.get("categories"))
        upvotes = from_union([from_none, lambda x: int(from_str(x))], obj.get("upvotes"))
        downvotes = from_union([from_none, lambda x: int(from_str(x))], obj.get("downvotes"))
        lang = from_union([from_str, from_none], obj.get("lang"))
        source_info = from_union([SourceInfo.from_dict, from_none], obj.get("source_info"))
        return NewsRecord(id, guid, published_on, imageurl, title, url, source, body, tags, categories, upvotes, downvotes, lang, source_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.id)
        result["guid"] = from_union([from_str, from_none], self.guid)
        result["published_on"] = from_union([from_int, from_none], self.published_on)
        result["imageurl"] = from_union([from_str, from_none], self.imageurl)
        result["title"] = from_union([from_str, from_none], self.title)
        result["url"] = from_union([from_str, from_none], self.url)
        result["source"] = from_union([from_str, from_none], self.source)
        result["body"] = from_union([from_str, from_none], self.body)
        result["tags"] = from_union([from_str, from_none], self.tags)
        result["categories"] = from_union([from_str, from_none], self.categories)
        result["upvotes"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.upvotes)
        result["downvotes"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.downvotes)
        result["lang"] = from_union([from_str, from_none], self.lang)
        result["source_info"] = from_union([lambda x: to_class(SourceInfo, x), from_none], self.source_info)
        return result

    @property
    def is_empty(self) -> bool:
        is_empty_cols = [
            'id',
            'guid',
            'published_on',
            'imageurl',
            'title',
            'url',
            'source',
            'body',
            'tags',
            'categories',
            'upvotes',
            'downvotes',
            'lang',
            'source_info',
        ]

        for col in is_empty_cols:
            if getattr(self, col) != 0:
                return False
        return True

    def download_article(self, use_alt_url: bool = False) -> str:
        """
        Download and return the HTML of this news article

        :param use_alt_url: The default is to use the url given in the guid attribute,
            if True then use url attribute instead of guid
        :return:
        """
        if not use_alt_url:
            url = self.guid
            alt_url = self.url
        else:
            url = self.url
            alt_url = None

        if pd.isnull(url):
            valid_url = False
        else:
            parsed = urlparse(url)
            valid_url = bool(parsed.scheme and parsed.netloc)

        if not valid_url:
            if alt_url is not None:
                return self.download_article(use_alt_url=True)
            raise NoValidNewsURLException(f'Url {url} is invalid')

        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        }

        if url is None:
            # Should not happen, for typing purposes
            raise ValueError('must provide a url')

        resp = requests.get(url, headers=headers)
        status_code = resp.status_code
        text = resp.text

        if alt_url is not None and status_code != 200:
            return self.download_article(use_alt_url=True)
        elif status_code != 200:
            raise InvalidNewsResponseException(f'Got status code {status_code} for request to {url}. Response: {text}')

        return text


class RateLimit:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'RateLimit':
        assert isinstance(obj, dict)
        return RateLimit()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class NewsData(ResponseAPIBase):
    type: Optional[int]
    message: Optional[str]
    promoted: Optional[List[Any]]
    data: Optional[List[NewsRecord]]
    rate_limit: Optional[RateLimit]
    has_warning: Optional[bool]

    def __init__(self, type: Optional[int], message: Optional[str], promoted: Optional[List[Any]], data: Optional[List[NewsRecord]], rate_limit: Optional[RateLimit], has_warning: Optional[bool]) -> None:
        self.type = type
        self.message = message
        self.promoted = promoted
        self.data = data
        self.rate_limit = rate_limit
        self.has_warning = has_warning

    @staticmethod
    def from_dict(obj: Any) -> 'NewsData':
        assert isinstance(obj, dict)
        type = from_union([from_int, from_none], obj.get("Type"))
        message = from_union([from_str, from_none], obj.get("Message"))
        promoted = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("Promoted"))
        data = from_union([lambda x: from_list(NewsRecord.from_dict, x), from_none], obj.get("Data"))
        rate_limit = from_union([RateLimit.from_dict, from_none], obj.get("RateLimit"))
        has_warning = from_union([from_bool, from_none], obj.get("HasWarning"))
        return NewsData(type, message, promoted, data, rate_limit, has_warning)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Type"] = from_union([from_int, from_none], self.type)
        result["Message"] = from_union([from_str, from_none], self.message)
        result["Promoted"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.promoted)
        result["Data"] = from_union([lambda x: from_list(lambda x: to_class(NewsRecord, x), x), from_none], self.data)
        result["RateLimit"] = from_union([lambda x: to_class(RateLimit, x), from_none], self.rate_limit)
        result["HasWarning"] = from_union([from_bool, from_none], self.has_warning)
        return result

    def to_df(self) -> pd.DataFrame:
        if not self.data:
            return pd.DataFrame()
        df = pd.DataFrame(self.to_dict()['Data'])
        df['published_on'] = df['published_on'].apply(pd.Timestamp.fromtimestamp)

        all_sources = []
        for record in self.data:
            si = record.source_info
            if si is not None:
                source_series = pd.Series(si.to_dict())
                all_sources.append(source_series)
        source_df = pd.concat(all_sources, axis=1).T
        df.drop('source_info', axis=1, inplace=True)
        new_cols = [col for col in source_df.columns if col not in df.columns]

        df = pd.concat([df, source_df[new_cols]], axis=1)

        return df

    @property
    def has_error(self) -> bool:
        # No response object in this API
        return self.message != 'News list successfully returned'

    # Pagination methods

    @property
    def is_empty(self) -> bool:
        if self.data is None:
            return True

        for record in self.data:
            if not record.is_empty:
                return False

        return True

    def __add__(self, other):
        out_obj = deepcopy(self)
        out_obj.data += other.data
        return out_obj

    def __radd__(self, other):
        out_obj = deepcopy(other)
        out_obj.data += self.data
        return out_obj

    @property
    def time_from(self) -> int:
        if self.data is None:
            raise ValueError('cannot determine time from as there is no data')

        times = [record.published_on for record in self.data if record.published_on is not None]
        if not times:
            raise ValueError('could not calculate time from as there is no data')
        min_times = min(times)
        min_times = cast(int, min_times)  # for mypy
        return min_times

    def delete_record_matching_time(self, time: int):
        # not a problem with this API, no overlapping time
        pass

    def trim_empty_records_at_beginning(self):
        # Earliest records are at the end of data

        # Delete, starting from end, oldest record
        for i, record in reversed(list(enumerate(self.data))):
            if record.is_empty:
                del self.data[i]
            else:
                # First non-empty record from end, we have now hit the actual data section, stop deleting
                break

    def download_articles(self, out_folder: Union[str, Path] = 'articles', num_threads: int = 20,
                          restart: bool = False):
        """
        Download the HTML of all news articles in this collection and save to files in a folder

        :param out_folder: Where to save the articles
        :param num_threads: How many concurrent requests to execute
        :param restart: False to not download where an article already exists, True to re-download in that case
        :return:
        """
        if self.data is None:
            raise ValueError('Cannot download articles as the data attribute is None')

        out_folder = Path(out_folder)
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        with ThreadPool(num_threads) as pool:
            results = []
            for article in self.data:
                res = pool.apply_async(_download_and_save_article, (article, out_folder, restart))
                results.append(res)

            for result in tqdm(results):
                result.get()


def _download_and_save_article(article: NewsRecord, out_folder: Path, restart: bool = False):
    out_path = out_folder / f'{article.id}.html'
    error_dir = out_folder / 'Error Responses'
    error_path = error_dir / f'{article.id}.txt'

    if not restart and out_path.exists():
        logger.info(f'Found existing text for article {article.id} and restart=False, skipping download')
        return

    try:
        text = article.download_article()
    except (
        requests.ConnectionError,
        requests.TooManyRedirects,
        NoValidNewsURLException,
        InvalidNewsResponseException
    ) as e:
        logger.error(f'Got error while downloading {article.id} from urls: {article.guid} and {article.url}. See {error_path}')
        if not os.path.exists(error_dir):
            try:
                os.makedirs(error_dir)
            except FileExistsError:
                pass  # created by another thread
        error_path.write_text(str(e))
        return

    # Got valid result
    logger.debug(f'Downloaded text for article {article.id}')
    out_path.write_text(text)


def news_from_dict(s: Any) -> NewsData:
    return NewsData.from_dict(s)


def news_to_dict(x: NewsData) -> Any:
    return to_class(NewsData, x)


class CouldNotGetNewsException(ResponseException):
    pass


class NoValidNewsURLException(Exception):
    pass


class InvalidNewsResponseException(ResponseException):
    pass