import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import dataclasses
import queue
import sys

from virtualdj_client import (
    VirtualDJClient, 
    VdjDeckSong,
    VdjDeckEngine,
    VdjMixer, 
    VdjBrowserFolder, 
    VdjBrowserFile,
    VirtualDJSongsDatabase,
)
#---------------------------------------------------------------------------------------
class VirtualDJMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.client: VirtualDJClient | None = None
        self._init_client()
        self.title("VirtualDJ Client")
        self.geometry("1024x768")
        self._define_menu()
        self._define_tab()
        self.interval_refresh = 100  # ms
        self._loop: asyncio.AbstractEventLoop | None = None
        self._stopping = threading.Event()
        self._result_queue = queue.Queue(maxsize=1)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._async_thread = threading.Thread(target=self._run_async_client, daemon=True)
        self._async_thread.start()
        self.after(self.interval_refresh, self.refresh_ui)
    #------------------------------------------------------------------------------------
    def on_close(self):
        if self._stopping.is_set():
            return
        self._stopping.set()
        self.destroy()
    #------------------------------------------------------------------------------------
    def _init_client(self):
        client = VirtualDJClient()
        self.client = client

        # Check if VirtualDJ is running
        client_running = client.is_app_running()
        print(f"VirtualDJ running => {client_running}")

        # Launch VirtualDJ if not running
        if client_running == False:
            print("Launching VirtualDJ...")
            client_launched = client.open_app()
            print(f"VirtualDJ launched => {client_launched}")
            client_running = client.is_app_running()
            print(f"VirtualDJ running => {client_running}")
            if (client_running == False):
                sys.exit()

        # Check the NetWork Control plugin
        client_connected = client.is_connected()
        print(f"VirtualDJ NetWork Control plugin connected => {client_connected}")
        if (client_connected == False):
            print("Check that the NetWork Control plugin is available and activated in VirtualDJ")
            sys.exit()
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
        self.notebook.add(self.get_tab,text="Get")
        self.send_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.send_tab,text="Send")
        self.songDB_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.songDB_tab,text="Songs database")

        """ GET tab """
        self._define_tab_get(self.get_tab)

        """ SEND tab """
        self._define_tab_send(self.send_tab)

        """ SONGSDB tab """
        self._define_tab_songsdb(self.songDB_tab)
    #------------------------------------------------------------------------------------
    def _define_tab_get(self, parent):
        frames_get_definition = [
            ("leftdecksong", "leftdecksong_frame", "Left Deck - Song", lambda client: client.get_DeckSong_async("left")),
            ("leftdeckengine", "leftdeckengine_frame", "Left Deck - Engine", lambda client: client.get_DeckEngine_async("left")),
            ("rightdecksong", "rightdecksong_frame", "Right Deck - Song", lambda client: client.get_DeckSong_async("right")),
            ("rightdeckengine", "rightdeckengine_frame", "Rigth Deck - Engine", lambda client: client.get_DeckEngine_async("right")),
            ("mixer", "mixer_frame", "Mixer", lambda client: client.get_Mixer_async()),
            ("browserfolder", "browserfolder_frame", "Browser - Folder", lambda client: client.get_BrowserFolder_async()),
            ("browserfile", "browserfile_frame", "Browser - File", lambda client: client.get_BrowserFile_async()),
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
    def _define_tab_send(self, parent):
        self.vdjscript_frame = ttk.LabelFrame(parent, text="VdjScript")
        self.vdjscript_frame.pack(fill="x",padx=10,pady=5)
        self.vdjscript_entry = ttk.Entry(self.vdjscript_frame)
        self.vdjscript_entry.pack(side="left",fill="x",expand=True,padx=5,pady=5)
        self.send_button = ttk.Button(self.vdjscript_frame, text="Send", command=self._send_vdjscript)
        self.send_button.pack(side="right",padx=5,pady=5)

        self.browser_frame = ttk.LabelFrame(parent, text="Browser")
        self.browser_frame.pack(fill="both",padx=10,pady=5)
        self.browser_folders_button = ttk.Button(self.browser_frame, text="FOLDERS", command=lambda: self._send_command("browser_window 'folders'"))
        self.browser_folders_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_songs_button = ttk.Button(self.browser_frame, text="SONGS", command=lambda: self._send_command("browser_window 'songs'"))
        self.browser_songs_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_sideview_button = ttk.Button(self.browser_frame, text="SIDEVIEW", command=lambda: self._send_command("browser_window 'sideview'"))
        self.browser_sideview_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_sidelist_button = ttk.Button(self.browser_frame, text="SIDELIST", command=lambda: self._send_command("browser_window 'sidelist'"))
        self.browser_sidelist_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_remixes_button = ttk.Button(self.browser_frame, text="REMIXES", command=lambda: self._send_command("browser_window 'remixes'"))
        self.browser_remixes_button.pack(side="left", fill="both", padx=5, pady=5)
        self.browser_sampler_button = ttk.Button(self.browser_frame, text="SAMPLER", command=lambda: self._send_command("browser_window 'sampler'"))
        self.browser_sampler_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_automix_button = ttk.Button(self.browser_frame, text="AUTOMIX", command=lambda: self._send_command("browser_window 'automix'"))
        self.browser_automix_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_karaoke_button = ttk.Button(self.browser_frame, text="KARAOKE", command=lambda: self._send_command("browser_window 'karaoke'"))
        self.browser_karaoke_button.pack(side="left", fill="both", padx=5,pady=5)
        

        self.browser_open_button = ttk.Button(self.browser_frame, text="OPEN/CLOSE FOLDER", command=lambda: self._send_command("browser_open_folder"))
        self.browser_open_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_up_button = ttk.Button(self.browser_frame, text="UP", command=lambda: self._send_command("browser_scroll -1"))
        self.browser_up_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_down_button = ttk.Button(self.browser_frame, text="DOWN", command=lambda: self._send_command("browser_scroll +1"))
        self.browser_down_button.pack(side="left", fill="both", padx=5,pady=5)
        self.browser_load_button = ttk.Button(self.browser_frame, text="LOAD", command=lambda: self._send_command("load"))
        self.browser_load_button.pack(side="left", fill="both", padx=5,pady=5)
    #------------------------------------------------------------------------------------
    def _define_tab_songsdb(self, parent):
        songsDB = VirtualDJSongsDatabase()
        database_list = songsDB.get_local_database_list()
    #------------------------------------------------------------------------------------
    def _send_vdjscript(self):
        vdjscript = self.vdjscript_entry.get().strip()
        if not vdjscript:
            return
        if self.client is None:
            return
        if self._loop is None:
            return
        try:
            future = asyncio.run_coroutine_threadsafe(self.client.send_async(vdjscript), self._loop)
            future.add_done_callback(self._vdjscript_done)
        except Exception as e:
            pass
    #------------------------------------------------------------------------------------
    def _send_command(self, vdjscript: str):
        #vdjscript = "browser_scroll +1"
        if not vdjscript:
            return
        if self.client is None:
            return
        if self._loop is None:
            return
        try:
            future = asyncio.run_coroutine_threadsafe(self.client.send_async(vdjscript), self._loop)
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
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._client_main_get())
        finally:
            self._loop.close()
            self._loop = None
    #------------------------------------------------------------------------------------
    async def _client_main_get(self):
        async with VirtualDJClient() as client:
            self.client = client
            tasks = [asyncio.create_task(self._poll_data(client, name, config["getter"])) for name, config in self.frames_get.items()]
                   
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