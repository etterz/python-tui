from textual.screen import Screen
from textual.widgets import Static
from textual import events
from typing import Optional
import asyncio
import datetime


def run_function(value: str) -> str:
    return f"Result: {value}\nProcessed at {datetime.datetime.now().isoformat()}"


class FormScreen(Screen):
    input_buffer: str = ""
    input_widget: Optional[Static] = None
    output_widget: Optional[Static] = None

    async def on_mount(self) -> None:
        await self.mount(Static("Form - type text and press Enter to run. Esc to go back.", id="instr"))
        self.input_widget = Static("Input: ", id="input")
        await self.mount(self.input_widget)
        self.output_widget = Static("Output:\n", id="output", expand=True)
        await self.mount(self.output_widget)

    async def on_key(self, event: events.Key) -> None:
        key = event.key
        if key == "escape":
            # Return to the launcher menu
            await self.app.pop_screen()
            return
        if key == "enter":
            value = self.input_buffer
            self.input_buffer = ""
            if self.input_widget:
                self.input_widget.update(f"Input: {self.input_buffer}")
            result = await asyncio.to_thread(run_function, value)
            prev = getattr(self.output_widget, "_text", "") or ""
            new = (prev + "\n\n" + result) if prev else result
            if self.output_widget:
                self.output_widget.update(new)
            return
        if key == "backspace":
            self.input_buffer = self.input_buffer[:-1]
            if self.input_widget:
                self.input_widget.update(f"Input: {self.input_buffer}")
            return
        if len(key) == 1:
            self.input_buffer += key
            # Static.update is synchronous; do not await
            if self.input_widget:
                self.input_widget.update(f"Input: {self.input_buffer}")


class FormWidget(Static):
    """A lightweight in-place form widget that can be mounted into the
    main app's body area so header/footer remain visible.

    This mirrors the behavior of the old FormScreen but does not replace
    the entire app screen stack.
    """
    def __init__(self, *, id: Optional[str] = "form-widget") -> None:
        super().__init__("", id=id, expand=True)
        self.input_buffer: str = ""
        self.output_text: str = ""

    async def on_mount(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        content = [
            "Form - type text and press Enter to run. Esc to go back.",
            "",
            f"Input: {self.input_buffer}",
            "",
            "Output:",
            self.output_text,
        ]
        self.update("\n".join(content))

    async def on_key(self, event: events.Key) -> None:
        key = event.key
        if key == "escape":
            # Signal the parent app to close the form (if supported)
            if hasattr(self.app, "_close_form"):
                await self.app._close_form()
            return
        if key == "enter":
            value = self.input_buffer
            self.input_buffer = ""
            result = await asyncio.to_thread(run_function, value)
            if self.output_text:
                self.output_text += "\n\n" + result
            else:
                self.output_text = result
            self._refresh()
            return
        if key == "backspace":
            self.input_buffer = self.input_buffer[:-1]
            self._refresh()
            return
        if len(key) == 1:
            self.input_buffer += key
            self._refresh()
