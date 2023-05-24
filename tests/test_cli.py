"""tests.test_cli"""

from datetime import datetime, timedelta
from random import randint
from sys import maxsize
from time import time
# import re
import os
import shutil

from click.testing import CliRunner
import pytest

from starcli.__main__ import cli, CACHE_DIR, CACHED_RESULT_PATH


@pytest.mark.usefixtures("auth")
class TestCli:
    def test_cli_debug(self):
        """Test cli when --debug is passed"""
        result = self.cli_result(debug=True)
        self.assertions(result, debug=True)

    def test_cli(self):
        """Test cli when no commands given & debug+auth off"""
        result = self.cli_result(debug=False, auth="")
        self.assertions(result, debug=False)

    @pytest.mark.auth  # This test needs --auth, otherwise skip
    def test_auth(self, auth):
        """Test basic authentication for valid auth credentials"""
        result = self.cli_result(auth=auth)
        self.assertions(
            result,
            # Testing rich logger output doesn't work
            # in_stderr=("DEBUG: auth: on",),
            # not_in_stderr=("The server did not accept the credentials.",),
        )

    # def test_no_auth(self):
    #     """Test without --auth"""
    #     result = self.cli_result(auth="")
        # Testing rich logger output doesn't work
        # self.assertions(result, in_stderr=("DEBUG: auth: off",))

    # def test_incorrect_auth(self):
    #     """Test incorrect credentials provided to --auth"""
    #     result = self.cli_result(auth="github:0000")
    #     self.assertions(
    #         result,
    #         # Testing rich logger output doesn't work
    #         # in_stderr=("The server did not accept the credentials.",),
    #     )

    def test_invalid_auth_format(self):
        """Test invalid credentials provided to --auth"""
        # XXX: --auth format not checked if a cache exists
        result = self.cli_result(auth="github:", clear_cache=True, nop=True)
        self.assertions(result, in_output=("Invalid authentication format",))

        result = self.cli_result(auth=":0000", clear_cache=True, nop=True)
        self.assertions(result, in_output=("Invalid authentication format",))

        result = self.cli_result(auth="abc", clear_cache=True, nop=True)
        self.assertions(result, in_output=("Invalid authentication format",))

    def test_cli_lang(self):
        """Test cli when --lang or -l is passed"""
        param_decls = ["--lang", "-l"]

        for param in param_decls:
            result = self.cli_result(param, "python", clear_cache=False)
            self.assertions(
                result,
                # Testing rich logger output doesn't work
                # in_stderr=("language:python",),
            )

    # Until upstream github trending dependency is fixed
    @pytest.mark.xfail()
    def test_cli_spoken_language(self):
        """Test cli when --spoken-language or -S is passed"""
        param_decls = ["--spoken-language", "-S"]
        # Currently, this option uses `search_github_trending`, which produces no 'DEBUG:'
        for param in param_decls:
            result = self.cli_result(param, "en")
            self.assertions(result, debug=False)

    def test_cli_created(self):
        """Test cli when --created or -c with valid option is passed"""
        param_decls = ["--created", "-c"]

        for param in param_decls:
            date_format = "%Y-%m-%d"
            day_range = 0 - randint(100, 400)
            created_date_value = ">=" + (
                datetime.utcnow() + timedelta(days=day_range)
            ).strftime(date_format)
            result = self.cli_result(param, created_date_value)
            self.assertions(result, not_in_output=("Invalid date",))

    def test_cli_created_invalid(self):
        """Test cli when --created or -c with invalid option is passed"""
        param_decls = ["--created", "-c"]

        for param in param_decls:
            date_format = "%d-%m-%Y"
            day_range = 0 - randint(100, 400)
            created_date_value = (
                datetime.utcnow() + timedelta(days=day_range)
            ).strftime(date_format)
            result = self.cli_result(param, created_date_value)
            self.assertions(
                result,
                in_output=("Invalid date",),
            )

    def test_cli_topic(self):
        """Test cli when --topic or -t is passed"""
        param_decls = ["--topic", "-t"]

        for param in param_decls:
            result = self.cli_result(
                param, "javascript", param, "nodejs", clear_cache=False
            )  # javascript + nodejs will likely come up together
            self.assertions(result)

    def test_cli_pushed(self):
        """Test cli when --pushed or -p is passed"""
        param_decls = ["--pushed", "-p"]

        for param in param_decls:
            date_format = "%Y-%m-%d"
            day_range = 0 - randint(100, 400)
            pushed_date_value = (
                datetime.utcnow() + timedelta(days=day_range)
            ).strftime(date_format)
            result = self.cli_result(param, pushed_date_value)
            self.assertions(result, not_in_output=("Invalid date",))

    def test_cli_pushed_invalid(self):
        """Test cli when invalid option to --pushed or -p is passed"""
        param_decls = ["--pushed", "-p"]

        for param in param_decls:
            date_format = "%d-%m-%Y"
            day_range = 0 - randint(100, 400)
            pushed_date_value = (
                datetime.utcnow() + timedelta(days=day_range)
            ).strftime(date_format)
            result = self.cli_result(param, pushed_date_value, clear_cache=False)
            self.assertions(
                result,
                in_output=("Invalid date"),
            )

    def test_cli_layout(self):
        """Test cli when --layout or -L is passed"""
        param_decls = ["--layout", "-L"]
        choices = ["list", "table", "grid"]

        for param in param_decls:
            for choice in choices:
                result = self.cli_result(param, choice, clear_cache=False)
                self.assertions(result)

    def test_cli_stars(self):
        """Test cli when --stars or -s is passed"""
        param_decls = ["--stars", "-s"]

        for param in param_decls:
            result = self.cli_result(param, 0)
            self.assertions(result)

            result = self.cli_result(param, 1)
            self.assertions(result)

            result = self.cli_result(param, maxsize)
            self.assertions(result)

    def test_cli_limit_results(self):
        """Test cli when --limit-results or -r is passed"""
        param_decls = ["--limit-results", "-r"]

        for param in param_decls:
            result = self.cli_result(param, 0, clear_cache=False)
            self.assertions(result)

            result = self.cli_result(param, 1, clear_cache=False)
            self.assertions(result)

            result = self.cli_result(param, maxsize, clear_cache=False)
            self.assertions(result)

            result = self.cli_result(param, -1, clear_cache=False)
            self.assertions(result)

    def test_cli_order(self):
        """Test cli when --order or -o is passed"""
        param_decls = ["--order", "-o"]
        choices = ["desc", "asc"]

        for param in param_decls:
            for choice in choices:
                result = self.cli_result(param, choice, clear_cache=False)
                self.assertions(result)

    def test_cli_long_stats(self):
        """Test cli when --long-stats is passed"""
        result = self.cli_result("--long-stats", clear_cache=False)
        self.assertions(result)

    @pytest.mark.xfail()
    def test_cli_date_range(self):
        """Test cli when --date-range or -d is passed"""
        param_decls = ["--date-range", "-d"]
        choices = ["today", "this-week", "this-month"]
        # Currently, this option uses `search_github_trending`, which produces no 'DEBUG:'
        for param in param_decls:
            for choice in choices:
                result = self.cli_result(param, choice)
                self.assertions(result, debug=False)

    def test_cli_user(self):
        """Test cli when --user or -U is passed"""
        param_decls = ["--user", "-u"]

        for param in param_decls:
            result = self.cli_result(param, "github", clear_cache=False)
            self.assertions(result)

    def test_cached_file_existence(self):
        """Test the caching of result"""

        self.cli_result(
            "--topic", "python", "--stars", ">100", clear_cache=True, nop=False
        )

        assert os.path.exists(CACHE_DIR), f"Cache directory not created: {CACHE_DIR}"
        assert os.path.exists(
            CACHED_RESULT_PATH
        ), f"Failed to create cache file: {CACHED_RESULT_PATH}"

    def test_time_diff_for_cached_result(self):
        """Test the time difference between fetching new and cached result"""

        start = time()
        self.cli_result("--topic", "python", "--stars", ">1000", clear_cache=True)
        end = time()
        new_result_runtime = end - start

        start = time()
        self.cli_result("--topic", "python", "--stars", ">1000", clear_cache=False)
        end = time()
        cached_result_runtime = end - start

        assert (
            new_result_runtime > cached_result_runtime
        ), f"Cached result took longer ({cached_result_runtime}) than newly fetching results ({new_result_runtime})."

    def cli_result(
        self,
        *args,
        debug=True,
        auth="",
        clear_cache=True,
        nop=False,
    ):
        """
        CliRunner() helper function. Returns a `click.testing.Result` object.
        Passes `--debug` by default. Passes `--auth` + credentials, if given.

        Also clear the cache if needed.
        """
        if clear_cache:
            try:
                shutil.rmtree(CACHE_DIR)
            except FileNotFoundError:
                pass

        runner = CliRunner()
        cli_params = list(args)

        if auth:
            cli_params.extend(["--auth", auth])
        elif self.auth:
            cli_params.extend(["--auth", self.auth])

        if debug:
            cli_params.append("--debug")

        if nop:
            cli_params.append("--nop")


        return runner.invoke(cli, cli_params) if cli_params else runner.invoke(cli)

    def assertions(
        self,
        result,
        exit_code=0,
        output=True,
        debug=True,
        in_output=(),
        not_in_output=(),
        in_stderr=(),
        not_in_stderr=(),
    ):
        """
        Helper function for basic assert statements.
        """
        if exit_code:
            assert result.exit_code == exit_code, f"`exit_code` should be '{exit_code}'"
        # if debug: # logs aren't captured in result.output so it doesn't work
        # assert "DEBUG" in result.output, f"'DEBUG' not in `result.output`"
        if output and not debug:
            assert result.output, "No cli output generated"
        elif not output:
            assert not result.output, "Cli output generated, but expected nothing"

        if in_output:
            for s in in_output:
                assert s in result.output, f"'{s}' not found in `result.output.`"
        if not_in_output:
            for s in not_in_output:
                assert (
                    not s in result.output
                ), f"{s} found in `result.output`, but shouldn't be."
        if in_stderr:
            for s in in_stderr:
                assert s in result.stderr, f"{s} not in `result.stderr`"
        if not_in_stderr:
            for s in not_in_stderr:
                assert not s in result.stderr, f"{s} shouldn't be in stderr"
