import os
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401

mod = "mod4"
term = "alacritty"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod], "Return", lazy.layout.toggle_split()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(term)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Max(),
    layout.Bsp(),
    layout.Stack(num_stacks=2)
]

widget_defaults = dict(
    font='mononoki',
    fontsize=22,
    padding=0,
)
extension_defaults = widget_defaults.copy()

batt_icon = '#00ff00'
vol_icon = '#00ffff'
cal_icon = '#ffff00'

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TextBox("  ", name="space"),
                widget.WindowName(),
                widget.TextBox("   ", name="battery", font = 'Font Awesome 5 Free', foreground = batt_icon),
                widget.Battery(charge_char = '', format = '{char} {percent:2.0%}'),
                widget.TextBox("   ", name="volume", font = 'Font Awesome 5 Free', foreground = vol_icon),
                widget.Volume(),
                widget.TextBox("   ", name="calendar", font = 'Font Awesome 5 Free', foreground = cal_icon),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.TextBox("  ", name="space"),
                widget.Systray(),
                widget.TextBox("  ", name="space"),
            ],
            30,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TextBox("  ", name="space"),
                widget.WindowName(),
                widget.TextBox("   ", name="battery", font = 'Font Awesome 5 Free', foreground = batt_icon),
                widget.Battery(charge_char = '', format = '{char} {percent:2.0%}'),
                widget.TextBox("   ", name="volume", font = 'Font Awesome 5 Free', foreground = vol_icon),
                widget.Volume(),
                widget.TextBox("   ", name="calendar", font = 'Font Awesome 5 Free', foreground = cal_icon),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.TextBox("  ", name="space"),
                widget.Systray(),
                widget.TextBox("  ", name="space"),
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname':   'branchdialog'},  # gitk
    {'wname':   'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
    autoscript = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([autoscript])

@hook.subscribe.startup
def wallpaper():
    wallscript = os.path.expanduser('~/.config/qtile/wallpaper.sh')
    subprocess.call([wallscript])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
#wmname = "LG3D"
wmname = "qtile"
