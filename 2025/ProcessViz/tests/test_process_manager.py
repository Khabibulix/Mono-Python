import pytest
import pytest_asyncio
import psutil
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from unittest.mock import patch, MagicMock, AsyncMock
from process_manager import ProcessAnalyzer, MAX_SCORE, ProcessGetter
from config_loader import get_config
from utils import normalizing_score

@pytest_asyncio.fixture(scope="module")
async def config():
    return await get_config()

@pytest.mark.asyncio
async def test_config_loaded(config):
    assert isinstance(config, dict)
    assert "paths" in config

@pytest.mark.asyncio
@patch('process_manager.psutil.pid_exists', return_value=False)
async def test_run_pid_not_exists(mock_pid_exists):
    analyzer = ProcessAnalyzer(99999)
    result = await analyzer.run()
    assert result is None

@pytest.mark.asyncio
@patch('process_manager.psutil.pid_exists', return_value=True)
@patch('process_manager.psutil.Process', side_effect=psutil.AccessDenied(pid=1234))
async def test_access_denied(mock_process, mock_pid_exists):
    analyzer = ProcessAnalyzer(1234)
    result = await analyzer.run()
    assert result is None
    mock_pid_exists.assert_called_once_with(1234)
    mock_process.assert_called_once_with(1234)

@pytest.mark.asyncio
@patch('process_manager.grab_sha256_async', new_callable=AsyncMock)
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
        "ppid": 1
    }

    mock_proc_instance.parent.side_effect = psutil.NoSuchProcess(pid=1234)

    mock_conn = MagicMock()
    mock_conn.raddr = ('192.168.1.42', 443)
    mock_conn.laddr = ('127.0.0.1', 1234)
    mock_conn.status = 'ESTABLISHED'

    mock_proc_instance.net_connections.return_value = [mock_conn]

    result = await ProcessGetter.fetch_infos_for_process(mock_proc_instance, process_pid)

    assert result is not None
    assert result["parent"] is None
    assert result["name"] == "malicious.exe"
    assert result["hash"] == "fakehash123"


@pytest.mark.asyncio
async def test_suspicious_path(config):
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):
        
        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = (config["paths"]["suspicious"][0] + "\\malicious.exe").lower()
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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=True), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):
        
        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = (config["paths"]["trustworthy"][0] + "\\malicious.exe").lower()
        mock_proc_instance.net_connections.return_value = []
        mock_process.return_value = mock_proc_instance

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    expected_score = normalizing_score(0, MAX_SCORE)
    assert result["score"] == expected_score
    assert result["justifications"].get("path_trustworthy", True)
    assert result["raw_metrics"]["path_trustworthy"]

@pytest.mark.asyncio
async def test_executable_is_not_signed_gets_30_points():
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=False), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=True):

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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ('192.168.1.42', 443)
        mock_conn.status = 'ESTABLISHED'

        mock_proc_instance.net_connections.return_value = [mock_conn]
        


        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(20, 135)
    assert "network_active" in result["justifications"]
    assert result["raw_metrics"]["network_active"]

@pytest.mark.asyncio
async def test_executable_connects_to_internet_with_wait_status_and_gets_0_points():
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ('192.168.1.42', 443)
        mock_conn.status = 'CLOSE_WAIT'

        mock_proc_instance.net_connections.return_value = [mock_conn]
        


        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert result["score"] == normalizing_score(0, 135)
    assert "network_active" not in result["justifications"]
    assert not result["raw_metrics"]["network_active"]

@pytest.mark.asyncio
async def test_net_connections_access_denied_gracefully_handled():
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=True), \
         patch('process_manager.is_invocating_scripts', return_value=False), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

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
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=False), \
         patch('process_manager.is_invocating_scripts', return_value=True), \
         patch('process_manager.is_process_bound_to_a_service', return_value=True), \
         patch('process_manager.is_deleted_executable', return_value=False):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ('192.168.1.42', 443)
        mock_conn.status = 'ESTABLISHED'

        mock_proc_instance.net_connections.return_value = [mock_conn]

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert normalizing_score(result["score"], 135) == 39
    assert all(key in result["justifications"] for key in("is_signed", "invokes_python", "network_active"))
    assert "warning" in result["risk_level"]

@pytest.mark.asyncio
async def test_executable_is_critical_risk_level(config):
    with patch('process_manager.psutil.pid_exists', return_value=True), \
         patch('process_manager.psutil.Process') as mock_process, \
         patch('process_manager.is_signed', return_value=False), \
         patch('process_manager.is_invocating_scripts', return_value=True), \
         patch('process_manager.is_process_bound_to_a_service', return_value=False), \
         patch('process_manager.is_deleted_executable', return_value=True):

        mock_proc_instance = MagicMock()
        mock_proc_instance.exe.return_value = (config["paths"]["suspicious"][0] + "\\malicious.exe").lower()
        mock_process.return_value = mock_proc_instance

        mock_conn = MagicMock()
        mock_conn.raddr = ('192.168.1.42', 443)
        mock_conn.status = 'ESTABLISHED'

        mock_proc_instance.net_connections.return_value = [mock_conn]

        analyzer = ProcessAnalyzer(1234)
        result = await analyzer.run()

    assert normalizing_score(result["score"], 135) == 66
    assert "critical" in result["risk_level"]

@pytest.mark.asyncio
@patch('process_manager.grab_sha256_async', new_callable=AsyncMock)
async def test_mock_grab_sha256_async(mock_hash):
    mock_hash.return_value = "fakehash123"
    result = await mock_hash()
    assert result == "fakehash123"

@pytest.mark.asyncio
@patch('process_manager.psutil.pid_exists', return_value=True)
@patch('process_manager.psutil.Process')
async def test_process_exe_access_denied(mock_process, _):
    mock_proc_instance = MagicMock()
    mock_proc_instance.exe.side_effect = psutil.AccessDenied(1234)
    mock_process.return_value = mock_proc_instance

    analyzer = ProcessAnalyzer(1234)
    result = await analyzer.run()
    assert result is None

@pytest.mark.asyncio
@patch('process_manager.psutil.Process')
@patch('process_manager.grab_sha256_async', new_callable=AsyncMock)
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
        "ppid": 1
    }

    mock_parent = MagicMock()
    mock_parent.name.return_value = "explorer.exe"
    mock_proc_instance.parent.return_value = mock_parent

    mock_conn = MagicMock()
    mock_conn.raddr = ('192.168.1.42', 443)
    mock_conn.laddr = ('127.0.0.1', 1234)
    mock_conn.status = 'ESTABLISHED'

    mock_proc_instance.net_connections.return_value = [mock_conn]

    mock_process_class.return_value = mock_proc_instance
    result = await ProcessGetter.fetch_infos_for_process(mock_proc_instance, process_pid)

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
@patch('process_manager.ProcessGetter.fetch_infos_for_process', new_callable=AsyncMock)
@patch('process_manager.psutil.Process')
@patch('process_manager.psutil.pids')
async def test_get_processes_success(mock_pids, mock_process_class, mock_fetch):
    mock_pids.return_value = [123, 456]
    mock_proc1 = MagicMock()
    mock_proc2 = MagicMock()
    mock_process_class.side_effect = [mock_proc1, mock_proc2]

    mock_fetch.side_effect = [
        {"name": "proc1"},
        {"name": "proc2"}
    ]

    result = await ProcessGetter.get_processes()

    assert isinstance(result, dict)
    assert len(result) == 2
    assert result[123]["name"] == "proc1"
    assert result[456]["name"] == "proc2"

    mock_pids.assert_called_once()
    assert mock_process_class.call_count == 2
    assert mock_fetch.call_count == 2

@pytest.mark.asyncio
@patch('process_manager.ProcessGetter.fetch_infos_for_process', new_callable=AsyncMock)
@patch('process_manager.psutil.Process')
@patch('process_manager.psutil.pids')
async def test_get_processes_with_errors(mock_pids, mock_process_class, mock_fetch_infos):
    mock_pids.return_value = [123, 456, 789]

    mock_proc1 = MagicMock()
    mock_proc2 = MagicMock()
    mock_proc3 = MagicMock()
    mock_process_class.side_effect = [mock_proc1, mock_proc2, mock_proc3]

    # Simule une exception pour le second PID
    mock_fetch_infos.side_effect = [
        {"name": "proc1"}, 
        psutil.AccessDenied(pid=456),
        {"name": "proc3"}
    ]

    result = await ProcessGetter.get_processes()

    assert 123 in result
    assert 456 not in result  # Erreur => ignoré
    assert 789 in result
    assert len(result) == 2


@pytest.mark.asyncio
@patch('process_manager.grab_sha256_async', return_value="fakehash123")
@patch('process_manager.get_dll_info_sync', return_value=["dll1.dll", "dll2.dll"])
@patch('process_manager.psutil.Process')
async def test_fetch_infos_for_process_with_opened_files(mock_process_class, mock_get_dll, mock_hash, config):
    process_pid = 5678
    mock_proc_instance = MagicMock()
    mock_proc_instance.as_dict.return_value = {
        "name": "trusted.exe",
        "memory_percent": 3.14,
        "exe": (config["paths"]["trustworthy"][0] + "\\trusted.exe").lower(),
        "create_time": 1630000000.0,
        "status": "sleeping",
        "ppid": 2
    }
    mock_proc_instance.parent.return_value.name.return_value = "explorer.exe"
    mock_proc_instance.net_connections.return_value = []
    mock_process_class.return_value = mock_proc_instance

    result = await ProcessGetter.fetch_infos_for_process(mock_proc_instance, process_pid, include_opened_files=True)

    # Assertions
    assert result["name"] == "trusted.exe"
    assert result["PID"] == process_pid
    assert result["path"].endswith("trusted.exe")
    assert result["opened_dll"] == ["dll1.dll", "dll2.dll"]
    assert result["connections"] is None
    assert result["memory_percent"] == 3.14