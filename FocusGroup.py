import sublime
import sublime_plugin


class FocusGroupEventListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        window  = view.window()
        if window.num_groups() > 1: 
            window.run_command("fg_focus_group")


class FgFocusGroup(sublime_plugin.WindowCommand):

    def apply_layout(self, division_count, focused_size, dimension_name, layout, active_group):
        if division_count == 2:
            layout[dimension_name][1] = focused_size if active_group == 0 else 1 - focused_size
        elif division_count == 3:
            unfocused_size = (1 - focused_size) * 0.5
            layout[dimension_name][1] = focused_size if active_group == 0 else unfocused_size
            layout[dimension_name][2] = layout[dimension_name][1] + (focused_size if active_group == 1 else unfocused_size)

    def run(self, **args):
        settings = sublime.load_settings('FocusGroup.sublime-settings')

        layout  = self.window.get_layout()
        active_group = self.window.active_group()

        column_count = len(layout['cols']) - 1
        row_count = len(layout['rows']) - 1

        if column_count > 1:
            col_focused_size = settings.get('fg.focusd_size_{}_segments'.format(column_count), 0.6)
            self.apply_layout(column_count, col_focused_size, 'cols', layout, active_group)

        if row_count > 1:
            row_focused_size = settings.get('fg.focusd_size_{}_segments'.format(row_count), 0.6)
            self.apply_layout(row_count, row_focused_size, 'rows', layout, active_group)

        if column_count > 1 or row_count > 1:
            self.window.run_command('set_layout', layout)
