import unittest
from unittest.mock import patch
from process_manager import ProcessAnalyzer


class TestProcessAnalyzer(unittest.TestCase):
    
    @patch('process_manager.psutil.pid_exists', return_value=False)
    def test_run_pid_not_exists(self, mock_pid_exists):
        analyzer = ProcessAnalyzer(999999)
        result = analyzer.run()
        self.assertIsNone(result)
    
    # Test 2 : Process inaccessible (AccessDenied) → run() retourne None
    # Mock: pid_exists = True, mais psutil.Process(pid) lève psutil.AccessDenied

    # Test 3 : Executable dans un chemin "suspicious" → +20 points
    # Mock: exe_path retourne un path commençant par CONFIG["paths"]["suspicious"][0]
    # Vérifie que justification["path_suspicious"] == True et score += 20

    # Test 4 : Executable dans un chemin "trustworthy" → -20 points
    # Mock: exe_path retourne un path commençant par CONFIG["paths"]["trustworthy"][0]
    # Vérifie que raw_metrics["path_trustworthy"] == True et score -= 20

    # Test 5 : Executable non signé → +30 points
    # Mock: is_signed() retourne False
    # Vérifie que justification["is_signed"] == True et score += 30

    # Test 6 : Executable signé → 0 point
    # Mock: is_signed() retourne True
    # Vérifie que justification ne contient pas "is_signed"

    # Test 7 : Le processus exécute du Python → +20 points
    # Mock: is_invocating_scripts() retourne True
    # Vérifie que justification["invokes_python"] == True et score += 20

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