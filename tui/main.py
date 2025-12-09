import asyncio
from pathlib import Path
from datetime import datetime
from typing import ClassVar
import textual
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical
from textual.screen import Screen
from textual.binding import Binding
from textual.message import Message
from textual.widget import Widget
from textual import on, log, events
from tui.screens.form_screen import FormWidget


# --- Utility Widgets ---

class BottomBar(Static):
    """A simple bottom bar widget that acts like a footer and is always visible."""
    
    def __init__(self, text: str = "", **kwargs) -> None:
        # Initialize Static with the initial text
        super().__init__(text, **kwargs)
        # Store the current content internally for comparison
        self._current_text = text 

    def set_help(self, text: str) -> None:
        """
        Update the help text. This is safer than updating renderable directly.
        """
        # CRITICAL FIX: The check must be against the widget's own state, 
        # not a private variable from the parent class.
        if not text or text == self._current_text:
            return
            
        self._current_text = text
        self.update(text)


class UpdatableFooter(Footer):
    """
    Custom Footer that allows a Static component (BottomBar) to be docked 
    and updated for persistent help text.
    
    NOTE: This uses the Footer widget, which is typically fixed to the bottom.
    The CustomFooter/Footer usually manages its own content/bindings.
    We are overriding the composition to include the BottomBar.
    """
    
    # Textual Footers are composed of internal elements, but we'll adapt
    # by making the BottomBar the *actual* Footer component in MainApp.
    # The CustomFooter class logic seems designed for a different setup.
    # For a simple bottom bar, we'll use BottomBar directly in MainApp.
    pass # Leaving this empty to indicate that we will use BottomBar directly 
         # or refactor this class to be a container for the BottomBar if needed.


# --- Main Application ---

class MainApp(App):
    """Main TUI launcher with a menu interface to open different screens."""

    BINDINGS: ClassVar[list[Binding | tuple[str, str] | tuple[str, str, str]]] = [
        Binding("f", "show_form", "Open form to run functions and view output", key_display="F"),
        Binding("ctrl+q", "quit", "Quit the application", key_display="Ctrl+Q"),
    ]

    AVAILABLE_SCREENS = [
        ("f", "Form", "Open form to run functions and view output"),
    ]
    
    CSS = """
    #content {
        align: center middle;
        padding: 0 5;
    }
    #bottom-bar {
        dock: bottom;
        height: 1;
        background: #000080; /* Dark blue */
        color: white;
        padding: 0 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._footer_help = "Ctrl+X then <key> activates commands"
        self._log_path: Path | None = None
        self._chord_mode = False
        self._current_view: Widget | None = None
        self._menu_widget: Static | None = None
        self._bottom_bar: BottomBar | None = None
        self._chord_clear_task: asyncio.Task | None = None

    def compose(self) -> ComposeResult:
        """Yield widgets for the main view."""
        yield Header()
        
        # Main content area
        with Vertical(id="content"):
            menu_text = self._build_menu()
            self._menu_widget = Static(menu_text, id="menu", expand=True)
            yield self._menu_widget
            
        # Use BottomBar directly instead of a complex CustomFooter/UpdatableFooter setup
        self._bottom_bar = BottomBar(f" {self._footer_help}", id="bottom-bar")
        yield self._bottom_bar

    async def on_mount(self) -> None:
        """Called after the application is mounted to the DOM."""
        
        # 1. Setup logging path
        try:
            self._log_path = Path.cwd() / "logs" / "tui_events.log"
            self._log_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # Only suppress if mkdir fails, but log it to the console
            self.log(f"Error setting up log directory: {e}")
            self._log_path = None
        
        # 2. Update initial help text (only if a log path was successfully created)
        if self._log_path:
            # NOTE: Assuming you added 'import textual' to fix the previous NameError
            self._file_log(f"TUI application started. Textual version: {getattr(textual, '__version__', 'N/A')}")
        
        # 3. Ensure BottomBar is updated
        if self._bottom_bar:
            self._bottom_bar.set_help(f" {self._footer_help}")
            # FIX HERE: refresh() is synchronous, so remove 'await'
            self._bottom_bar.refresh()


    def _build_menu(self) -> str:
        """Build the launcher menu text display."""
        return "\n".join([
            "╔════════════════════════════════════════════╗",
            "║             TUI Application Launcher         ║",
            "╚════════════════════════════════════════════╝",
            "",
            "Available Screens:",
            "──────────────────────────────────────────────",
            "  [f]   Form          Open form to run functions",
            "",
            "Global Shortcuts:",
            "──────────────────────────────────────────────",
            "  [Ctrl+X q]  Quit the application (Chord Mode)",
            "",
            "Tip: Press a key above to launch that screen."
        ])

    # --- Actions (Called via bindings) ---

    def action_show_form(self) -> None:
        """Action for binding 'f' to open the form."""
        asyncio.create_task(self._open_form())

    # Textual App already has an action_quit for ctrl+q. We keep the manual one below
    # for the chord mode logic, but use the built-in action_quit binding.
    
    # --- Key Handling and Chord Mode ---

    async def on_key(self, event: events.Key) -> None:
        """Handle key presses for chord mode logic."""
        key = event.key
        
        # --- FIX 1: Logging - Replaced non-existent .ctrl, .alt, .shift attributes ---
        # We use event.name and event.character for safer, more reliable diagnostics.
        self.log(
            f"Key event: key={key!r}, name={event.name!r}, character={event.character!r}"
        )
        if self._log_path:
            self._file_log(
                f"Key event: key={key!r}, name={event.name!r}, character={event.character!r}"
            )
        
        # NOTE: If you are using Textual version 0.50.0 or newer, you should 
        # use 'self.app.check_bindings(event)' here to handle App-level bindings
        # before proceeding to manual logic like below.

        # 1. Forward key to current view if mounted (e.g., FormWidget)
        # This prevents App-level shortcuts from firing when a sub-screen is active.
        if self._current_view:
            # When a widget has focus, it handles key events before the App's on_key.
            # If you specifically need to bypass the standard event flow here, 
            # you would check event.stop propagation status. However, returning 
            # early based on _current_view is a valid pattern for simple view switching.
            return 
        
        # 2. Handle Chord Mode
        if self._chord_mode:
            self._chord_mode = False
            await self._clear_chord_indicator()
            
            # The key 'q' is consumed by the chord logic here
            if key.lower() == "q":
                self.exit()
                return

        # 3. Detect Chord Prefix (Ctrl+X)
        # --- FIX 2: Chord Detection - Check the event name for 'ctrl+x' ---
        # The key string is the most reliable cross-platform way to detect Ctrl+X
        # OR, for older terminals that map Ctrl+X to a character, check that too.
        is_ctrl_x = (
            key.lower() == "ctrl+x" or 
            getattr(event, "character", None) == "\x18" # ASCII for Ctrl+X
        )

        if is_ctrl_x:
            self._chord_mode = True
            self.log("Entered chord mode (prefix detected)")
            await self._show_chord_indicator("Chord: Ctrl+X — waiting for next key")
            return

        # 4. Handle Direct Key Mapping
        # This should usually be handled by App BINDINGS, but keeping the logic for direct key 'f'.
        if key == "f":
            await self._open_form()
            return
            
    # --- Screen Management ---

    async def _open_form(self) -> None:
        """Replace the menu with an in-place form widget so header/footer remain visible."""
        if self._current_view:
            return
            
        if self._menu_widget:
            await self._menu_widget.remove()
            self._menu_widget = None
            
        # CRITICAL: Ensure FormWidget is available/defined
        self._current_view = FormWidget()
        await self.query_one("#content").mount(self._current_view)

    async def _close_form(self) -> None:
        """Remove the in-place form and restore the launcher menu."""
        if self._current_view:
            await self._current_view.remove()
            self._current_view = None
            
        menu_text = self._build_menu()
        self._menu_widget = Static(menu_text, id="menu", expand=True)
        await self.query_one("#content").mount(self._menu_widget)

    # --- Footer/Indicator Logic ---

    async def _show_chord_indicator(self, text: str, timeout: float = 3.0) -> None:
        """Show a transient chord indicator in the bottom bar."""
        if not self._bottom_bar:
            return
            
        display = f" {text}"
        self._bottom_bar.set_help(display)

        if self._log_path:
            self._file_log(f"Show chord indicator: {text}")

        if self._chord_clear_task and not self._chord_clear_task.done():
            self._chord_clear_task.cancel()
            
        self._chord_clear_task = asyncio.create_task(self._delayed_clear_chord_indicator(timeout))

    async def _delayed_clear_chord_indicator(self, timeout: float) -> None:
        """Wait for timeout, then clear the chord indicator."""
        await asyncio.sleep(timeout)
        if self._chord_mode: # Only clear if we are not still waiting for a key
            return
        await self._clear_chord_indicator()

    async def _clear_chord_indicator(self) -> None:
        """Reset the bottom bar to the default help text."""
        if not self._bottom_bar:
            return

        display = f" {self._footer_help}"
        self._bottom_bar.set_help(display)

        if self._log_path:
            self._file_log("Cleared chord indicator / reset help")

    # --- Logging ---

    def _file_log(self, message: str) -> None:
        """Append a timestamped diagnostic message to the workspace log file."""
        if not self._log_path:
            return
        
        try:
            ts = datetime.utcnow().isoformat() + "Z"
            with open(self._log_path, "a", encoding="utf-8") as fh:
                fh.write(f"{ts} - {message}\n")
        except Exception as e:
            # We are inside a logger, so just log the failure to console/internal log
            self.log(f"Failed to write to file log: {e}")

# --- Launcher ---

def main() -> None:
    """Launch the TUI application with a TUI-based menu."""
    # We remove the outer try...except block to ensure Textual's App.run() 
    # executes its cleanup routines in the event of a crash.
    MainApp().run()


if __name__ == "__main__":
    main()