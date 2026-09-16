import tkinter as tk
from tkinter import ttk
import asyncio
import threading
import dataclasses
import queue

from virtualdj_client import (
    VirtualDJClient, 
    VdjDeckData, 
    VdjMixer, 
    VdjBrowserFolder, 
    VdjBrowserFile,
)
#---------------------------------------------------------------------------------------
class VirtualDJMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VirtualDJ - Monitor")
        self.geometry("1024x768")
        self.client: VirtualDJClient | None = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self._stopping = threading.Event()
        self._result_queue = queue.Queue(maxsize=1)
        self.interval_refresh = 100  # ms
        self._define_frame()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.async_thread = threading.Thread(target=self._run_async_client, daemon=True)
        self.async_thread.start()
        self.after(self.interval_refresh, self.refresh_ui)
    #------------------------------------------------------------------------------------
    def on_close(self):
        if self._stopping.is_set():
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

            widget.insert("end", data)

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
            while not self._stopping.is_set():
                try:
                    result = await self._refresh_data(client)
                    try:
                        self._result_queue.get_nowait()
                    except queue.Empty:
                        pass
                    try:
                        self._result_queue.put_nowait(result)
                    except queue.Full:
                        pass
                except Exception as exc:
                    try:
                        self._result_queue.get_nowait()
                    except queue.Empty:
                        pass
                    try:
                        self._result_queue.put_nowait({"error": exc})
                    except queue.Full:
                        pass

                await asyncio.sleep(self.interval_refresh / 1000)
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
    async def _refresh_data(self, client: VirtualDJClient):
        """ Async request """
        (leftdeck, rightdeck, mixer, browserfolder, browserfile) = await asyncio.gather(
            client.get_DeckData_async("left"),
            client.get_DeckData_async("right"),
            client.get_Mixer_async(),
            client.get_BrowserFolder_async(),
            client.get_BrowserFile_async(),
        )
        return {
            "leftdeck" : leftdeck,
            "rightdeck" : rightdeck,
            "mixer": mixer,
            "browserfolder": browserfolder,
            "browserfile": browserfile,
            }
    #------------------------------------------------------------------------------------
    def refresh_ui(self):
        try:
            while True:
                result = self._result_queue.get_nowait()

                if "error" in result:
                    self._update_frame_text(self.leftdeck_frame, f"Refresh error: {result["error"]}")
                    continue

                self._update_frame_text(self.leftdeck_frame, result["leftdeck"])
                self._update_frame_text(self.rightdeck_frame, result["rightdeck"])
                self._update_frame_text(self.mixer_frame, result["mixer"])
                self._update_frame_text(self.browserfolder_frame, result["browserfolder"])
                self._update_frame_text(self.browserfile_frame, result["browserfile"])

        except queue.Empty:
            pass

        if not self._stopping.is_set():
            self.after(self.interval_refresh, self.refresh_ui)
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()