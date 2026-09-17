import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import dataclasses
import queue

from virtualdj_client import (
    VirtualDJClient, 
    VdjDeckSong,
    VdjDeckEngine,
    VdjMixer, 
    VdjBrowserFolder, 
    VdjBrowserFile,
)
#---------------------------------------------------------------------------------------
class VirtualDJMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("VirtualDJ Client")
        self.geometry("1024x768")
        self._define_menu()
        self._define_tab()
        self.interval_refresh = 100  # ms

        self.client: VirtualDJClient | None = None
        self.loop: asyncio.AbstractEventLoop | None = None
        self._stopping = threading.Event()
        self._result_queue = queue.Queue(maxsize=1)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.async_thread = threading.Thread(target=self._run_async_client, daemon=True)
        self.async_thread.start()
        self.after(self.interval_refresh, self.refresh_ui)
    #------------------------------------------------------------------------------------
    def on_close(self):
        if self._stopping.is_set():
            return
        self._stopping.set()
        self.destroy()
    #------------------------------------------------------------------------------------
    def _define_menu(self):
        menubar = tk.Menu(self)

        help_menu = tk.Menu(menubar , tearoff=False)
        help_menu.add_command(label="Exit", command=self.on_close)
        help_menu.add_command(label="About", command=self._show_about)
        
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)
     #------------------------------------------------------------------------------------
    def _show_about(self):
        messagebox.showinfo("About VirtualDJ Client",
                            "version: 1.1.8\n\n"
                            "developped by DJCEL")
    #------------------------------------------------------------------------------------
    def _define_tab(self):
        """ we define 2 tabs """
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both",expand=True)
        self.get_tab = ttk.Frame(self.notebook)
        self.send_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.get_tab,text="Get")
        self.notebook.add(self.send_tab,text="Send")

        """ GET tab """
        self._define_frame_get(self.get_tab)

        """ SEND tab """
        self._define_frame_send(self.send_tab)
        
    #------------------------------------------------------------------------------------
    def _define_frame_get(self, parent):
        frames_get_definition = [
            ("leftdecksong", "leftdecksong_frame", "Left Deck - Song",
     lambda client: client.get_DeckSong_async("left")),
            ("leftdeckengine", "leftdeckengine_frame", "Left Deck - Engine",
     lambda client: client.get_DeckEngine_async("left")),
            ("rightdecksong", "rightdecksong_frame", "Right Deck - Song",
     lambda client: client.get_DeckSong_async("right")),
            ("rightdeckengine", "rightdeckengine_frame", "Rigth Deck - Engine",
     lambda client: client.get_DeckEngine_async("right")),
            ("mixer", "mixer_frame", "Mixer",
     lambda client: client.get_Mixer_async()),
            ("browserfolder", "browserfolder_frame", "Browser - Folder",
     lambda client: client.get_BrowserFolder_async()),
            ("browserfile", "browserfile_frame", "Browser - File",
     lambda client: client.get_BrowserFile_async()),
        ]

        self.frames_get = {}

        for row, (name, frame_id, frame_title, getter) in enumerate(frames_get_definition):
            frame = self._make_frame(parent, frame_title)
            setattr(self, frame_id, frame)
            self.frames_get[name] = {"frame": frame, "getter": getter}
            parent.grid_rowconfigure(row, weight=1,minsize=0)
            frame.grid(row=row,column=0,sticky="nsew",padx=10,pady=5)

        parent.grid_columnconfigure(0,weight=1)

    #------------------------------------------------------------------------------------
    def _define_frame_send(self, parent):
      
        self.vdjscript_frame = ttk.LabelFrame(parent, text="VdjScript")
        self.vdjscript_frame.pack(fill="x",padx=10,pady=5)
        self.vdjscript_entry = ttk.Entry(self.vdjscript_frame)
        self.vdjscript_entry.pack(side="left",fill="x",expand=True,padx=5,pady=5)
        self.send_button = ttk.Button(self.vdjscript_frame, text="Send", command=self._send_vdjscript)
        self.send_button.pack(side="right",padx=5,pady=5)
        self.vdjscript_entry.bind("<Return>",lambda event:self._send_vdjscript())
    #------------------------------------------------------------------------------------
    def _send_vdjscript(self):
        vdjscript = self.vdjscript_entry.get().strip()
        if not vdjscript:
            return
        if self.client is None:
            return
        if self.loop is None:
            return
        try:
            future = asyncio.run_coroutine_threadsafe(self.client.send_async(vdjscript), self.loop)
            future.add_done_callback(self._vdjscript_done)
        except Exception as e:
            pass
    #------------------------------------------------------------------------------------
    def _vdjscript_done(self, future):
        try:
            result = future.result()
        except Exception as e:
            pass
    #------------------------------------------------------------------------------------
    def _make_frame(self, parent, title: str):
        frame = ttk.LabelFrame(parent,text=title)
        text = tk.Text(frame, height=1, state='disabled', font=("Consolas",10))
        text.pack(fill="both", expand=True)
        frame.text_widget = text
        return frame
    #------------------------------------------------------------------------------------
    def _update_frame_text(self, frame, vdjdata):
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
            self.loop.run_until_complete(self._client_main_get())
        finally:
            self.loop.close()
            self.loop = None
    #------------------------------------------------------------------------------------
    async def _client_main_get(self):
        async with VirtualDJClient() as client:
            self.client = client
            tasks = [asyncio.create_task(self._poll_data(client, name, config)) for name, config in self.frames_get.items()]
                   
            try:
                await asyncio.gather(*tasks)
            finally:
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                   
            self.client = None
    #------------------------------------------------------------------------------------
    async def _poll_data(self, client, name, config):
        getter = config["getter"]

        while not self._stopping.is_set():
            start_time = asyncio.get_running_loop().time()

            try:
                value = await getter(client)
            except Exception as e:
                value = e
            
            result_dict = {"name": name, "value": value}
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
                value = result["value"]
                config = self.frames_get.get(name)
                if config is not None:
                    self._update_frame_text(config["frame"], value)
                 
        except queue.Empty:
            pass

        if not self._stopping.is_set():
            self.after(self.interval_refresh, self.refresh_ui)
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()