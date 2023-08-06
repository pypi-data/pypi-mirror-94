import unittest
import ep_lcd_menu as elm
import ep_statemachine as es

class Test(unittest.TestCase):
    def test_init(self):
        menu = elm.menu(menu_config_file="test/menu1.json")
        menu.load()

        self.assertEqual(menu.sm.state.identifier, "Entry1")
        display = menu.render()
        self.assertEqual(display[0], ">Entry1         ")
        menu.next()
        self.assertEqual(menu.sm.state.identifier, "Entry2")
        display = menu.render()
        self.assertEqual(display[0], " Entry2         ")
        menu.next()
        self.assertEqual(menu.sm.state.identifier, "Entry3")
        display = menu.render()
        self.assertEqual(display[0], " Entry3         ")
        menu.next()
        self.assertEqual(menu.sm.state.identifier, "Entry3")
        display = menu.render()
        self.assertEqual(display[0], " Entry3         ")
        menu.prev()
        self.assertEqual(menu.sm.state.identifier, "Entry2")
        display = menu.render()
        self.assertEqual(display[0], " Entry2         ")
        menu.prev()
        self.assertEqual(menu.sm.state.identifier, "Entry1")
        display = menu.render()
        self.assertEqual(display[0], ">Entry1         ")
        menu.prev()
        self.assertEqual(menu.sm.state.identifier, "Entry1")
        display = menu.render()
        self.assertEqual(display[0], ">Entry1         ")
        menu.click()
        self.assertEqual(menu.sm.state.identifier, "Entry1.1")
        display = menu.render()
        self.assertEqual(display[0], " Entry1.1       ")
        menu.next()
        self.assertEqual(menu.sm.state.identifier, "Entry1.2")
        display = menu.render()
        self.assertEqual(display[0], " Entry1.2       ")
        menu.click()
        self.assertEqual(menu.sm.state.identifier, "Entry1.2")
        display = menu.render()
        self.assertEqual(display[0], " Entry1.2       ")
        menu.next()
        self.assertEqual(menu.sm.state.identifier, "up")
        display = menu.render()
        self.assertEqual(display[0], ">up             ")
        menu.click()
        self.assertEqual(menu.sm.state.identifier, "Entry1")
        display = menu.render()
        self.assertEqual(display[0], ">Entry1         ")

    def test_actions(self):
        menu = elm.menu("test/menu1.json")

        i = 0

        def action_state_1_1():
            nonlocal i
            i = 1
            menu.t_return()

        menu.action_states["ActionState1.1"] = es.state(
            "ActionState1.1", 
            entry_action=action_state_1_1
            )

        menu.load()
        menu.click()
        self.assertEqual(menu.sm.state.identifier, "Entry1.1")
        menu.click()
        self.assertEqual(menu.sm.state.identifier, "Entry1.1")
        self.assertEqual(i, 1)

    def test_render(self):
        menu = elm.menu("test/menu2.json")

        menu.display_funcs = {
            "print_test": lambda: "test"
        }

        menu.load()

        self.assertEqual(menu.sm.state.identifier, "Entry1")
        display = menu.render()
        self.assertEqual(display[0], " Entry1         ")
        self.assertEqual(display[1], "  test          ")
        menu.next()