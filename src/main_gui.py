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
        self.ui_refresh_interval_ms = 100  # refresh each 100ms
        self._define_frame()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.async_thread = threading.Thread(target=self._run_async_client, daemon=True)
        self.async_thread.start()
        self.after(self.ui_refresh_interval_ms, self.refresh_ui)
    #------------------------------------------------------------------------------------
    def on_close(self):
        if self._stopping:
            return
        self._stopping = True
        self.destroy()
    #------------------------------------------------------------------------------------
    def _make_frame(self, title: str):
        frame = ttk.LabelFrame(self,text=title)
        text = tk.Text(frame, height=8, state='disabled', font=("Consolas",10))
        text.pack(fill="both", expand=True)
        frame.text_widget = text
        return frame
    #------------------------------------------------------------------------------------
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

            widget.insert("end", str(data))

        widget.configure(state="disabled")
    #------------------------------------------------------------------------------------
    def _run_async_client(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_until_complete(self._client_main())
        finally:
            self.loop.close()
            self.loop = None
    #------------------------------------------------------------------------------------
    async def _client_main(self):
        async with VirtualDJClient() as client:
            self.client = client
            while not self._stopping:
                await asyncio.sleep(0.2)
            self.client = None
    #------------------------------------------------------------------------------------
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
    #------------------------------------------------------------------------------------
    async def _get_all_data(self):
        """ Async request """
        if self.client is None:
             return None
        leftdeck = await self.client.get_DeckData_async("left")
        rightdeck = await self.client.get_DeckData_async("right")
        mixer = await self.client.get_Mixer_async()
        browserfolder = await self.client.get_BrowserFolder_async()
        browserfile = await self.client.get_BrowserFile_async()
        results =  (leftdeck, rightdeck, mixer, browserfolder, browserfile)
        return results
    #------------------------------------------------------------------------------------
    def _on_result(future):
        try:
            results = future.result()
            self.after(0, self._update_ui, results)
        except Exception as e:
            print(f"Request error: {e}")
    #------------------------------------------------------------------------------------
    def refresh_ui(self):
        """ GUI refresh """
        if (not self._stopping and self.loop is not None and self.client is not None):
            future = asyncio.run_coroutine_threadsafe(self._get_all_data(), self.loop)
            def on_result(future):
                try:
                    results = future.result()
                    self.after(0, self._update_ui, results)
                except Exception as e:
                    print(f"Request error: {e}")
            future.add_done_callback(on_result)

        if not self._stopping:
            self.after(self.ui_refresh_interval_ms, self.refresh_ui)
    #------------------------------------------------------------------------------------
    def update_ui(self, results):
        (leftdeck, rightdeck, mixer, browserfolder, browserfile) = results
        self._update_frame_text(self.leftdeck_frame, leftdeck)
        self._update_frame_text(self.rightdeck_frame, rightdeck)
        self._update_frame_text(self.mixer_frame, mixer)
        self._update_frame_text(self.browserfolder_frame, browserfolder)
        self._update_frame_text(self.browserfile_frame, browserfile)
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()