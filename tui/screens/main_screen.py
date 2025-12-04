from textual.screen import Screen
from textual.widgets import Static
from textual import events


class MainScreen(Screen):
    async def on_mount(self) -> None:
        await self.mount(Static("Main Screen - Press Esc to return to launcher.", expand=True))

    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            await self.app.pop_screen()
