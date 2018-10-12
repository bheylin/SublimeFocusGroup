import sublime
import sublime_plugin


def get_settings():
    return sublime.load_settings('FocusGroup.sublime-settings')

def is_layout_in_progress(settings):
    return settings.get("fg.is_layout_in_progress", False)

def set_layout_in_progress(settings, value):
    return settings.get("fg.is_layout_in_progress", value)


class FocusGroupEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        window  = view.window()
        if window.num_groups() > 1: 
            window.run_command("fg_focus_group")


class FgFocusGroup(sublime_plugin.WindowCommand):

    def apply_layout(self, division_count, focused_size, dimension_name, layout, active_group):
        remainder = 1 - focused_size
        if division_count == 2:
            layout[dimension_name][1] = focused_size if active_group == 0 else remainder
        else:
            inner_elems_count = division_count - 1
            unfocused_size = remainder / inner_elems_count
            dimension = layout[dimension_name]

            last = 0
            for i in range(1, division_count):
                print(i)
                dimension[i] = last + (focused_size if active_group == (i-1) else unfocused_size)
                last = dimension[i]

    def run(self, **args):
        settings = get_settings()

        if is_layout_in_progress(settings):
            return

        set_layout_in_progress(settings, True)
        layout  = self.window.get_layout()
        active_group = self.window.active_group()

        column_count, row_count = len(layout['cols']) - 1, len(layout['rows']) - 1

        if column_count > 1:
            col_focused_size = settings.get('fg.focusd_size_{}_segments'.format(column_count), 0.6)
            self.apply_layout(column_count, col_focused_size, 'cols', layout, active_group)

        if row_count > 1:
            row_focused_size = settings.get('fg.focusd_size_{}_segments'.format(row_count), 0.6)
            self.apply_layout(row_count, row_focused_size, 'rows', layout, active_group)

        if column_count > 1 or row_count > 1:
            self.window.run_command('set_layout', layout)
            set_layout_in_progress(settings, False)
