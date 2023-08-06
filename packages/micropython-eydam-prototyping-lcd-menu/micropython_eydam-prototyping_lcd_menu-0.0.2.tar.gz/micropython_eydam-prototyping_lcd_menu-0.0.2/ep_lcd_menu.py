import json
import ep_statemachine as es
import time

class menu:
    def __init__(self, menu_config_file="menu.json", display_type="pc", display_size=(2, 16), display=None):
        self.menu_config_file = menu_config_file
        self.config = None
        self.sm = es.statemachine([])
        self.events = {
            "next": es.event("next"),
            "prev": es.event("prev"),
            "click": es.event("click"),
            "return": es.event("return"),
        }
        self.action_states = {}
        self.display_funcs = {}
        self.display = display
        self.display_type = display_type
        self.display_size = display_size
        self.cursor_pos = 0

    def load(self):
        with open(self.menu_config_file, "r") as f:
            self.config = json.load(f)
        
        self.build_submenu(self.config["menu"], True)

        self.sm.init()

    def build_submenu(self, menu_config, top_menu=False, parent=None):
        first = None
        prev = None

        if not top_menu:
            menu_config.append({"title": "up", "on_click": "click"})

        for entry in menu_config:
            if first is None:
                s = es.state(entry["title"], initial=top_menu)
                first = s
                prev = s
            else:
                s = es.state(entry["title"])
            s.data = entry
            
            self.sm.states.append(s)

            t_prev = es.transition(prev, events=[self.events["prev"]])
            s.transitions["prev"] = t_prev
            t_next = es.transition(s, events=[self.events["next"]])
            s.transitions["next"] = t_next

            if "on_click" in entry:
                if entry["on_click"] == "click":
                    t_on_click = es.transition(parent, events=[self.events["click"]])
                    s.transitions["click"] = t_on_click
                elif entry["on_click"] in self.action_states:
                    act_st = self.action_states[entry["on_click"]]
                    t_on_click = es.transition(act_st, events=[self.events["click"]])
                    act_st.add_transition(es.transition(s, events=[self.events["return"]]))
                    s.transitions["click"] = t_on_click

            if s != prev:
                t_next = es.transition(s, events=[self.events["next"]])
                prev.transitions["next"] = t_next

            if "children" in entry:
                c = self.build_submenu(entry["children"], parent=s)
                t_down = es.transition(c, events=[self.events["click"]])
                s.transitions["click"] = t_down

            prev = s
        
        return first

    def render(self, lines=[1,2]):
        rows = self.display_size[0]
        cols = self.display_size[1]

        display = [""]*rows
        state = self.sm.state
        if rows >= 2:
            display[0] = ">" if self.has_click() else " "
            display[0] += state.identifier[0:cols-2]
            display[1] = "  "
            if "second_line" in state.data:
                if "reading" in state.data["second_line"]:
                    if state.data["second_line"]["reading"] in self.display_funcs:
                        display[1] += self.display_funcs[state.data["second_line"]["reading"]]()
                        
            for i in range(len(display)):
                while len(display[i]) < cols:
                    display[i] += " "

        if self.display_type == "1602":
            if display is not None:
                if 1 in lines:
                    self.display.move_to(0,0)
                    self.display.putstr(display[0])
                if 2 in lines:
                    self.display.move_to(0,1)
                    self.display.putstr(display[1])
                
        return display
        
    def get_next_state(self):
        state = self.sm.state
        if "next" in state.transitions:
            if state.transitions["next"].dst != state:
                return state.transitions["next"].dst
        return None

    def get_prev_state(self):
        state = self.sm.state
        if "prev" in state.transitions:
            if state.transitions["prev"].dst != state:
                return state.transitions["prev"].dst
        return None

    def has_click(self):
        return "click" in self.sm.state.transitions

    def build_list_submenu(self):
        pass

    def next(self):
        self.sm.action(self.events["next"])
        self.render()

    def prev(self):
        self.sm.action(self.events["prev"])
        self.render()

    def click(self):
        self.sm.action(self.events["click"])
        self.render()

    def t_return(self):
        self.sm.action(self.events["return"])
        self.render()


class menu_rot_enc(menu):
    def __init__(self, rotary=None, button_pin=None, update_interval=3000, menu_config_file="menu.json", 
        display_type="pc", display_size=(2, 16), display=None, timer_id_1=1, timer_id_2=2):
        import machine

        super().__init__(menu_config_file=menu_config_file, display_type=display_type, display_size=display_size, display=display)
        self.rotary = rotary
        self.old_rotary_val = 0
        self.button_pin = button_pin
        self.button = machine.Pin(button_pin, machine.Pin.IN)
        self.button.irq(trigger=machine.Pin.IRQ_RISING, handler=self.debounced_click)
        self.last_click = time.ticks_ms()

        self.tim_rotary = machine.Timer(timer_id_1)
        self.tim_rotary.init(mode=machine.Timer.PERIODIC, freq=10, callback=self.check_rotary)

        self.tim_render = machine.Timer(timer_id_2)
        self.tim_render.init(mode=machine.Timer.PERIODIC, period=update_interval, callback=lambda t: self.render(lines=[2]))


    def debounced_click(self, pin):
        if time.ticks_ms()-self.last_click > 500:
            self.click()
            self.last_click = time.ticks_ms()

    def check_rotary(self, timer):
        new_val = self.rotary.value()
        if self.old_rotary_val > new_val:
            self.prev()

        if self.old_rotary_val < new_val:
            self.next()
        
        self.old_rotary_val = new_val