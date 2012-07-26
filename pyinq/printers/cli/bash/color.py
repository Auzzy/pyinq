class Color(object):
    def __init__(self, val):
        self.val = val
        self.is_bold = False

    def background(self):
        return self._get_color("")

    def foreground(self):
        return self._get_color("0;")

    def bold(self):
        col = Color(self.val)
        col.is_bold = True
        return col

    def _get_color(self, type_str):
        escape_str = "\033[{type}{color}m"
        val = self.val + (10 if type_str=="" else 0)
        type_str += "1;" if self.is_bold else ""
        return escape_str.format(type=type_str,color=val)

    @staticmethod
    def default():
        return "\033[0m"

BLACK = Color(30)
RED = Color(31)
GREEN = Color(32)
ORANGE = Color(33)
BLUE = Color(34)
MAGENTA = Color(35)
CYAN = Color(36)
GREY = Color(37)
CHARCOAL = Color(90)
PEACH = Color(91)
LIME = Color(92)
YELLOW = Color(93)
SKY = Color(94)
PINK = Color(95)
TEAL = Color(96)
WHITE = Color(97)

def color_print(text, fore=GREY, back=BLACK):
    fore_str = fore.foreground()
    back_str = back.background()
    print "{fore}{back}{text}{clear}".format(fore=fore_str,
                         back=back_str,
                         text=text,
                         clear=Color.default())
