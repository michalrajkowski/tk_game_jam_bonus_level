import pyxel

class AnimationHandler():
    def __init__(self):
        self.blocking_anim_queue = []
        self.not_blocking_anim_queue = []
        self.go_back_to_state_after_blocking = None
        self.game_manager = None
        self.room_manager = None

    def end_room_anim(self):
        self.add_anim(EndTurnAnimation(1.0,0,0), True)

    def has_block_anims(self):
        return len(self.blocking_anim_queue) > 0
    
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
        animation.room_manager = self.room_manager
        if blocking:
            self.blocking_anim_queue.append(animation)
        else:
            self.not_blocking_anim_queue.append(animation)
    def remove_anim(self, animation):
        try:
            self.blocking_anim_queue.remove(animation)
            # self.not_blocking_anim_queue.remove(animation)
        except:
            print("STH WENT WRONG")
        try:
            # self.blocking_anim_queue.remove(animation)
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
        self.room_manager = None
        self.overtime = 0.0
    
    def skip_animation(self):
        self.current_time = 0.0
        self.overtime = 0.5
    def do_one_frame(self):
        self.current_time -= 1/30
        if self.current_time + self.overtime<= 0.0:
            self.on_end()
            # usun siebie z listy
            self.animation_manager.remove_anim(self)
        
    def draw_animation(self):
        pass

    def on_end(self):
        pass

class BoxAnimation(Animation):
    def __init__(self, max_time, x, y, size=5, color=1, anim_element=None):
        super().__init__(max_time, x, y, anim_element)
        self.size = size
        self.color = color

    def draw_animation(self):
        pyxel.rectb(self.x, self.y, self.size, self.size, self.color)

class StatIncreaseAnimation(Animation):
    def __init__(self, max_time, x, y, text, color, anim_element=None):
        super().__init__(max_time, x, y, anim_element)
        self.text = text
        self.color = color
    
    def draw_animation(self):
       max_offset_y = 15
       offset_y = (1.0 - (self.current_time/self.max_time))* max_offset_y
       pyxel.text(self.x, self.y +20 - offset_y, self.text, self.color)


class EndTurnAnimation(Animation):
    def __init__(self, max_time, x, y, size=5, color=1, anim_element=None):
        super().__init__(max_time, x, y, anim_element)
        self.size = size
        self.color = color

    def draw_animation(self):
        # Fill screen with black rect
        anim_percent = 1.0 - self.current_time/self.max_time
        pyxel.rect(0,0, 300*anim_percent, 300, 0)
    
    def on_end(self):
        self.room_manager.load_next_room_content()
        anim = StartTurnAnimation(1.0, 0,0)
        self.animation_manager.add_anim(anim, True)
        # Add animation that will reveal screen?

class StartTurnAnimation(Animation):
    def __init__(self, max_time, x, y, size=5, color=1, anim_element=None):
        super().__init__(max_time, x, y, anim_element)
        self.size = size
        self.color = color

    def draw_animation(self):
        # Fill screen with black rect
        anim_percent = self.current_time/self.max_time
        pyxel.rect(0,0, 300*anim_percent, 300, 0)
    
    def on_end(self):
        pass
        # Add animation that will reveal screen?

class TalkAnimation(Animation):
    def __init__(self, max_time, x, y, object_w, text: str, anim_element=None):
        super().__init__(max_time, x, y, anim_element)
        self.text = text
        self.talk_speed = 20.0
        self.max_time = (len(self.text)) / self.talk_speed
        self.overtime = 2.0
        self.current_time = self.max_time
        self.talk_bubble_size = 100
        self.object_w = object_w
        self.line_height = 6  # Height of each line of text
        self.talk_bubble_h = 10  # Initial height
        self.fragment_text()

    def fragment_text(self):
        # Split the text into lines based on the width of the bubble
        self.text_lines = split_text_into_lines(self.text, self.talk_bubble_size)
        # Update the talk bubble height based on the number of lines
        self.talk_bubble_h = len(self.text_lines) * self.line_height + 4
        self.text = '\n'.join(self.text_lines)  

    def draw_animation(self):
        # Draw the bubble
        pyxel.rect(
            self.x + self.object_w / 2 - self.talk_bubble_size / 2,
            self.y - self.talk_bubble_h,
            self.talk_bubble_size + 4,
            self.talk_bubble_h,
            0
        )
        pyxel.rectb(
            self.x + self.object_w / 2 - self.talk_bubble_size / 2,
            self.y - self.talk_bubble_h,
            self.talk_bubble_size + 4,
            self.talk_bubble_h,
            7
        )

        # Draw each line of text inside the bubble
        percent = (1.0 - (self.current_time)/(self.max_time))*100
        if (percent > 100):
            percent = 100
        talk_text = cut_percentage(self.text, percent)
        pyxel.text(
            self.x + self.object_w / 2 - self.talk_bubble_size / 2 + 2,
            self.y - self.talk_bubble_h + 2,
            talk_text,
            7
        )


def split_text_into_lines(text, bubble_width):
    current_line = []
    current_width = 0
    result_lines = []

    for char in text:
        # Each character has a width of 3 pixels, plus 1 pixel of space
        char_width = 3
        space_width = 1 if len(current_line) > 0 else 0

        if current_width + char_width + space_width <= bubble_width:
            current_line.append(char)
            current_width += char_width + space_width
        else:
            result_lines.append(''.join(current_line))
            current_line = [char]
            current_width = char_width

    if current_line:
        result_lines.append(''.join(current_line))

    return result_lines

def cut_percentage(text, percent):
    """
    Cuts the specified percentage of the text.
    
    :param text: The input text (str).
    :param percent: The percentage of the text to cut (float or int).
    :return: The shortened text (str).
    """
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    
    cut_length = int(len(text) * (percent / 100))
    return text[:cut_length]