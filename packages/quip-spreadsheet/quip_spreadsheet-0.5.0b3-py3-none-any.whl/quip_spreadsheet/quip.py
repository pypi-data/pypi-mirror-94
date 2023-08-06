from __future__ import annotations
import logging
from typing import Any, List, Dict, Optional, Union
from json.decoder import JSONDecodeError
from dataclasses import dataclass, field
from enum import Enum

import xml.etree.ElementTree


import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError


class QuipSpreadsheetClientException(Exception):
    """Generic Exception raised when an error occurs in the client."""


class QuipApiTimeoutException(QuipSpreadsheetClientException):
    """Exception raised when a Timeout occurs while making a request to the Quip API."""


class QuipApiConnectionException(QuipSpreadsheetClientException):
    """Exception raised when a ConnectionError occurs while making a request to the Quip API."""


class QuipApiHTTPErrorException(QuipSpreadsheetClientException):
    """Exception raised when an HTTPError occurs while making a request to the Quip API."""


class QuipApiNotAJSON(QuipSpreadsheetClientException):
    """Exception raised when the response from the Quip API is not a JSON."""


class QuipUserException(QuipSpreadsheetClientException):
    """Exception raised when it's not possible to parse the current authenticated user."""


class QuipFolderException(QuipSpreadsheetClientException):
    """Exception raised when it's not possible to parse a given folder."""


class QuipThreadException(QuipSpreadsheetClientException):
    """Exception raised when it's not possible to parse a given thread."""


class QuipSpreadsheetDomParsingException(QuipSpreadsheetClientException):
    """Exception raised when it's not possible to parse the DOM of a given spreadsheet."""


class QuipSpreadsheetPageNotFoundException(QuipSpreadsheetClientException):
    """Exception raised when the the page requested does not exist in a given spreadsheet."""


@dataclass
class QuipUser:
    name: str
    id: str
    is_robot: bool
    affinity: float
    desktop_folder_id: str
    archive_folder_id: str
    starred_folder_id: str
    private_folder_id: str
    trash_folder_id: str
    shared_folder_ids: List[str]
    group_folder_ids: List[str]
    profile_picture_url: str
    subdomain: str
    url: str


@dataclass
class QuipSearchResults:
    threads: List[QuipThread] = field(default_factory=list)
    spreadsheets: List[QuipSpreadsheet] = field(default_factory=list)


class API_ROUTES(Enum):
    CURRENT_USER = "users/current"
    FOLDERS = "folders/%s"
    THREADS = "threads/%s"
    SEARCH_THREADS = "threads/search"


class QuipClient:
    def __init__(
        self,
        access_token: str,
        base_url: str,
        request_timeout: int = 10,
        logger: Any = logging.getLogger(__name__),
    ):
        self.__access_token = access_token
        self.__auth = f"Bearer {access_token}"
        self.base_url = base_url
        self.url = f"{base_url}1" if base_url.endswith("/") else f"{base_url}/1"
        self.request_timeout = request_timeout
        self.logger = logger

    def _make_request(self, path: str, kwargs: dict = {}) -> dict:
        kwargs = {
            "headers": {"Authorization": self.__auth},
            "timeout": self.request_timeout,
            **kwargs,
        }

        http_code = 0
        try:
            self.logger.debug("Making request to %s/%s.", self.base_url, path)
            res = requests.get(f"{self.url}/{path}", **kwargs)
            http_code = res.status_code
            res.raise_for_status()
            data = res.json()
        except Timeout as exc:
            self.logger.error("Timeout of %ss has been exceeded.", self.request_timeout)
            self.logger.debug(exc)
            raise QuipApiTimeoutException from exc
        except ConnectionError as exc:
            self.logger.error("A connection error occurred.")
            self.logger.debug(exc)
            raise QuipApiConnectionException from exc
        except HTTPError as exc:
            self.logger.error(
                "An HTTP Error occurred while making the request: %s.", http_code
            )
            self.logger.debug(exc)
            raise QuipApiHTTPErrorException from exc
        except JSONDecodeError as exc:
            self.logger.error("The response returned by the API is not a valid JSON.")
            self.logger.debug(exc)
            raise QuipApiNotAJSON from exc

        return data

    def get_authenticated_user(self) -> QuipUser:
        """Returns the user corresponding to our access token."""
        data = self._make_request(API_ROUTES.CURRENT_USER.value)

        try:
            user = QuipUser(**data)
        except TypeError as exc:
            self.logger.error("Unable to parse current user.")
            self.logger.debug(exc)
            raise QuipUserException from exc

        return user

    def get_folder(self, folder_id: str) -> QuipFolder:
        """Returns the folder with the given ID."""
        data = self._make_request(API_ROUTES.FOLDERS.value % folder_id)

        try:
            folder = QuipFolder(
                access_token=self.__access_token,
                base_url=self.base_url,
                request_timeout=self.request_timeout,
                logger=self.logger,
                **data.get("folder"),
                member_ids=data["member_ids"],
                children=data["children"],
            )
        except (TypeError, KeyError) as exc:
            self.logger.error("Unable to parse retrieved folder.")
            self.logger.debug(exc)
            raise QuipFolderException from exc

        return folder

    def __make_thread(self, data: Dict[str, Any]) -> Union[QuipThread, QuipSpreadsheet]:
        try:
            if "document_id" not in data.get("thread"):
                data["thread"]["document_id"] = None
            if data.get("thread").get("type") == "spreadsheet":
                return QuipSpreadsheet(
                    access_token=self.__access_token,
                    base_url=self.base_url,
                    request_timeout=self.request_timeout,
                    logger=self.logger,
                    **data.get("thread"),
                    access_levels=data.get("access_levels"),
                    expanded_user_ids=data.get("expanded_user_ids"),
                    user_ids=data.get("user_ids"),
                    shared_folder_ids=data.get("shared_folder_ids"),
                    invited_user_emails=data.get("invited_user_emails"),
                    html=data.get("html"),
                )
            else:
                return QuipThread(
                    access_token=self.__access_token,
                    base_url=self.base_url,
                    request_timeout=self.request_timeout,
                    logger=self.logger,
                    **data.get("thread"),
                    access_levels=data.get("access_levels"),
                    expanded_user_ids=data.get("expanded_user_ids"),
                    user_ids=data.get("user_ids"),
                    shared_folder_ids=data.get("shared_folder_ids"),
                    invited_user_emails=data.get("invited_user_emails"),
                    html=data.get("html"),
                )
        except (TypeError, KeyError) as exc:
            self.logger.error("Unable to parse retrieved thread.")
            self.logger.debug(exc)
            raise QuipThreadException from exc

    def get_thread(self, thread_id: str) -> Union[QuipThread, QuipSpreadsheet]:
        """Returns the thread with the given ID."""
        data = self._make_request(API_ROUTES.THREADS.value % thread_id)
        thread = self.__make_thread(data)
        return thread

    def search_threads(
        self, query: str, count: int = None, only_match_titles: bool = True
    ) -> QuipSearchResults:
        """Search threads by query."""
        params = {"query": query, "only_match_titles": only_match_titles}

        if count is not None:
            params.update({"count": count})
        data = self._make_request(API_ROUTES.SEARCH_THREADS.value, {"params": params})

        results = QuipSearchResults()
        for thread_data in data:
            search_result = self.__make_thread(thread_data)
            if isinstance(search_result, QuipSpreadsheet):
                results.spreadsheets.append(search_result)
            elif isinstance(search_result, QuipThread):
                results.threads.append(search_result)

        return results


@dataclass
class QuipFolder(QuipClient):
    access_token: str
    base_url: str
    request_timeout: int
    id: str
    title: str
    creator_id: str
    created_usec: int
    updated_usec: int
    member_ids: List[str]
    children: List[Dict[str, str]]
    logger: Any = logging.getLogger(__name__)

    def __post_init__(self):
        super().__init__(
            self.access_token, self.base_url, self.request_timeout, self.logger
        )

    def resolve_children(self):
        resolved_children = (
            list()
        )  # type: List[Union[QuipThread, QuipFolder, QuipSpreadsheet]]
        for child in self.children:
            if "folder_id" in child:
                resolved_children.append(self.get_folder(child["folder_id"]))
            elif "thread_id" in child:
                resolved_children.append(self.get_thread(child["thread_id"]))
            else:
                continue

        return resolved_children


@dataclass
class QuipThread(QuipClient):
    access_token: str
    base_url: str
    request_timeout: int
    author_id: str
    created_usec: int
    id: str
    link: str
    thread_class: str
    title: str
    type: str
    updated_usec: str
    access_levels: Optional[Dict[str, Dict[str, str]]]
    expanded_user_ids: Optional[List[str]]
    user_ids: Optional[List[str]]
    shared_folder_ids: Optional[List[str]]
    invited_user_emails: Optional[List[str]]
    document_id: Optional[str]
    html: Optional[str]
    sharing: Optional[Dict[str, Dict[str, str]]]
    owning_company_id: Optional[str]
    is_deleted: bool = False
    logger: Any = logging.getLogger(__name__)

    def __post_init__(self):
        super().__init__(
            self.access_token, self.base_url, self.request_timeout, self.logger
        )

    def load_content(self):
        data = self._make_request(API_ROUTES.THREADS.value % self.id)
        self.access_levels = data["access_levels"]
        self.expanded_user_ids = data["expanded_user_ids"]
        self.user_ids = data["user_ids"]
        self.shared_folder_ids = data["shared_folder_ids"]
        self.invited_user_emails = data["invited_user_emails"]
        self.document_id = data.get("thread")["document_id"]
        self.html = data["html"]

    def get_content(self) -> str:
        if self.html is None or len(self.html.strip()) == 0:
            self.load_content()
        if self.html is not None:
            return self.html
        else:
            raise QuipSpreadsheetClientException


class QuipPage:
    def __init__(self, node: xml.etree.ElementTree.Element, logger: Any):
        self.node = node
        self.logger = logger

    def __eq__(self, other: QuipPage) -> bool:
        return self.node == other.node

    def get_rows(self) -> List[QuipRow]:
        items = self.node.iterfind(".//tbody/tr")
        rows = list()
        for item in items:
            rows.append(QuipRow(item, self.logger))
        return rows

    def get_nth_row(self, index: int) -> QuipRow:
        """Returns the `Element` corresponding to the nth row in a given page."""
        items = self.get_rows()
        index = -1 if index == -1 else index - 1
        try:
            row = items[index]
        except (IndexError) as exc:
            self.logger.error("Row requested not found.")
            raise QuipSpreadsheetDomParsingException from exc
        return row

    def get_first_row(self) -> QuipRow:
        """Returns the `Element` corresponding to the first row in a given page."""
        return self.get_nth_row(1)

    def get_last_row(self) -> QuipRow:
        """Returns the `Element` corresponding to the last row in a given page."""
        return self.get_nth_row(-1)

    def get_row_by_content(self, content: str) -> QuipRow:
        try:
            [row] = list(self.node.iterfind("tbody/tr/td/*[.='%s']...." % content))
        except ValueError as exc:
            self.logger.error("Unable to find row with content (%s).", content)
            raise QuipSpreadsheetDomParsingException from exc
        return QuipRow(row, self.logger)


class QuipRow:
    def __init__(self, node: xml.etree.ElementTree.Element, logger: Any):
        self.node = node
        self.logger = logger
        self.index = self.__get_row_index()

    def __get_row_index(self):
        try:
            [column] = self.node.iterfind("./td[1]")
            index = int(column.text.strip())
        except ValueError as exc:
            self.logger.error("Unable to find row index.")
            raise QuipSpreadsheetDomParsingException from exc
        return index

    @staticmethod
    def _recursive_get_text(
        node: xml.etree.ElementTree.Element,
        strip: bool = True,
        separator: str = "",
    ):
        """Finds the text in a node and recursively traverses
        its children to find more text."""
        text_list = list()
        if node.text is not None and len(node.text.replace("\u200b", "").strip()) > 0:
            node_text = node.text.strip() if strip == True else node.text
            text_list.append(node_text)
        for child in node.getchildren():
            child_text_list = QuipRow._recursive_get_text(child, strip, separator)
            if len(child_text_list) > 0:
                text_list.append(child_text_list)
        return separator.join(text_list)

    def get_row_cells_content(
        self,
        include_index: bool = True,
        strip: bool = True,
        separator: str = "",
    ) -> List[str]:
        """Returns the text of items in each cell of the given row."""
        cells_content = list()
        columns = self.node.iterfind("./td")
        for column in columns:
            cells_content.append(self._recursive_get_text(column, strip, separator))

        return cells_content if include_index == True else cells_content[1:]


class QuipSpreadsheet(QuipThread):
    dom = None

    def parse_document_html(self) -> xml.etree.ElementTree.Element:
        """Returns an `Element` corresponding the Quip document HTML"""
        document_xml = f"<html>{self.get_content()}</html>"
        try:
            self.dom = xml.etree.ElementTree.fromstring(document_xml.encode("utf-8"))
        except xml.etree.ElementTree.ParseError as exc:
            self.logger.error("Unable to parse spreadsheet DOM.")
            self.logger.debug(exc)
            raise QuipSpreadsheetDomParsingException from exc
        return self.dom

    def get_named_page(self, name: str) -> QuipPage:
        """Returns an `Element` corresponding the given page,
        optionally sets is as current page."""
        if self.dom is None:
            self.dom = self.parse_document_html()
        try:
            [page] = list(self.dom.iterfind(".//table[@title='%s']" % name))
        except ValueError as exc:
            self.logger.error(
                "Unable to find page requested in spreadsheet (%s).", name
            )
            raise QuipSpreadsheetPageNotFoundException from exc

        return QuipPage(page, self.logger)

    def get_nth_page(self, index: int) -> QuipPage:
        """Returns an `Element` corresponding the nth page,
        optionally sets is as current page."""
        if self.dom is None:
            self.dom = self.parse_document_html()
        try:
            pages = list(self.dom.iterfind(".//table"))
            page = pages[index]
        except (ValueError, IndexError) as exc:
            self.logger.error(
                "Unable to find page requested in spreadsheet (%s).", index
            )
            raise QuipSpreadsheetPageNotFoundException from exc

        return QuipPage(page, self.logger)

    def get_first_page(self) -> QuipPage:
        """Returns the `Element` of the first page in the document,
        optionally sets is as current page."""
        return self.get_nth_page(0)

    def get_last_page(self) -> QuipPage:
        """Returns the `Element` of the last page in the document,
        optionally sets is as current page."""
        return self.get_nth_page(-1)
