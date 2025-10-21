<<<<<<< HEAD
# self.assertEqual(result["score"], normalizing_score(20, 135)) where 20 is the awaited score

=======
>>>>>>> 41acee971d9e4e8cecb325e933b7e8b23c3004cc
import unittest, psutil, sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
from process_manager import ProcessAnalyzer, MAX_SCORE
from config_loader import CONFIG
from utils import normalizing_score

class TestProcessAnalyzer(unittest.TestCase):
    
    @patch('process_manager.psutil.pid_exists', return_value=False)
    def test_run_pid_not_exists(self, mock_pid_exists):
        analyzer = ProcessAnalyzer(999999)
        result = analyzer.run()
        self.assertIsNone(result)
    
    @patch('process_manager.psutil.pid_exists', return_value=True)
    @patch('process_manager.psutil.Process', side_effect=psutil.AccessDenied(pid=1234))
    def test_access_denied(self, mock_process, mock_pid_exists):
        analyzer = ProcessAnalyzer(1234)
        result = analyzer.run()
        self.assertIsNone(result)
        mock_pid_exists.assert_called_once_with(1234)
        mock_process.assert_called_once_with(1234)

    def test_suspicious_path(self):
        with patch('process_manager.psutil.pid_exists', return_value=True), \
            patch('process_manager.psutil.Process') as mock_process, \
            patch('process_manager.is_signed', return_value=True), \
            patch('process_manager.is_invocating_scripts', return_value=False), \
            patch('process_manager.is_process_bound_to_a_service', return_value=True), \
            patch('process_manager.is_deleted_executable', return_value=False):
            
            mock_proc_instance = MagicMock()
            mock_proc_instance.exe.return_value = (CONFIG["paths"]["suspicious"][0] + "\\malicious.exe").lower()
            mock_proc_instance.net_connections.return_value = []
            mock_process.return_value = mock_proc_instance
        
            analyzer = ProcessAnalyzer(1234)
            result = analyzer.run()

        expected_score = normalizing_score(20, MAX_SCORE)
    
        self.assertEqual(result["score"], expected_score)
        self.assertTrue(result["justifications"].get("path_suspicious", False))
        self.assertTrue(result["raw_metrics"]["path_suspicious"])

    def test_trustworthy_path(self):
        with patch('process_manager.psutil.pid_exists', return_value=True), \
            patch('process_manager.psutil.Process') as mock_process, \
            patch('process_manager.is_signed', return_value=True), \
            patch('process_manager.is_invocating_scripts', return_value=True), \
            patch('process_manager.is_process_bound_to_a_service', return_value=True), \
            patch('process_manager.is_deleted_executable', return_value=False):
            
            mock_proc_instance = MagicMock()
            mock_proc_instance.exe.return_value = (CONFIG["paths"]["trustworthy"][0]+"\\malicious.exe").lower()
            mock_proc_instance.net_connections.return_value = []
            mock_process.return_value = mock_proc_instance
        
            analyzer = ProcessAnalyzer(1234)
            result = analyzer.run()

        expected_score = normalizing_score(0, MAX_SCORE)
    
        self.assertEqual(result["score"], expected_score)
        self.assertTrue(result["justifications"].get("path_trustworthy", True))
        self.assertTrue(result["raw_metrics"]["path_trustworthy"])
<<<<<<< HEAD
=======

    def test_executable_is_signed_gets_30_points(self):
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
            result = analyzer.run()

    
        self.assertEqual(result["score"], normalizing_score(30, 135))
        self.assertTrue(result["justifications"].get("is_signed", True))
        self.assertFalse(result["raw_metrics"]["is_signed"])
>>>>>>> 41acee971d9e4e8cecb325e933b7e8b23c3004cc

    def test_executable_is_not_signed_gets_30_points(self):
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
            result = analyzer.run()

    
        self.assertEqual(result["score"], normalizing_score(30, 135))
        self.assertTrue(result["justifications"].get("is_signed", True))
        self.assertFalse(result["raw_metrics"]["is_signed"])

    def test_executable_is_signed_gets_0_points(self):
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
            result = analyzer.run()

    
        self.assertEqual(result["score"], normalizing_score(0, 135))
        self.assertNotIn("is_signed", result["justifications"])
        self.assertTrue(result["raw_metrics"]["is_signed"])

    def test_executable_is_executing_python_and_gets_20_points(self):
        with patch('process_manager.psutil.pid_exists', return_value=True), \
            patch('process_manager.psutil.Process') as mock_process, \
            patch('process_manager.is_signed', return_value=True), \
            patch('process_manager.is_invocating_scripts', return_value=True), \
            patch('process_manager.is_process_bound_to_a_service', return_value=True), \
            patch('process_manager.is_deleted_executable', return_value=False):

            mock_proc_instance = MagicMock()
            mock_proc_instance.exe.return_value = ("d:\\apps\\myapp\\app.exe").lower()
            mock_proc_instance.net_connections.return_value = []
            mock_process.return_value = mock_proc_instance

        
            analyzer = ProcessAnalyzer(1234)
            result = analyzer.run()

    
        self.assertEqual(result["score"], normalizing_score(20, 135))
        self.assertIn("invokes_python", result["justifications"])
        self.assertTrue(result["raw_metrics"]["invokes_python"])

    # Test 8 : Le processus est lié à un service → 0 point
    # Mock: is_process_bound_to_a_service() retourne True
    # Vérifie que justification ne contient pas "not_bound_to_a_service"

    # Test 9 : Le processus n'est PAS lié à un service → +15 points
    # Mock: is_process_bound_to_a_service() retourne False
    # Vérifie que justification["not_bound_to_a_service"] == True et score += 15

    # Test 10 : Le binaire a été supprimé (deleted) → +15 points
    # Mock: is_deleted_executable() retourne True
    # Vérifie que justification["path_deleted"] == True et score += 15

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



if __name__ == "__main__":
    unittest.main()