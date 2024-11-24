import pyxel

class AnimationHandler():
    def __init__(self):
        self.blocking_anim_queue = []
        self.not_blocking_anim_queue = []
        self.go_back_to_state_after_blocking = None
        self.game_manager = None

    def do_one_frame(self):
        for anim in self.not_blocking_anim_queue:
            anim.do_one_frame()
        if len(self.blocking_anim_queue) == 0:
            if self.go_back_to_state_after_blocking != None:
                self.game_manager.game_state = self.go_back_to_state_after_blocking
                self.go_back_to_state_after_blocking = None
            return

        current_blocking_anim = self.blocking_anim_queue[0]
        current_blocking_anim.do_one_frame()

    def skip_current(self):
        if len(self.blocking_anim_queue) == 0:
            return
        current_blocking_anim = self.blocking_anim_queue[0]
        current_blocking_anim.skip_animation()

    def draw_animations(self):
        for anim in self.not_blocking_anim_queue:
            anim.draw_animation()
        if len(self.blocking_anim_queue) == 0:
            return
        current_blocking_anim = self.blocking_anim_queue[0]
        current_blocking_anim.draw_animation()

    def add_anim(self, animation, blocking=False):
        animation.animation_manager = self
        if blocking:
            self.blocking_anim_queue.append(animation)
        else:
            self.not_blocking_anim_queue.append(animation)
    def remove_anim(self, animation):
        try:
            self.blocking_anim_queue.remove(animation)
            self.not_blocking_anim_queue.remove(animation)
        except:
            print("STH WENT WRONG")


class Animation():
    def __init__(self, max_time, x, y, anim_element = None):
        self.max_time = max_time
        self.current_time = self.max_time
        self.x = x
        self.y = y
        self.anim_element = anim_element
        self.animation_manager = None
    
    def skip_animation(self):
        self.current_time = 0.0
    def do_one_frame(self):
        self.current_time -= 1/30
        if self.current_time <= 0.0:
            # usun siebie z listy
            self.animation_manager.remove_anim(self)
        
    def draw_animation(self):
        pass

class BoxAnimation(Animation):
    def __init__(self, max_time, x, y, size=5, color=1, anim_element=None):
        super().__init__(max_time, x, y, anim_element)
        self.size = size
        self.color = color

    def draw_animation(self):
        pyxel.rectb(self.x, self.y, self.size, self.size, self.color)