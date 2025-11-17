import pytest
import asyncio
import hashlib
import subprocess

from unittest.mock import patch, mock_open

from app.utils.utils import (
    hexdump,
    grab_sha256_hash_of_process,
    grab_sha256_async,
    is_signed,
    normalizing_score,
    analyze_score_risk,
    estimate_risk_level,
)

def test_hexdump_basic():
    data = b"Hello World!"
    lines = hexdump(data, length=4)
    assert len(lines) == 3
    assert "Hello" in lines[0] or "Hell" in lines[0]  # ASCII portion

def test_grab_sha256_hash_of_process():
    content = b"abc123"
    m = hashlib.sha256()
    m.update(content)
    expected = m.hexdigest()

    with patch("builtins.open", mock_open(read_data=content)):
        result = grab_sha256_hash_of_process("dummy_path")
        assert result == expected


@pytest.mark.asyncio
async def test_grab_sha256_async():
    content = b"test_async"
    m = hashlib.sha256()
    m.update(content)
    expected = m.hexdigest()

    with patch("builtins.open", mock_open(read_data=content)):
        result = await grab_sha256_async("dummy_path")
        assert result == expected


def test_is_signed_success():
    fake_output = subprocess.CompletedProcess(args=[], returncode=0, stdout="Signed", stderr="")
    with patch("subprocess.run", return_value=fake_output):
        assert is_signed("dummy.exe") is True

def test_is_signed_failure():
    fake_output = subprocess.CompletedProcess(args=[], returncode=0, stdout="No signature found", stderr="")
    with patch("subprocess.run", return_value=fake_output):
        assert is_signed("dummy.exe") is False

def test_is_signed_missing_file():
    with patch("subprocess.run", side_effect=FileNotFoundError):
        result = is_signed("dummy.exe")
        assert "signtool.exe not found" in result


def test_normalizing_score():
    assert normalizing_score(50, 100) == 50
    assert normalizing_score(150, 100) == 100
    assert normalizing_score(-10, 100) == 0


def test_analyze_score_risk():
    assert analyze_score_risk(85) == "critical"
    assert analyze_score_risk(65) == "warning"
    assert analyze_score_risk(30) == "safe"


def test_estimate_risk_level_basic():
    metrics = {
        "path_suspicious": True,
        "path_deleted": False,
        "strange_chars": True,
        "not_bound_to_service": False,
        "invokes_python": False,
        "network_active": True,
        "is_signed": False,
        "path_trustworthy": False,
    }
    assert estimate_risk_level(metrics) == "high"

    metrics = {
        "is_signed": True,
        "path_trustworthy": True,
    }
    assert estimate_risk_level(metrics) == "low"

    assert estimate_risk_level(None) == "unknown"