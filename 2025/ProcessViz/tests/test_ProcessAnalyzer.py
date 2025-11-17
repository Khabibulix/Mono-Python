import pytest
import pytest_asyncio
import psutil
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from unittest.mock import patch, MagicMock, AsyncMock
from app.ProcessAnalyzer import ProcessAnalyzer
from app.ProcessGetter import ProcessGetter
from app.config_loader import get_config
from app.utils.utils_score import MAX_SCORE
from app.utils.utils import normalizing_score


@pytest_asyncio.fixture(scope="module")
async def config():
    return await get_config()


@pytest.mark.asyncio
async def test_config_loaded(config):
    assert isinstance(config, dict)
    assert "paths" in config


@pytest.mark.asyncio
@patch("app.utils.utils_score.psutil.pid_exists", return_value=False)
async def test_run_pid_not_exists(mock_pid_exists):
    analyzer = ProcessAnalyzer(99999)
    result = await analyzer.run()
    assert result is None


@pytest.mark.asyncio
@patch("app.utils.utils_score.psutil.pid_exists", return_value=True)
@patch(
    "app.utils.utils_score.psutil.Process", side_effect=psutil.AccessDenied(pid=1234)
)
async def test_access_denied(mock_process, mock_pid_exists):
    analyzer = ProcessAnalyzer(1234)
    result = await analyzer.run()
    assert result is None
    mock_pid_exists.assert_called_once_with(1234)
    mock_process.assert_called_once_with(1234)


@pytest.mark.asyncio
async def test_suspicious_path(config):
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = (
            config["paths"]["suspicious"][0] + "\\malicious.exe"
        ).lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    expected_score = normalizing_score(20, MAX_SCORE)
    assert result["score"] == expected_score
    assert result["justifications"].get("path_suspicious", False)
    assert result["raw_metrics"]["path_suspicious"]


@pytest.mark.asyncio
async def test_trustworthy_path(config):
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = (
            config["paths"]["trustworthy"][0] + "\\malicious.exe"
        ).lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    expected_score = normalizing_score(config["weights"]["trustworthy_path"], MAX_SCORE)
    assert result["score"] == expected_score
    assert result["justifications"].get("path_trustworthy") is True
    assert result["raw_metrics"]["path_trustworthy"] is True


@pytest.mark.asyncio
async def test_executable_is_not_signed_gets_30_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=False
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(30, 135)
    assert "is_signed" in result["justifications"]
    assert not result["raw_metrics"]["is_signed"]


@pytest.mark.asyncio
async def test_executable_is_signed_gets_0_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(0, 135)
    assert "is_signed" not in result["justifications"]
    assert result["raw_metrics"]["is_signed"]


@pytest.mark.asyncio
async def test_executable_is_signed_gets_0_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=True
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(15, 135)
    assert "path_deleted" in result["justifications"]
    assert result["raw_metrics"]["path_deleted"]


@pytest.mark.asyncio
async def test_executable_contains_strange_chars_gets_15_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("C:\\weird\\µ$\\script.exe").lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(15, 135)
    assert "strange_chars" in result["justifications"]
    assert result["raw_metrics"]["strange_chars"]


@pytest.mark.asyncio
async def test_executable_connects_to_internet_and_gets_20_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ("192.168.1.42", 443)
        mock_conn.status = "ESTABLISHED"

        mock_proc_instance.net_connections.return_value = [mock_conn]

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(20, 135)
    assert "network_active" in result["justifications"]
    assert result["raw_metrics"]["network_active"]


@pytest.mark.asyncio
async def test_executable_connects_to_internet_with_wait_status_and_gets_0_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ("192.168.1.42", 443)
        mock_conn.status = "CLOSE_WAIT"

        mock_proc_instance.net_connections.return_value = [mock_conn]

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(0, 135)
    assert "network_active" not in result["justifications"]
    assert not result["raw_metrics"]["network_active"]


@pytest.mark.asyncio
async def test_net_connections_access_denied_gracefully_handled():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance
        mock_proc_instance.net_connections.side_effect = psutil.AccessDenied(1234)
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result is not None
    assert result["score"] == normalizing_score(0, 135)
    assert "network_active" not in result["justifications"]


@pytest.mark.asyncio
async def test_executable_not_connects_to_internet_and_gets_0_points():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=True
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=False
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance
        mock_proc_instance.net_connections.return_value = []

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(0, 135)
    assert "network_active" not in result["justifications"]
    assert not result["raw_metrics"]["network_active"]


@pytest.mark.asyncio
async def test_executable_is_score_normalized_correctly_and_risk_level_ok():
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=False
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=True
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=True
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=False
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ("192.168.1.42", 443)
        mock_conn.status = "ESTABLISHED"

        mock_proc_instance.net_connections.return_value = [mock_conn]

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert normalizing_score(result["score"], 135) == 39
    assert all(
        key in result["justifications"]
        for key in ("is_signed", "invokes_python", "network_active")
    )
    assert "warning" in result["risk_level"]


@pytest.mark.asyncio
async def test_executable_is_critical_risk_level(config):
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process, patch(
        "app.utils.utils_score.is_signed", return_value=False
    ), patch(
        "app.utils.utils_score.is_invocating_scripts", return_value=True
    ), patch(
        "app.utils.utils_score.is_process_bound_to_a_service", return_value=False
    ), patch(
        "app.utils.utils_score.is_deleted_executable", return_value=True
    ):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = (
            config["paths"]["suspicious"][0] + "\\malicious.exe"
        ).lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ("192.168.1.42", 443)
        mock_conn.status = "ESTABLISHED"

        mock_proc_instance.net_connections.return_value = [mock_conn]

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert normalizing_score(result["score"], 135) == 66
    assert "critical" in result["risk_level"]


@pytest.mark.asyncio
async def test_process_exe_access_denied(config):
    with patch("app.utils.utils_score.psutil.pid_exists", return_value=True), patch(
        "app.utils.utils_score.psutil.Process"
    ) as mock_process_class:

        # Cas exe AccessDenied
        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.side_effect = psutil.AccessDenied(1234)
        mock_process_class.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()
        assert result is None

        # Cas fetch_infos_for_process
        process_pid = 5678
        mock_proc_instance = MagicMock()
        mock_proc_instance.as_dict.return_value = {
            "name": "trusted.exe",
            "memory_percent": 3.14,
            "exe": (config["paths"]["trustworthy"][0] + "\\trusted.exe").lower(),
            "create_time": 1630000000.0,
            "status": "sleeping",
            "ppid": 2,
        }
        mock_proc_instance.parent.return_value.name.return_value = "explorer.exe"
        mock_proc_instance.net_connections.return_value = []

        mock_process_class.return_value = mock_proc_instance

        with patch(
            "app.ProcessGetter.grab_sha256_async", return_value="fakehash123"
        ), patch(
            "app.utils.utils_process.get_dll_info_sync",
            return_value=["dll1.dll", "dll2.dll"],
        ):
            result = await ProcessGetter.fetch_infos_for_process(
                mock_proc_instance, process_pid, include_opened_files=True
            )

        assert result["name"] == "trusted.exe"
        assert result["PID"] == process_pid
        assert result["path"].endswith("trusted.exe")
        assert result["opened_dll"] == ["dll1.dll", "dll2.dll"]
        assert result["connections"] is None
        assert result["memory_percent"] == 3.14
