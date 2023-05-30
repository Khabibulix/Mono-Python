from crack import *
import pytest
import importlib


def test_layout_color():
    assert Layout.ROUGE.endswith("1m")

def test_methods_of_Cracker_class_for_crack_dict():
    assert getattr(cracker, "crack_dict")

def test_methods_of_Cracker_class_for_crack_smart():
    assert getattr(cracker, "crack_smart")

def test_import_of_hashlib():
    assert importlib.util.find_spec("hashlib")

def test_import_of_string():
    assert importlib.util.find_spec('string')

def test_import_of_argparse():
    assert importlib.util.find_spec('argparse')

def test_crack_dict_with_md5():
    assert cracker.crack_dict("95fa9d10dd5aed2c42004a915de00c8d", "wordlist.txt") == True


def test_crack_dict_with_sha_256():
    assert cracker.crack_dict("c6841067cb3a30ee869659fe47e50f9a59cd68ada7d3cac07ae985dee34871dc", "wordlist.txt") == True


def test_crack_smart_with_md5_with_lower_case():
    assert cracker.crack_smart("d9d7dbddc29177b121a6aa1bb09d15fd", "*a*") == True
    #bab


def test_crack_smart_with_sha_256_with_lower_case():
    assert cracker.crack_smart("ecdd97405c79b408ee7791029d05d2b57893d9b06a1282531e0df729daefcef5", "*a*") == True
    #bab

def test_crack_smart_with_md5_with_upper_case():
    assert cracker.crack_smart("96c119ee89e0b239407244b51e38fa61", "^A^") == True
    #BAB

def test_crack_smart_with_sha_256_with_upper_case():
    assert cracker.crack_smart("5a421865e06163d285dbe857d63b445980f9bf6309c68ec558c62ff6315400ba", "^A^") == True
    #BAB

def test_crack_smart_with_md5_with_numbers():
    assert cracker.crack_smart("310dcbbf4cce62f762a2aaa148d556bd", "²3²") == True
    #333

def test_crack_smart_with_sha_256_with_numbers():
    assert cracker.crack_smart("556d7dc3a115356350f1f9910b1af1ab0e312d4b3e4fc788d2da63668f36d017", "²3²") == True
    #333

def test_crack_smart_with_md5_with_lower_case_and_upper_case():
    assert cracker.crack_smart("56f27dc9bb026e86ee241fa197d00fb0", "^b^") == True
    #BbB

def test_crack_smart_withmd5_and_sha_256_for_all_characters():
    assert cracker.crack_smart("56f27dc9bb026e86ee241fa197d00fb0", "*^3*") == True and cracker.crack_smart("927fb10118a9b87f40a56e31a6ec5e1e", "*^3*") == True
    #b83b"""


def test_generate_the_hack_for_md5():
    assert cracker.generate_the_hack(1, "abruti") == "95fa9d10dd5aed2c42004a915de00c8d"


def test_generate_the_hack_for_sha_256():
    assert cracker.generate_the_hack(2, "abruti") == "c6841067cb3a30ee869659fe47e50f9a59cd68ada7d3cac07ae985dee34871dc"


def test_md5_length():
    x = cracker.generate_the_hack(1, "testingthatshit")
    y = cracker.generate_the_hack(1, "testingthatothershit")
    assert (len(x) + len(y)) / 2 == 32
    #should be 32

def test_sha_256_length():
    x = cracker.generate_the_hack(2, "testingthatshit")
    y = cracker.generate_the_hack(2, "testingthatothershit")
    assert (len(x) + len(y)) / 2 == 64
    #should be 64


