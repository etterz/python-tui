from textual.app import App
from textual.widgets import Header, Static, Footer
from tui.screens.form_screen import FormScreen, FormWidget
from textual import events
import asyncio
from typing import Optional
from pathlib import Path
from datetime import datetime
import textual


class UpdatableFooter(Footer):
    """Footer that contains a left-side Static we can update at runtime.

    We mount a small `Static` inside the Footer during `on_mount` and
    expose `set_help(text)` to update that left area. This places the
    help text inside the real bottom footer pane.
    """
    def __init__(self, help_text: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self._help_text = help_text
        self._left: Optional[Static] = None

    async def on_mount(self) -> None:  # type: ignore[override]
        # mount a left-aligned Static inside the Footer
        self._left = Static(self._help_text, id="footer-left")
        await self.mount(self._left)

    def set_help(self, text: str) -> None:
        if self._left:
            try:
                self._left.update(text)
            except Exception:
                pass


class BottomBar(Static):
    """A simple bottom bar widget that acts like a footer and is always visible.

    Use `set_help(text)` to update the displayed help/palette text.
    """
    def __init__(self, text: str = "", **kwargs) -> None:
        super().__init__(text, **kwargs)

    def set_help(self, text: str) -> None:
        try:
            self.update(text)
        except Exception:
            pass


class MainApp(App):
    """Main TUI launcher with a menu interface to open different screens.

    Shows available screens/features with keyboard shortcuts.
    Press Ctrl+X q to quit.
    """

    BINDINGS = []

    AVAILABLE_SCREENS = [
        ("f", "Form", "Open form to run functions and view output"),
    ]

    async def on_mount(self) -> None:
        await self.mount(Header())

        # Footer/help text used for persistent/help display
        self._footer_help = "Ctrl+X then <key> activates commands"

        # Add a small header-area help Static so persistent help is visible
        # at the top of the app (reliable in VS Code terminals).
        self._header_help = Static(f"^P  {self._footer_help}", id="header-help", expand=False)
        try:
            await self.view.dock(self._header_help, edge="top", size=1)
        except Exception:
            try:
                await self.mount(self._header_help)
            except Exception:
                self._header_help = None

        # Build the launcher menu (dock it so the bottom bar remains visible)
        menu_text = self._build_menu()
        self._menu_widget = Static(menu_text, id="menu", expand=True)
        try:
            await self.view.dock(self._menu_widget, edge="top")
        except Exception:
            # fall back to mount if docking isn't supported
            await self.mount(self._menu_widget)


        # Mount a Footer subclass (UpdatableFooter) so the help text appears
        # inside the real bottom footer pane. We include a small palette
        # indicator prefix before the help text.
        # Prefer docking the real UpdatableFooter into the app view bottom
        # (this places the help inside the true Footer if the Textual
        # environment supports it). If docking fails, fall back to the
        # controlled BottomBar and dock/mount that instead.
        self._built_footer = UpdatableFooter(help_text=f"^P  {self._footer_help}")
        self._using_built_footer = False
        try:
            # try to dock the UpdatableFooter at the bottom of the view
            # request a single-line height to increase chance of visibility
            # request two lines for the footer so it's visible above any
            # terminal/IDE status bars that may obscure the last row.
            await self.view.dock(self._built_footer, edge="bottom", size=2)
            self._using_built_footer = True
        except Exception:
            try:
                # docking failed; fall back to a BottomBar
                self._bottom_bar = BottomBar(f"^P  {self._footer_help}", id="bottom-bar", expand=False)
                try:
                    self._bottom_bar.styles.padding = (0, 1)
                    self._bottom_bar.styles.background = "dark_blue"
                    self._bottom_bar.styles.color = "white"
                except Exception:
                    pass
                try:
                    # request two lines for the bottom bar
                    await self.view.dock(self._bottom_bar, edge="bottom", size=2)
                except Exception:
                    # docking the bottom bar failed; mount as a last resort
                    try:
                        await self.mount(self._bottom_bar)
                    except Exception:
                        pass
            except Exception:
                # if even creating BottomBar failed, continue silently
                pass
        # Ensure log directory exists and initial help is recorded
        try:
            self._log_path = Path.cwd() / "logs" / "tui_events.log"
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception:
            self._log_path = None
        # Ensure the mounted footer shows the initial help text immediately.
        try:
            if hasattr(self, "_built_footer") and getattr(self, "_built_footer"):
                display = f"^P  {self._footer_help}"
                try:
                    self._built_footer.set_help(display)
                except Exception:
                    try:
                        self._built_footer.update(display)
                    except Exception:
                        pass
                try:
                    await self._built_footer.refresh()
                except Exception:
                    pass
        except Exception:
            pass
        try:
            if getattr(self, "_log_path", None):
                if getattr(self, "_using_built_footer", False):
                    self._file_log("Docked UpdatableFooter and set initial help")
                else:
                    self._file_log("Mounted/docked BottomBar and set initial help")
        except Exception:
            pass
        # Inspect the mounted footer to ensure its left Static is present
        # Inspect mounted bottom bar for visibility
        try:
            self._inspect_footer()
            # dump widget tree for debugging
            try:
                self._dump_widget_tree()
            except Exception:
                pass
            # try forcing a UI/layout refresh to encourage rendering
            try:
                # prefer awaiting if refresh is async
                try:
                    await self.refresh()
                except TypeError:
                    # maybe refresh is not awaitable
                    try:
                        self.refresh()
                    except Exception:
                        pass
            except Exception:
                pass
        except Exception:
            pass
        # Ensure the mounted footer shows the initial help text immediately.
        try:
            if getattr(self, "_bottom_bar", None):
                # Ensure bottom bar content is set and visible right away.
                display = f"^P  {self._footer_help}"
                try:
                    self._bottom_bar.set_help(display)
                except Exception:
                    try:
                        self._bottom_bar.update(display)
                    except Exception:
                        pass
                try:
                    await self._bottom_bar.refresh()
                except Exception:
                    pass
        except Exception:
            pass

    def _build_menu(self) -> str:
        """Build the launcher menu text display."""
        lines = [
            "╔════════════════════════════════════════╗",
            "║         TUI Application Launcher       ║",
            "╚════════════════════════════════════════╝",
            "",
            "Available Screens:",
            "──────────────────────────────────────────",
        ]
        for key, name, desc in self.AVAILABLE_SCREENS:
            lines.append(f"  [{key}]  {name:<20} {desc}")
        lines.extend([
            "",
            "Global Shortcuts:",
            "──────────────────────────────────────────",
            "  [Ctrl+X q]  Quit the application",
            "",
            "Tip: Press a key above to launch that screen.",
        ])
        return "\n".join(lines)

    async def on_key(self, event: events.Key) -> None:
        key = event.key

        # Debug log the key event to help diagnose terminal mappings
        try:
            char = getattr(event, "character", None)
        except Exception:
            char = None
        self.log(
            f"Key event: key={key!r}, character={char!r}, ctrl={getattr(event,'ctrl',False)}, alt={getattr(event,'alt',False)}, shift={getattr(event,'shift',False)}"
        )
        # Fallback: print to stdout so users running from a shell always see
        # the key event diagnostic even if Textual's logger isn't visible.
        try:
            print(
                f"Key event: key={key!r}, character={char!r}, ctrl={getattr(event,'ctrl',False)}, alt={getattr(event,'alt',False)}, shift={getattr(event,'shift',False)}"
            )
        except Exception:
            pass
        # Also append to the diagnostic log file if available
        try:
            if getattr(self, "_log_path", None):
                self._file_log(
                    f"Key event: key={key!r}, character={char!r}, ctrl={getattr(event,'ctrl',False)}, alt={getattr(event,'alt',False)}, shift={getattr(event,'shift',False)}"
                )
        except Exception:
            pass

        # If an in-place current view is mounted (e.g. the FormWidget), forward
        # the key event directly to it so that the widget can handle navigation
        # like Escape. This keeps header/footer visible while the widget
        # receives input.
        if getattr(self, "_current_view", None):
            try:
                await self._current_view.on_key(event)
                return
            except Exception:
                pass

        # If we're currently in chord mode, consume the next key
        if getattr(self, "_chord_mode", False):
            self._chord_mode = False
            # clear indicator immediately
            await self._clear_chord_indicator()
            if key.lower() == "q":
                self.exit()
            return

        # Robust detection for Ctrl+X: modifier + 'x' or Ctrl-X control char
        is_ctrl_x = False
        if getattr(event, "ctrl", False) and key == "x":
            is_ctrl_x = True
        elif char:
            try:
                if isinstance(char, str) and len(char) == 1 and ord(char) == 24:
                    is_ctrl_x = True
            except Exception:
                pass

        if is_ctrl_x:
            self._chord_mode = True
            self.log("Entered chord mode (prefix detected)")
            # show transient on-screen indicator
            await self._show_chord_indicator("Chord: Ctrl+X — waiting for next key")
            return

        # Direct key mapping for screen shortcuts
        if key == "f":
            await self._open_form()
            return

    async def _open_form(self) -> None:
        """Replace the menu with an in-place form widget so header/footer remain visible."""
        if getattr(self, "_current_view", None):
            return
        if getattr(self, "_menu_widget", None):
            try:
                await self._menu_widget.remove()
            except Exception:
                pass
            self._menu_widget = None
        self._current_view = FormWidget()
        await self.mount(self._current_view)

    async def _close_form(self) -> None:
        """Remove the in-place form and restore the launcher menu."""
        if getattr(self, "_current_view", None):
            try:
                await self._current_view.remove()
            except Exception:
                pass
            self._current_view = None
        menu_text = self._build_menu()
        self._menu_widget = Static(menu_text, id="menu", expand=True)
        try:
            await self.view.dock(self._menu_widget, edge="top")
        except Exception:
            await self.mount(self._menu_widget)

    async def _show_chord_indicator(self, text: str, timeout: float = 3.0) -> None:
        """Show a transient chord indicator in the footer bar for `timeout` seconds."""
        # Prefer updating header help (always visible in IDE). Fall back to bottom bar/footer.
        target_footer = getattr(self, "_header_help", None) or getattr(self, "_bottom_bar", None) or getattr(self, "_built_footer", None) or getattr(self, "_footer_bar", None)
        if not target_footer:
            return
        try:
            # show transient text in the footer's left area (include small palette)
            # fall back to calling `update` if the object exposes it
            display = f"^P  {text}"
            if hasattr(target_footer, "set_help"):
                target_footer.set_help(display)
            else:
                try:
                    target_footer.update(display)
                except Exception:
                    pass
        except Exception:
            pass

        # Also update the visible bottom bar explicitly so external terminals see it.
        try:
            if getattr(self, "_bottom_bar", None):
                self._bottom_bar.update(f"^P  {text}")
        except Exception:
            pass
        # also write to the file log so we can inspect later
        try:
            if getattr(self, "_log_path", None):
                self._file_log(f"Show chord indicator: {text}")
        except Exception:
            pass
        try:
            if getattr(self, "_chord_clear_task", None) and not self._chord_clear_task.done():
                self._chord_clear_task.cancel()
        except Exception:
            pass
        self._chord_clear_task = asyncio.create_task(self._delayed_clear_chord_indicator(timeout))

    async def _delayed_clear_chord_indicator(self, timeout: float) -> None:
        await asyncio.sleep(timeout)
        await self._clear_chord_indicator()

    async def _clear_chord_indicator(self) -> None:
        target_footer = getattr(self, "_header_help", None) or getattr(self, "_bottom_bar", None) or getattr(self, "_built_footer", None) or getattr(self, "_footer_bar", None)
        if not target_footer:
            return
        try:
            display = f"^P  {self._footer_help}"
            if hasattr(target_footer, "set_help"):
                target_footer.set_help(display)
            else:
                try:
                    target_footer.update(display)
                except Exception:
                    pass
        except Exception:
            pass
        # Also update our explicit bottom bar if present
        try:
            if getattr(self, "_bottom_bar", None):
                self._bottom_bar.update(display)
        except Exception:
            pass
        try:
            if getattr(self, "_log_path", None):
                self._file_log("Cleared chord indicator / reset help")
        except Exception:
            pass

    def _file_log(self, message: str) -> None:
        """Append a timestamped diagnostic message to the workspace log file.

        The log file is created under `./logs/tui_events.log` relative to the
        current working directory where the TUI is launched.
        """
        try:
            if not getattr(self, "_log_path", None):
                return
            ts = datetime.utcnow().isoformat() + "Z"
            with open(self._log_path, "a", encoding="utf-8") as fh:
                fh.write(f"{ts} - {message}\n")
        except Exception:
            pass

    def _inspect_footer(self) -> None:
        """Log and file-log the current state of the mounted footer and its left child."""
        try:
            built = getattr(self, "_built_footer", None)
            bottom = getattr(self, "_bottom_bar", None)
            msg = f"Inspect footer: built_footer={built!r}, bottom_bar={bottom!r}"
            self.log(msg)
            if getattr(self, "_log_path", None):
                self._file_log(msg)
            # If we have an UpdatableFooter, inspect its _left child.
            if built:
                left = getattr(built, "_left", None)
                msg2 = f"Inspect footer: _left={left!r}, id={getattr(left,'id',None)}"
                self.log(msg2)
                if getattr(self, "_log_path", None):
                    self._file_log(msg2)
            # If we have a BottomBar, log its id and current renderable.
            if bottom:
                try:
                    msg3 = f"Inspect bottom_bar: id={getattr(bottom,'id',None)}, renderable={getattr(bottom,'renderable',None)}"
                except Exception:
                    msg3 = f"Inspect bottom_bar: id={getattr(bottom,'id',None)}"
                self.log(msg3)
                if getattr(self, "_log_path", None):
                    self._file_log(msg3)
            # Log textual version for debugging
            try:
                ver = getattr(textual, "__version__", None)
                vmsg = f"Textual version: {ver}"
                self.log(vmsg)
                if getattr(self, "_log_path", None):
                    self._file_log(vmsg)
            except Exception:
                pass
            # attempt to apply styling to the left static to make it stand out
            if built and getattr(built, "_left", None):
                left = getattr(built, "_left")
                try:
                    # try applying padding and colors; fail silently if API differs
                    left.styles.padding = (0, 1)
                    left.styles.background = "dark_blue"
                    left.styles.color = "white"
                    self.log("Applied styles to footer-left Static")
                    if getattr(self, "_log_path", None):
                        self._file_log("Applied styles to footer-left Static")
                except Exception:
                    try:
                        # as a fallback, prefix the help with visual marker
                        left.update(f">> {left.renderable if hasattr(left, 'renderable') else ''}")
                    except Exception:
                        pass
        except Exception:
            pass

    def _dump_widget_tree(self) -> None:
        """Write a concise dump of the current view/widget tree to the log file.

        This helps identify whether the bottom bar widget is present in the
        layout and what its `renderable` is at runtime.
        """
        try:
            lines = []
            def node_repr(w, depth=0):
                try:
                    wid = getattr(w, "id", None)
                except Exception:
                    wid = None
                try:
                    rend = getattr(w, "renderable", None)
                except Exception:
                    rend = None
                prefix = "  " * depth
                lines.append(f"{prefix}{w.__class__.__name__} id={wid!r} renderable={rend!r}")
                try:
                    children = getattr(w, "children", [])
                except Exception:
                    children = []
                for c in children:
                    node_repr(c, depth+1)

            root = getattr(self, "view", None)
            if root is None:
                return
            node_repr(root, 0)
            dump = "\n".join(lines)
            self.log("Widget tree:\n" + dump)
            if getattr(self, "_log_path", None):
                self._file_log("Widget tree:\n" + dump)
        except Exception:
            pass

    async def _delayed_inspect_footer(self) -> None:
        await asyncio.sleep(0.05)
        try:
            self._inspect_footer()
        except Exception:
            pass


def main() -> None:
    """Launch the TUI application with a TUI-based menu."""
    MainApp().run()


if __name__ == "__main__":
    main()
