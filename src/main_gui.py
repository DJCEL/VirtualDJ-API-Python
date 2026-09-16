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
    def _define_frame(self):
        self.leftdecksong_frame = self._make_frame("Left Deck - Song")
        self.leftdeckengine_frame = self._make_frame("Left Deck - Engine")
        self.rightdecksong_frame = self._make_frame("Right Deck - Song")
        self.rightdeckengine_frame = self._make_frame("Right Deck - Engine")
        self.mixer_frame = self._make_frame("Mixer")
        self.browserfolder_frame = self._make_frame("Browser - Folder")
        self.browserfile_frame = self._make_frame("Browser - File")

        self.leftdecksong_frame.pack(fill="both", expand=True, padx=10, pady=2)
        self.leftdeckengine_frame.pack(fill="both", expand=True, padx=10, pady=2)
        self.rightdecksong_frame.pack(fill="both", expand=True, padx=10, pady=2)
        self.rightdeckengine_frame.pack(fill="both", expand=True, padx=10, pady=2)
        self.mixer_frame.pack(fill="both", expand=True, padx=10, pady=2)
        self.browserfolder_frame.pack(fill="both", expand=True, padx=10, pady=2)
        self.browserfile_frame.pack(fill="both", expand=True, padx=10, pady=2)
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
            tasks = [
                asyncio.create_task(self._poll_data(client,"leftdecksong" , lambda: client.get_DeckSong_async("left") )),
                asyncio.create_task(self._poll_data(client,"leftdeckengine" , lambda: client.get_DeckEngine_async("left") )),
                asyncio.create_task(self._poll_data(client,"rightdecksong", lambda: client.get_DeckSong_async("right"))),
                asyncio.create_task(self._poll_data(client,"rightdeckengine", lambda: client.get_DeckEngine_async("right"))),
                asyncio.create_task(self._poll_data(client,"mixer", lambda: client.get_Mixer_async())),
                asyncio.create_task(self._poll_data(client,"browserfolder", lambda: client.get_BrowserFolder_async())),
                asyncio.create_task(self._poll_data(client,"browserfile", lambda: client.get_BrowserFile_async())),
            ]
                   
            try:
                await asyncio.gather(*tasks)
            finally:
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                   
            self.client = None
    #------------------------------------------------------------------------------------
    async def _poll_data(self, client, name, getter):
        while not self._stopping.is_set():
            start_time = asyncio.get_running_loop().time()

            try:
                result = await getter()
                result_dict = {"name": name, "value": result}
            except Exception as e:
                result_dict = {"name": name, "value": e}
            
            self._result_queue.put(result_dict)

            elapsed = asyncio.get_running_loop().time() - start_time
            delay = max(0.0, (self.interval_refresh / 1000) - elapsed)

            if delay > 0:
                try:
                    await asyncio.wait_for(self._stopping.wait(), timeout=delay)
                except asyncio.TimeoutError:
                    pass
    #------------------------------------------------------------------------------------
    def refresh_ui(self):
        try:
            while True:
                result = self._result_queue.get_nowait()
                name = result["name"]

                if "error" in result:
                    value = f"Refresh error: {result['error']}"
                else:
                    value = result["value"]
                 
                if name == "leftdecksong":
                    self._update_frame_text(self.leftdecksong_frame, value)
                elif name == "leftdeckengine":
                    self._update_frame_text(self.leftdeckengine_frame, value)
                elif name == "rightdecksong":
                    self._update_frame_text(self.rightdecksong_frame, value)
                elif name == "rightdeckengine":
                    self._update_frame_text(self.rightdeckengine_frame, value)
                elif name == "mixer":
                    self._update_frame_text(self.mixer_frame, value)
                elif name == "browserfolder":
                    self._update_frame_text(self.browserfolder_frame, value)
                elif name == "browserfile":
                    self._update_frame_text(self.browserfile_frame, value)
        except queue.Empty:
            pass

        if not self._stopping.is_set():
            self.after(self.interval_refresh, self.refresh_ui)
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()