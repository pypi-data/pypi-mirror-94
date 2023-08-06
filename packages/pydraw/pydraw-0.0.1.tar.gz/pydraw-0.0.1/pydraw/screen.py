import turtle;
import inspect;

from pydraw import Color;
from pydraw import Location;

INPUT_TYPES = [
    'mousedown',
    'mouseup',
    'mousedrag',
    'keydown',
    'keyup',
    'keypress'
];

ALPHABET = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
];

UPPER_ALPHABET = [];
for letter in ALPHABET:
    UPPER_ALPHABET.append(letter.upper());

KEYS = [
           '1',
           '2',
           '3',
           '4',
           '5',
           '6',
           '7',
           '8',
           '9',
           '0',

           # '!',
           # '@',
           # '#',
           # '$',
           # '%',
           # '^',
           # '&',
           # '*',
           # '(',
           # ')',

           '-',  # note: appears to be the shift key?

           # '_',
           # '=',
           # '+',
           # '\\',
           # '|',
           # ',',
           # '<',
           # '.',
           # '>'
           # '/',
           # '?',

           'Up',
           'Down',
           'Left',
           'Right',

           'space',
           'Shift_L',
           'Shift_R',
           'Control_L',
           'Control_R'
       ] + ALPHABET + UPPER_ALPHABET;

BUTTONS = [
    1,
    2,
    3
];

BORDER_CONSTANT = 10;


class Screen:
    """
    A class containing methods and values that can be manipulated in order to affect
    the window that is created. Sort of like a canvas.
    """

    def __init__(self, width=800, height=600, title="pydraw"):
        self._screen = turtle.Screen();
        self._screen.screensize(width, height);
        self._screen.setup(width + BORDER_CONSTANT, height + BORDER_CONSTANT);
        # This was not necessary as the canvas will align with the window's dimensions as set in the above line.

        self._screen.title(title);

        self._screen.colormode(255);

        # By default we want to make sure that all objects are drawn instantly.
        self._screen.tracer(0);
        self._screen.update();

        # --- #

        self.registry = {};  # The input function registry (stores input callbacks)

    def color(self, color: Color) -> None:
        """
        Set the background color of the screen.
        :param color: the color to set the background to
        :return: None
        """
        self._screen.bgcolor(color.__value__());

    def picture(self, pic: str) -> None:
        """
        Set the background picture of the screen.
        :param pic: the path to said picture from the file
        :return: None
        """
        self._screen.bgpic(pic);

    # Size
    def resize(self, width, height) -> None:
        """
        Resize the screen to new dimensions
        :param width: the width to resize to
        :param height: the height to resize to
        :return: None
        """
        self._screen.screensize(width, height);

    def size(self) -> (int, int):
        """
        Get the size of the screen (please note this is not the canvas, and those attributes should be
        retrieved using the width() and height() methods respectively)
        :return: a tuple containing the width and height of the screen
        """
        return self._screen.window_width(), self._screen.window_height();

    def width(self) -> int:
        """
        Returns the width of the CANVAS within the screen. Important.
        :return: an integer representing the width of the canvas
        """
        return self._screen.getcanvas().winfo_width() - BORDER_CONSTANT;

    def height(self) -> int:
        """
        Returns the height of the CANVAS within the screen. Important.
        :return:
        """
        return self._screen.getcanvas().winfo_height() - BORDER_CONSTANT;

    # Direct Manipulation
    def clear(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.clear();

    def update(self) -> None:
        """
        Updates the screen.
        :return: None
        """
        try:
            self._screen.update();
        except turtle.Terminator:
            # If we experience the termination exception, we will print the termination of the program
            # and exit the python program.
            print('Terminated.');
            exit(1);

    def exit(self) -> None:
        """
        You must call this method to have the window properly exit.
        :return: None
        """
        self._screen.clear();
        turtle.done();

    # ------------------------------------------------------- #

    def listen(self) -> None:
        """
        Reads the file for input functions and registers them as callbacks!
        The input-type is determined by the name of the function.

        Allowed Names:
          - mousedown
          - mouseup
          - mousedrag
          - keydown
          - keyup
          - keypress (deprecated)
        :return: None
        """
        frm = inspect.stack()[1];
        mod = inspect.getmodule(frm[0]);
        for (name, function) in inspect.getmembers(mod, inspect.isfunction):
            if name.lower() not in INPUT_TYPES:
                continue;

            self.registry[name.lower()] = function;
            print('Registered input-function:', name);

        self._listen();

    def _listen(self):
        self._screen.listen();

        # Keyboard
        for key in KEYS:
            self._screen.onkeypress(self._create_lambda('keydown', key), key);
            self._screen.onkeyrelease(self._create_lambda('keyup', key), key);

            # custom implemented keypress
            self._onkeytype(self._create_lambda('keypress', key), key);

        # Mouse
        for btn in BUTTONS:
            self._screen.onclick(self._create_lambda('mousedown', btn), btn);  # mousedown
            self._onrelease(self._create_lambda('mouseup', btn), btn);
            self._ondrag(self._create_lambda('mousedrag', btn), btn);

            # custom implemented mouseclick
            self._onmouseclick(self._create_lambda('mouseclick', btn), btn);

    # pending type-definition (function?)
    def _create_lambda(self, method: str, key):
        """
        A hacked method to create lambdas for key-event registration.
        :param key: the key to create the lambda for
        :return: A lambda
        """
        if method == 'keydown':
            return lambda: (self._keydown(key));
        elif method == 'keyup':
            return lambda: (self._keyup(key));
        elif method == 'mousedown':
            return lambda x, y: (self._mousedown(key, self.create_location(x, y)));
        elif method == 'mouseup':
            return lambda x, y: (self._mouseup(key, self.create_location(x, y)));
        elif method == 'mousedrag':
            return lambda x, y: (self._mousedrag(key, self.create_location(x, y)));
        else:
            return None;

    def _keydown(self, key) -> None:
        if 'keydown' not in self.registry:
            return;

        self.registry['keydown'](key);

    def _keyup(self, key) -> None:
        if 'keyup' not in self.registry:
            return;

        self.registry['keyup'](key);

    def _keypress(self, key) -> None:
        if 'keypress' not in self.registry:
            return;

        self.registry['keypress'](key);

    def _mousedown(self, button, location) -> None:
        if 'mousedown' not in self.registry:
            return;

        try:
            self.registry['mousedown'](button, location);
        except TypeError:
            raise TypeError('An argument error occurred. This is most likely due to a lack of proper argumentation. '
                            'Please note that the \'mousedown\' function requires a button and location argument.');

    def _mouseup(self, button, location) -> None:
        if 'mouseup' not in self.registry:
            return;

        try:
            self.registry['mouseup'](button, location);
        except TypeError:
            raise TypeError('An argument error occurred. This is most likely due to a lack of proper argumentation. '
                            'Please note that the \'mouseup\' function requires a button and location argument.');

    def _mouseclick(self, button, location) -> None:
        if 'mouseclick' not in self.registry:
            return;

        try:
            self.registry['mouseclick'](button, location);
        except TypeError:
            raise TypeError('An argument error occurred. This is most likely due to a lack of proper argumentation. '
                            'Please note that the \'mouseclick\' function requires a button and location argument.');

    def _mousedrag(self, button, location) -> None:
        if 'mousedrag' not in self.registry:
            return;

        try:
            self.registry['mousedrag'](button, location);
        except TypeError:
            raise TypeError('An argument error occurred. This is most likely due to a lack of proper argumentation. '
                            'Please note that the \'mousedrag\' function requires a button and location argument.')

    # --- Helper Methods --- #
    def create_location(self, x, y) -> Location:
        """
        Is passed turtle-based coordinates and converts them into normal coordinates
        :param x: the x component
        :param y: the y component
        :return: a location comprised of the passed x and y components
        """
        return Location(x + (self.width() / 2), -y + (self.height() / 2));

    # -- Internals -- #
    def _onrelease(self, fun, btn, add=None):
        """
        An internal method hooking into the TKinter canvas.
        :param fun: the function to call upon mouse release
        :param btn: the mouse button to bind to
        :param add: i have no clue what this does
        :return: None
        """

        def eventfun(event):
            x, y = (self._screen.cv.canvasx(event.x) / self._screen.xscale,
                    -self._screen.cv.canvasy(event.y) / self._screen.yscale)
            fun(x, y)

        self._screen.cv.bind("<Button%s-ButtonRelease>" % btn, eventfun, add);

    def _ondrag(self, fun, btn, add=None):
        """
        An internal method hooking into the TKinter canvas.
        :param fun: the function to call upon drag
        :param btn: the mouse button to bind to
        :param add: i have no clue
        :return: None
        """

        # noinspection PyBroadException
        def eventfun(event):
            try:
                x, y = (self._screen.cv.canvasx(event.x) / self._screen.xscale,
                        -self._screen.cv.canvasy(event.y) / self._screen.yscale)
                fun(x, y)
            except Exception:
                pass

        self._screen.cv.bind("<Button%s-Motion>" % btn, eventfun, add);

    def _onmouseclick(self, fun, btn, add=None):
        pass;

    def _onkeytype(self, fun, btn, add=None):
        pass;
