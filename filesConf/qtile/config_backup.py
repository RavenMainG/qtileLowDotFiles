# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Importamos la libreria de Os para manejar los script externos
import os
import subprocess

from libqtile import hook

# Variables de entorno

# Incio, variables para controlar de forma alternativa el enfoque, el desplazamiento
# de ventanas y el ajuste de ventanas con las flechas del teclado 
l = "Left"
r = "Right"
d = "Down"
u = "Up"
#fin

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Switch between windows ALTERNATIVE WHIT ARROWS 
    Key([mod], l, lazy.layout.left(), desc="Move focus to left"),
    Key([mod], r, lazy.layout.right(), desc="Move focus to right"),
    Key([mod], d, lazy.layout.down(), desc="Move focus down"),
    Key([mod], u, lazy.layout.up(), desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Move windows between left/right columns or move up/down in current stack ALTERNATIVE WHIT ARROWS

    Key([mod, "shift"], l, lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], r, lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], d, lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], u, lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Grow windows. If current window is on the edge of screen and direction ALTERNATIVE WHIT ARROWS

    Key([mod, "control"], l, lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], r, lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], d, lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], u, lazy.layout.grow_up(), desc="Grow window up"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # Key mod for float window 
    Key([mod], "f", lazy.window.toggle_floating()),

    # Key mod for fullscreen
    Key([mod], "m", lazy.window.toggle_fullscreen()),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Key mod for rofi
    Key([mod], 'd', lazy.spawn('rofi -show drun'), desc = 'Lanza rofi'),

    # Key for Brigthness
    Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl set +5%')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl set 5%-')),

    # Key for volume
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=["#20daaa", "#20daaa"],
        border_focus = "#ffadbb", 
        border_width=4,
        margin = 5,
        margin_on_single = 15
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Font Awesome 5 Free Regular",
    fontsize=15,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
               widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#585b6a',
                padding = 0,
                foreground = '#585b6a',
                fmt = '',
                fontsize = 30
            ),

            widget.Image(
                filename = '/home/pandora/Descargas/bars-solid.svg',
                mouse_callbacks = {'Button1': lazy.spawn("rofi -show drun")},
                background = '#585b6a',
                margin = 3
            ),

            widget.Clock(
                foreground = '#ffa9ff',
                background = '#585b6a',
                format=" %Y-%m-%d %a %I:%M %p"
            ),
           widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#9996ab',
                padding = 0,
                foreground = '#585b6a',
                fmt = '',
                fontsize = 30
            ),
            widget.Prompt(),
            widget.TextBox(
                padding = 280
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#9996ab',
                padding = 0,
                foreground = '#585b6a',
                text = '',
                fontsize = 30
            ),

            widget.GroupBox(
                font= "Fira Code Nerd Font",#"Hack Nerd Font",
                background = '#585b6a',
                #foreground = '#585b6a',
                fontsize = 22,
                active = '#e6b9ec',
                inactive = '#f6eda8',
                highlight_method='line',
                highlight_color = ['#585b6a', '#585b6a'],
                this_current_screen_border = '#e6b9ec',
                margin_x = 8
                #margin
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#9996ab',
                padding = 0,
                foreground = '#585b6a',
                fmt = '',
                fontsize = 30
            ),
            widget.TextBox(
                padding = 150
            ),
            widget.Chord(
                chords_colors={
                    "launch": ("#ff0000", "#ffffff"),
                },
                name_transform=lambda name: name.upper(),
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#9996ab',
                padding = 0,
                foreground = '#9bdfdf',
                text = '',
                fontsize = 30
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#9bdfdf',
                padding = 0,
                foreground = '#ff5408',
                text = '  ',
                fontsize = 20
            ),
            widget.ThermalSensor(
                background = '#9bdfdf',
                foreground = '#fffaf2',
                fmt = ': {}',
                tag_sensor = "Core 0"
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#9bdfdf',
                padding = 0,
                foreground = '#ff8089',
                text = '',
                fontsize = 30
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#ff8089',
                padding = 0,
                foreground = '#fff04f',
                text = ' :',
                fontsize = 23
            ),
            widget.Memory(
                foreground = '#fffaf2',
                background = '#ff8089',
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e btop')},
                fmt = '{}'
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#ff8089',
                padding = 0,
                foreground = '#d1c8ff',
                text = '',
                fontsize = 30
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#d1c8ff',
                padding = 0,
                foreground = '#fff04f',
                text = ' 墳: ',
                fontsize = 20
            ),
            widget.PulseVolume(
                foreground = '#fffaf2',
                background = '#d1c8ff',
                limit_max_volume = True,
                fmt = '{} '
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#d1c8ff',
                padding = 0,
                foreground = '#20daac',
                text = '',
                fontsize = 30
            ),
            widget.TextBox(
                font = 'Hack Nerd Font',
                background = '#20daac',
                padding = 0,
                foreground = '#fff04f',
                text = ' :',
                fontsize = 20
            ),
            widget.Backlight(
                backlight_name = 'intel_backlight',
                background = '#20daac',
                fmt = ' {}  '
            ),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# Configuraciones de scripts

# Array de comandos a ejecutar al inicar qtile
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])