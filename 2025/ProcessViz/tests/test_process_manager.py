import pytest
import pytest_asyncio
import psutil
import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from unittest.mock import patch, MagicMock
from process_manager import ProcessAnalyzer, MAX_SCORE
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

# Test 10 : Le binaire a été supprimé (deleted) → +15 points
# Mock: is_deleted_executable() retourne True
# Vérifie que justification["path_deleted"] == True et score += 15
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

# Test 11 : Executable contient des caractères suspects → +15 points
# Mock: exe_path = "C:\\weird\\µ$\\script.exe"
# Vérifie que justification["strange_chars"] == True et score += 15

# Test 12 : Activité réseau détectée → +20 points
# Mock: proc.net_connections() retourne une liste avec une connexion raddr + status CONN_ESTABLISHED
# Vérifie que justification["network_active"] == True et score += 20

# Test 13 : Aucune activité réseau → 0 point
# Mock: proc.net_connections() retourne []
# Vérifie que justification ne contient pas "network_active"

# Test 14 : Score total normalisé et risk_level corrects
# Mock un ensemble de conditions pour forcer un score (par ex: 60)
# Vérifie que score est normalisé correctement (avec normalizing_score)
# Vérifie que risk_level correspond bien à la valeur attendue (avec analyze_score_risk)

# Test 15 : Tous les mocks combinés → test end-to-end d’un run() complet
# Simule un cas avec plusieurs flags actifs, vérifie le score final et les justifications
