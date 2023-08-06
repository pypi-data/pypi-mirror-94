import os
import unittest
from copy import deepcopy
from xml.etree.ElementTree import Element

import requests_mock
from requests.exceptions import ConnectTimeout, ConnectionError

from quip.quip import (
    QuipClient,
    QuipPage,
    QuipRow,
    QuipSearchResults,
    QuipSpreadsheetClientException,
    API_ROUTES,
    QuipUser,
    QuipFolder,
    QuipThread,
    QuipSpreadsheet,
    QuipApiHTTPErrorException,
    QuipApiTimeoutException,
    QuipApiConnectionException,
    QuipApiNotAJSON,
    QuipUserException,
    QuipFolderException,
    QuipThreadException,
    QuipSpreadsheetDomParsingException,
    QuipSpreadsheetPageNotFoundException,
)

from tests.constants import (
    QUIP_ACCESS_TOKEN,
    QUIP_BASE_URL,
    LOGS_PREFIX,
    USER_JSON,
    FOLDER_JSON,
    THREAD_JSON,
    SPREADSHEET_CONTENT,
)


class TestQuipClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        if os.getenv("ENV") is not None:
            del os.environ["ENV"]

    def setUp(self) -> None:
        self.quip = QuipClient(QUIP_ACCESS_TOKEN, QUIP_BASE_URL, 5)

    def tearDown(self) -> None:
        del self.quip

    def test_init(self):
        self.assertEqual(
            f"Bearer {QUIP_ACCESS_TOKEN}", self.quip._QuipClient__auth  # type: ignore
        )
        self.assertEqual(f"{QUIP_BASE_URL}/1", self.quip.url)
        self.assertEqual(5, self.quip.request_timeout)

    @requests_mock.Mocker(kw="mock")
    def test__make_request(self, **kwargs):
        kwargs["mock"].get(f"{QUIP_BASE_URL}/1/", status_code=500)

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipApiHTTPErrorException):
                self.quip._make_request("")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}An HTTP Error occurred while making the request: 500.",
            )

        kwargs["mock"].get(f"{QUIP_BASE_URL}/1/", exc=ConnectTimeout)

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipApiTimeoutException):
                self.quip._make_request("")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Timeout of 5s has been exceeded.",
            )

        kwargs["mock"].get(f"{QUIP_BASE_URL}/1/", exc=ConnectionError)

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipApiConnectionException):
                self.quip._make_request("")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}A connection error occurred.",
            )

        kwargs["mock"].get(f"{QUIP_BASE_URL}/1/", content=b"abc")

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipApiNotAJSON):
                self.quip._make_request("")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}The response returned by the API is not a valid JSON.",
            )

        kwargs["mock"].get(f"{QUIP_BASE_URL}/1/", json={"Hello": "World"})

        data = self.quip._make_request("")

        self.assertDictEqual(data, {"Hello": "World"})

    @requests_mock.Mocker(kw="mock")
    def test_get_authenticated_user(self, **kwargs):
        wrong_user = deepcopy(USER_JSON)
        del wrong_user["id"]
        wrong_user["user_id"] = "1234"
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.CURRENT_USER.value}", json=wrong_user
        )

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipUserException):
                self.quip.get_authenticated_user()

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Unable to parse current user.",
            )

        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.CURRENT_USER.value}", json=USER_JSON
        )
        expected_user = QuipUser(**USER_JSON)
        user = self.quip.get_authenticated_user()

        self.assertEqual(expected_user.name, user.name)
        self.assertEqual(expected_user.id, user.id)
        self.assertEqual(expected_user.is_robot, user.is_robot)
        self.assertEqual(expected_user.affinity, user.affinity)
        self.assertEqual(expected_user.desktop_folder_id, user.desktop_folder_id)
        self.assertEqual(expected_user.archive_folder_id, user.archive_folder_id)
        self.assertEqual(expected_user.starred_folder_id, user.starred_folder_id)
        self.assertEqual(expected_user.private_folder_id, user.private_folder_id)
        self.assertEqual(expected_user.trash_folder_id, user.trash_folder_id)
        self.assertEqual(expected_user.shared_folder_ids, user.shared_folder_ids)
        self.assertEqual(expected_user.group_folder_ids, user.group_folder_ids)
        self.assertEqual(expected_user.profile_picture_url, user.profile_picture_url)
        self.assertEqual(expected_user.subdomain, user.subdomain)
        self.assertEqual(expected_user.url, user.url)

    @requests_mock.Mocker(kw="mock")
    def test_get_folder(self, **kwargs):
        wrong_folder = deepcopy(FOLDER_JSON)
        del wrong_folder["member_ids"]
        wrong_folder["members"] = "1234"
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.FOLDERS.value}" % "abc1234",
            json=wrong_folder,
        )

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipFolderException):
                self.quip.get_folder("abc1234")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Unable to parse retrieved folder.",
            )

        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.FOLDERS.value}" % "abc1234",
            json=FOLDER_JSON,
        )
        expected_folder = QuipFolder(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            logger=object,
            **FOLDER_JSON.get("folder"),
            member_ids=FOLDER_JSON["member_ids"],
            children=FOLDER_JSON["children"],
        )
        folder = self.quip.get_folder("abc1234")

        self.assertEqual(expected_folder.id, folder.id)
        self.assertEqual(expected_folder.title, folder.title)
        self.assertEqual(expected_folder.creator_id, folder.creator_id)
        self.assertEqual(expected_folder.created_usec, folder.created_usec)
        self.assertEqual(expected_folder.updated_usec, folder.updated_usec)
        self.assertListEqual(expected_folder.member_ids, folder.member_ids)
        self.assertListEqual(expected_folder.children, folder.children)

    @requests_mock.Mocker(kw="mock")
    def test_get_thread(self, **kwargs):
        wrong_thread = deepcopy(THREAD_JSON)
        del wrong_thread["thread"]["id"]
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}" % "abc1234",
            json=wrong_thread,
        )

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipThreadException):
                self.quip.get_thread("abc1234")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Unable to parse retrieved thread.",
            )

        not_a_spreadsheet_thread = deepcopy(THREAD_JSON)
        not_a_spreadsheet_thread["thread"]["type"] = "something_else"
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}" % "abc1234",
            json=not_a_spreadsheet_thread,
        )

        thread = self.quip.get_thread("abc1234")

        self.assertIsInstance(thread, QuipThread)

        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}" % "abc1234",
            json=THREAD_JSON,
        )
        expected_thread = QuipSpreadsheet(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=THREAD_JSON["access_levels"],
            expanded_user_ids=THREAD_JSON["expanded_user_ids"],
            user_ids=THREAD_JSON["user_ids"],
            shared_folder_ids=THREAD_JSON["shared_folder_ids"],
            invited_user_emails=THREAD_JSON["invited_user_emails"],
            html=THREAD_JSON["html"],
        )
        thread = self.quip.get_thread("abc1234")

        self.assertIsInstance(thread, QuipSpreadsheet)
        self.assertEqual(expected_thread.author_id, thread.author_id)
        self.assertEqual(expected_thread.created_usec, thread.created_usec)
        self.assertEqual(expected_thread.document_id, thread.document_id)
        self.assertEqual(expected_thread.id, thread.id)
        self.assertEqual(expected_thread.is_deleted, thread.is_deleted)
        self.assertEqual(expected_thread.link, thread.link)
        self.assertEqual(expected_thread.thread_class, thread.thread_class)
        self.assertEqual(expected_thread.title, thread.title)
        self.assertEqual(expected_thread.type, thread.type)
        self.assertEqual(expected_thread.updated_usec, thread.updated_usec)
        self.assertDictEqual(expected_thread.access_levels, thread.access_levels)  # type: ignore
        self.assertListEqual(
            expected_thread.expanded_user_ids, thread.expanded_user_ids  # type: ignore
        )
        self.assertListEqual(expected_thread.user_ids, thread.user_ids)  # type: ignore
        self.assertListEqual(
            expected_thread.shared_folder_ids, thread.shared_folder_ids  # type: ignore
        )
        self.assertListEqual(
            expected_thread.invited_user_emails, thread.invited_user_emails  # type: ignore
        )
        self.assertEqual(expected_thread.html, thread.html)

    @requests_mock.Mocker(kw="mock")
    def test_search_thread(self, **kwargs):
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.SEARCH_THREADS.value}",
            json=[THREAD_JSON],
        )

        results = self.quip.search_threads("My", 1)
        self.assertIsInstance(results, QuipSearchResults)
        self.assertIsInstance(results.spreadsheets[0], QuipSpreadsheet)


class TestQuipFolder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        if os.getenv("ENV") is not None:
            del os.environ["ENV"]

    @requests_mock.Mocker(kw="mock")
    def test_resolve_children(self, **kwargs):
        one_thread = deepcopy(THREAD_JSON)
        one_thread["thread"]["id"] = "abc1234"
        kwargs["mock"].register_uri(
            "GET",
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}"
            % one_thread.get("thread").get("id"),
            json=one_thread,
        )
        other_thread = deepcopy(THREAD_JSON)
        other_thread["thread"]["id"] = "abc5678"
        kwargs["mock"].register_uri(
            "GET",
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}"
            % other_thread.get("thread").get("id"),
            json=other_thread,
        )

        folder_w_threads = QuipFolder(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **FOLDER_JSON.get("folder"),
            member_ids=FOLDER_JSON["member_ids"],
            children=[
                {"thread_id": one_thread.get("thread").get("id")},
                {"thread_id": other_thread.get("thread").get("id")},
            ],
        )
        threads = folder_w_threads.resolve_children()

        self.assertIsInstance(threads[0], QuipThread)
        self.assertEqual(threads[0].id, one_thread.get("thread").get("id"))
        self.assertIsInstance(threads[1], QuipThread)
        self.assertEqual(threads[1].id, other_thread.get("thread").get("id"))

        one_folder = deepcopy(FOLDER_JSON)
        one_folder["folder"]["id"] = "abc1234"
        kwargs["mock"].register_uri(
            "GET",
            f"{QUIP_BASE_URL}/1/{API_ROUTES.FOLDERS.value}"
            % one_folder.get("folder").get("id"),
            json=one_folder,
        )
        other_folder = deepcopy(FOLDER_JSON)
        other_folder["folder"]["id"] = "abc5678"
        kwargs["mock"].register_uri(
            "GET",
            f"{QUIP_BASE_URL}/1/{API_ROUTES.FOLDERS.value}"
            % other_folder.get("folder").get("id"),
            json=other_folder,
        )

        folder_w_folders = QuipFolder(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **FOLDER_JSON.get("folder"),
            member_ids=FOLDER_JSON["member_ids"],
            children=[
                {"folder_id": one_folder.get("folder").get("id")},
                {"folder_id": other_folder.get("folder").get("id")},
            ],
        )
        folders = folder_w_folders.resolve_children()

        self.assertIsInstance(folders[0], QuipFolder)
        self.assertEqual(folders[0].id, one_folder.get("folder").get("id"))
        self.assertIsInstance(folders[1], QuipFolder)
        self.assertEqual(folders[1].id, other_folder.get("folder").get("id"))

        folder_w_both = QuipFolder(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **FOLDER_JSON.get("folder"),
            member_ids=FOLDER_JSON["member_ids"],
            children=[
                {"folder_id": one_folder.get("folder").get("id")},
                {"thread_id": one_thread.get("thread").get("id")},
            ],
        )
        folders_n_threads = folder_w_both.resolve_children()

        self.assertIsInstance(folders_n_threads[0], QuipFolder)
        self.assertEqual(folders_n_threads[0].id, one_folder.get("folder").get("id"))
        self.assertIsInstance(folders_n_threads[1], QuipThread)
        self.assertEqual(folders_n_threads[1].id, one_thread.get("thread").get("id"))


class TestQuipThread(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        if os.getenv("ENV") is not None:
            del os.environ["ENV"]

    @requests_mock.Mocker(kw="mock")
    def test_get_content(self, **kwargs):
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}"
            % THREAD_JSON.get("thread").get("id"),
            exc=ConnectionError,
        )
        thread = QuipThread(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=THREAD_JSON["access_levels"],
            expanded_user_ids=THREAD_JSON["expanded_user_ids"],
            user_ids=THREAD_JSON["user_ids"],
            shared_folder_ids=THREAD_JSON["shared_folder_ids"],
            invited_user_emails=THREAD_JSON["invited_user_emails"],
            html=THREAD_JSON["html"],
        )
        self.assertEqual(thread.get_content(), THREAD_JSON["html"])

        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}"
            % THREAD_JSON.get("thread").get("id"),
            json=THREAD_JSON,
        )
        other_thread = QuipThread(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=None,
            expanded_user_ids=None,
            user_ids=None,
            shared_folder_ids=None,
            invited_user_emails=None,
            html=None,
        )

        self.assertEqual(other_thread.get_content(), THREAD_JSON["html"])

    @requests_mock.Mocker(kw="mock")
    def test_load_content(self, **kwargs):
        kwargs["mock"].get(
            f"{QUIP_BASE_URL}/1/{API_ROUTES.THREADS.value}"
            % THREAD_JSON.get("thread").get("id"),
            json=THREAD_JSON,
        )
        original_thread = deepcopy(THREAD_JSON)
        original_thread["thread"]["document_id"] = None
        thread = QuipThread(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **original_thread.get("thread"),
            access_levels=None,
            expanded_user_ids=None,
            user_ids=None,
            shared_folder_ids=None,
            invited_user_emails=None,
            html=None,
        )
        thread.load_content()

        self.assertEqual(thread.access_levels, THREAD_JSON["access_levels"])
        self.assertListEqual(
            thread.expanded_user_ids, THREAD_JSON["expanded_user_ids"]  # type: ignore
        )
        self.assertListEqual(thread.user_ids, THREAD_JSON["user_ids"])  # type: ignore
        self.assertListEqual(
            thread.shared_folder_ids, THREAD_JSON["shared_folder_ids"]  # type: ignore
        )
        self.assertListEqual(
            thread.invited_user_emails, THREAD_JSON["invited_user_emails"]  # type: ignore
        )
        self.assertEqual(thread.document_id, THREAD_JSON["thread"]["document_id"])


class TestQuipSpreadsheet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        if os.getenv("ENV") is not None:
            del os.environ["ENV"]

    def setUp(self) -> None:
        self.spreadsheet = QuipSpreadsheet(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=THREAD_JSON["access_levels"],
            expanded_user_ids=THREAD_JSON["expanded_user_ids"],
            user_ids=THREAD_JSON["user_ids"],
            shared_folder_ids=THREAD_JSON["shared_folder_ids"],
            invited_user_emails=THREAD_JSON["invited_user_emails"],
            html=SPREADSHEET_CONTENT,
        )

    def tearDown(self) -> None:
        self.spreadsheet = None

    def test_parse_document_html(self):
        dom = self.spreadsheet.parse_document_html()

        self.assertIsInstance(dom, Element)
        self.assertEqual(dom.getchildren()[0].tag, "h1")
        self.assertEqual(dom.getchildren()[1].getchildren()[0].tag, "table")

        spreadsheet = QuipSpreadsheet(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=THREAD_JSON["access_levels"],
            expanded_user_ids=THREAD_JSON["expanded_user_ids"],
            user_ids=THREAD_JSON["user_ids"],
            shared_folder_ids=THREAD_JSON["shared_folder_ids"],
            invited_user_emails=THREAD_JSON["invited_user_emails"],
            html="<<</",
        )

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipSpreadsheetDomParsingException):
                dom = spreadsheet.parse_document_html()

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Unable to parse spreadsheet DOM.",
            )

    def test_get_named_page(self):
        page = self.spreadsheet.get_named_page("Sheet1")

        self.assertIsInstance(page, QuipPage)

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipSpreadsheetPageNotFoundException):
                self.spreadsheet.get_named_page("Sheet2")

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Unable to find page requested in spreadsheet (Sheet2).",
            )

    def test_get_page_by_index(self):
        first_page = self.spreadsheet.get_first_page()

        self.assertIsInstance(first_page, QuipPage)

        last_page = self.spreadsheet.get_last_page()

        self.assertEqual(first_page, last_page)

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipSpreadsheetPageNotFoundException):
                self.spreadsheet.get_nth_page(2)

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Unable to find page requested in spreadsheet (2).",
            )


class TestQuipPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        if os.getenv("ENV") is not None:
            del os.environ["ENV"]

    def setUp(self) -> None:
        self.spreadsheet = QuipSpreadsheet(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=THREAD_JSON["access_levels"],
            expanded_user_ids=THREAD_JSON["expanded_user_ids"],
            user_ids=THREAD_JSON["user_ids"],
            shared_folder_ids=THREAD_JSON["shared_folder_ids"],
            invited_user_emails=THREAD_JSON["invited_user_emails"],
            html=SPREADSHEET_CONTENT,
        )
        self.page = self.spreadsheet.get_named_page("Sheet1")

    def tearDown(self) -> None:
        self.spreadsheet = None
        self.page = None

    def test_get_row_by_index(self):
        first_row = self.page.get_first_row()

        self.assertIsInstance(first_row, QuipRow)
        self.assertEqual(first_row.node.getchildren()[0].text, "1")

        last_row = self.page.get_last_row()

        self.assertIsInstance(last_row, QuipRow)
        self.assertEqual(last_row.node.getchildren()[0].text, "3")

        nth_row = self.page.get_nth_row(1)

        self.assertIsInstance(nth_row, QuipRow)
        self.assertEqual(nth_row.node.getchildren()[0].text, "1")

        with self.assertLogs(level="ERROR") as context_mngr:
            with self.assertRaises(QuipSpreadsheetDomParsingException):
                self.page.get_nth_row(5)

            self.assertEqual(
                context_mngr.output[0],
                f"ERROR{LOGS_PREFIX}Row requested not found.",
            )

    def test_get_row_by_content(self):
        row = self.page.get_row_by_content("TECH TRACK")

        self.assertIsInstance(row, QuipRow)
        self.assertEqual(row.index, 1)


class TestQuipRow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        if os.getenv("ENV") is not None:
            del os.environ["ENV"]

    def setUp(self) -> None:
        self.spreadsheet = QuipSpreadsheet(
            QUIP_ACCESS_TOKEN,
            QUIP_BASE_URL,
            request_timeout=10,
            **THREAD_JSON.get("thread"),
            access_levels=THREAD_JSON["access_levels"],
            expanded_user_ids=THREAD_JSON["expanded_user_ids"],
            user_ids=THREAD_JSON["user_ids"],
            shared_folder_ids=THREAD_JSON["shared_folder_ids"],
            invited_user_emails=THREAD_JSON["invited_user_emails"],
            html=SPREADSHEET_CONTENT,
        )
        self.page = self.spreadsheet.get_named_page("Sheet1")

    def tearDown(self) -> None:
        self.spreadsheet = None
        self.page = None

    def test_get_row_cells_content(self):
        row = self.page.get_nth_row(2)
        cells = row.get_row_cells_content()

        self.assertTrue(len(cells), 8)
        self.assertListEqual(
            cells,
            ["2", "", "Date", "Title", "Location", "Language", "Capacity", "Owner"],
        )

        cells = row.get_row_cells_content(include_index=False)
        self.assertTrue(len(cells), 7)
        self.assertListEqual(
            cells,
            ["", "Date", "Title", "Location", "Language", "Capacity", "Owner"],
        )


if __name__ == "__main__":
    unittest.main()