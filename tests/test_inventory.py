import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lootbox_sim.inventory import Inventory

def test_add_single_item():
    inv = Inventory()
    inv.add_item("Sword")
    assert inv.items["Sword"] == 1

def test_add_multiple_items():
    inv = Inventory()
    inv.add_item("Sword")
    inv.add_item("Sword")
    assert inv.items["Sword"] == 2

def test_add_different_items():
    inv = Inventory()
    inv.add_item("Sword")
    inv.add_item("Shield")
    assert inv.items["Sword"] == 1
    assert inv.items["Shield"] == 1
