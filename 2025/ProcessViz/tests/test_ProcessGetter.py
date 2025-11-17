import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import psutil
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.ProcessGetter import ProcessGetter
from app.config_loader import get_config


@pytest_asyncio.fixture(scope="module")
async def config():
    return await get_config()


@pytest.mark.asyncio
async def test_config_loaded(config):
    assert isinstance(config, dict)
    assert "paths" in config


@pytest.mark.asyncio
@patch("app.ProcessGetter.grab_sha256_async", new_callable=AsyncMock)
async def test_no_such_process(mock_hash, config):
    process_pid = 1234
    mock_hash.return_value = "fakehash123"

    mock_proc_instance = MagicMock()
    mock_proc_instance.as_dict.return_value = {
        "name": "malicious.exe",
        "memory_percent": 12.5,
        "exe": (config["paths"]["suspicious"][0] + "\\malicious.exe").lower(),
        "create_time": 1630000000.0,
        "status": "running",
        "ppid": 1,
    }

    mock_proc_instance.parent.side_effect = psutil.NoSuchProcess(pid=1234)

    mock_conn = MagicMock()
    mock_conn.raddr = ("192.168.1.42", 443)
    mock_conn.laddr = ("127.0.0.1", 1234)
    mock_conn.status = "ESTABLISHED"

    mock_proc_instance.net_connections.return_value = [mock_conn]

    result = await ProcessGetter.fetch_infos_for_process(
        mock_proc_instance, process_pid
    )

    assert result is not None
    assert result["parent"] is None
    assert result["name"] == "malicious.exe"
    assert result["hash"] == "fakehash123"


@pytest.mark.asyncio
@patch("app.ProcessGetter.grab_sha256_async", new_callable=AsyncMock)
async def test_mock_grab_sha256_async(mock_hash):
    mock_hash.return_value = "fakehash123"
    result = await mock_hash()
    assert result == "fakehash123"


@pytest.mark.asyncio
@patch("app.ProcessGetter.psutil.Process")
@patch("app.ProcessGetter.grab_sha256_async", new_callable=AsyncMock)
async def test_fetch_infos_for_process(mock_hash, mock_process_class, config):
    process_pid = 1234
    mock_hash.return_value = "fakehash123"

    mock_proc_instance = MagicMock()
    mock_proc_instance.as_dict.return_value = {
        "name": "malicious.exe",
        "memory_percent": 12.5,
        "exe": (config["paths"]["suspicious"][0] + "\\malicious.exe").lower(),
        "create_time": 1630000000.0,
        "status": "running",
        "ppid": 1,
    }

    mock_parent = MagicMock()
    mock_parent.name.return_value = "explorer.exe"
    mock_proc_instance.parent.return_value = mock_parent

    mock_conn = MagicMock()
    mock_conn.raddr = ("192.168.1.42", 443)
    mock_conn.laddr = ("127.0.0.1", 1234)
    mock_conn.status = "ESTABLISHED"

    mock_proc_instance.net_connections.return_value = [mock_conn]

    mock_process_class.return_value = mock_proc_instance
    result = await ProcessGetter.fetch_infos_for_process(
        mock_proc_instance, process_pid
    )

    assert isinstance(result, dict)
    assert result["name"] == "malicious.exe"
    assert result["PID"] == process_pid
    assert result["path"].endswith("malicious.exe")
    assert result["status"] == "running"
    assert result["parent"] == "explorer.exe"
    assert result["hash"] == "fakehash123"
    assert result["memory_percent"] == 12.5
    assert isinstance(result["connections"], list)
    assert any("192.168.1.42:443" in conn for conn in result["connections"])


@pytest.mark.asyncio
@patch(
    "app.ProcessGetter.ProcessGetter.fetch_infos_for_process", new_callable=AsyncMock
)
@patch("app.ProcessGetter.psutil.Process")
@patch("app.ProcessGetter.psutil.pids")
async def test_get_processes_success(mock_pids, mock_process_class, mock_fetch):
    mock_pids.return_value = [123, 456]
    mock_proc1 = MagicMock()
    mock_proc2 = MagicMock()
    mock_process_class.side_effect = [mock_proc1, mock_proc2]

    mock_fetch.side_effect = [{"name": "proc1"}, {"name": "proc2"}]

    result = await ProcessGetter.get_processes()

    assert isinstance(result, dict)
    assert len(result) == 2
    assert result[123]["name"] == "proc1"
    assert result[456]["name"] == "proc2"

    mock_pids.assert_called_once()
    assert mock_process_class.call_count == 2
    assert mock_fetch.call_count == 2


@pytest.mark.asyncio
@patch(
    "app.ProcessGetter.ProcessGetter.fetch_infos_for_process", new_callable=AsyncMock
)
@patch("app.ProcessGetter.psutil.Process")
@patch("app.ProcessGetter.psutil.pids")
async def test_get_processes_with_errors(
    mock_pids, mock_process_class, mock_fetch_infos
):
    mock_pids.return_value = [123, 456, 789]

    mock_proc1 = MagicMock()
    mock_proc2 = MagicMock()
    mock_proc3 = MagicMock()
    mock_process_class.side_effect = [mock_proc1, mock_proc2, mock_proc3]

    # Simule une exception pour le second PID
    mock_fetch_infos.side_effect = [
        {"name": "proc1"},
        psutil.AccessDenied(pid=456),
        {"name": "proc3"},
    ]

    result = await ProcessGetter.get_processes()

    assert 123 in result
    assert 456 not in result  # Erreur => ignoré
    assert 789 in result
    assert len(result) == 2


@pytest.mark.asyncio
async def test_fetch_infos_for_process_with_opened_files(config):
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

    with patch(
        "app.ProcessGetter.psutil.Process", return_value=mock_proc_instance
    ), patch(
        "app.utils.utils_process.get_dll_info_sync",
        return_value=["dll1.dll", "dll2.dll"],
    ), patch(
        "app.ProcessGetter.grab_sha256_async", return_value="fakehash123"
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
