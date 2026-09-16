import tkinter as tk
from tkinter import ttk
import asyncio
import threading
import dataclasses

from virtualdj_client import VirtualDJClient, VdjDeckData, VdjMixer, VdjBrowserFolder, VdjBrowserFile

class VirtualDJMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VirtualDJ - Monitor")
        self.geometry("1024x768")
        self.client: VirtualDJClient | None = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self._stopping = False
        self.interval_refresh = 100  # refresh each 100ms
        self._define_frame()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        threading.Thread(target=self._run_async_client, daemon=True).start()
        self.after(self.interval_refresh, self.refresh_ui)

    def on_close(self):
        self._stopping = True
        self.destroy()

    def _make_frame(self, title: str):
        frame = ttk.LabelFrame(self,text=title)
        text = tk.Text(frame, height=8, state='disabled', font=("Consolas",10))
        text.pack(fill="both", expand=True)
        frame.text_widget = text
        return frame

    def _update_frame_text(self,frame, vdjdata):
        widget = frame.text_widget
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        
        if vdjdata is None:
            widget.insert("end", "No data yet...")
        else:
            if dataclasses.is_dataclass(vdjdata):
                data = dataclasses.asdict(vdjdata)
            else:
                data = vars(vdjdata)

            widget.insert("end", data)

        widget.configure(state="disabled")

    def _run_async_client(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._client_main())
  

    async def _client_main(self):
        async with VirtualDJClient() as client:
            self.client = client
            while not self._stopping:
                await asyncio.sleep(0.2)

    def _define_frame(self):
        self.leftdeck_frame = self._make_frame("Left Deck")
        self.rightdeck_frame = self._make_frame("Right Deck")
        self.mixer_frame = self._make_frame("Mixer")
        self.browserfolder_frame = self._make_frame("Browser Folder")
        self.browserfile_frame = self._make_frame("Browser File")
        self.leftdeck_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.rightdeck_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.mixer_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.browserfolder_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.browserfile_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def refresh_ui(self):
        if self.client is not None:
            leftdeck = self.client.get_DeckData("left")
            self._update_frame_text(self.leftdeck_frame, leftdeck)
            rightdeck = self.client.get_DeckData("right")
            self._update_frame_text(self.rightdeck_frame, rightdeck)
            mixer = self.client.get_Mixer()
            self._update_frame_text(self.mixer_frame, mixer)
            browserfolder =  self.client.get_BrowserFolder()
            self._update_frame_text(self.browserfolder_frame, browserfolder)
            browserfile=  self.client.get_BrowserFile()
            self._update_frame_text(self.browserfile_frame, browserfile)
        if not self._stopping:
            self.after(self.interval_refresh,self.refresh_ui)

#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()