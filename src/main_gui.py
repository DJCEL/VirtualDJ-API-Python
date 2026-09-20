import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import dataclasses
import queue
import sys
import os
from pathlib import Path

__version__ = "1.0.9"

from virtualdj_client import (
    VirtualDJClient, 
    VdjDeckSong,
    VdjDeckEngine,
    VdjMixer, 
    VdjBrowserFolder, 
    VdjBrowserFile,
    VdjAutomix,
    VdjVideo,
    VirtualDJSongsDatabase,
)
from virtualdj_client import __version__ as __vdjclient_version__
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
        self.client = VirtualDJClient()
        self.songsDB = VirtualDJSongsDatabase()

        # Check if VirtualDJ is running
        client_running = self.client.is_app_running()
        print(f"VirtualDJ running => {client_running}")

        # Launch VirtualDJ if not running
        if client_running == False:
            print("Launching VirtualDJ...")
            client_launched = self.client.open_app()
            print(f"VirtualDJ launched => {client_launched}")
            client_running = self.client.is_app_running()
            print(f"VirtualDJ running => {client_running}")
            if (client_running == False):
                sys.exit()

        # Check the NetWork Control plugin
        client_connected = self.client.is_connected()
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
                            f"GUI version: {__version__}\n"
                            f"VirtualDJClient version: {__vdjclient_version__}\n\n"
                            "developped by DJCEL")
    #------------------------------------------------------------------------------------
    def _define_tab(self):
        """ we define 2 tabs """
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both",expand=True)
        self.send_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.send_tab,text="Send")
        self.get_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.get_tab,text="Get")
        self.songDB_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.songDB_tab,text="Songs database")

        """ SEND tab """
        self._define_tab_send(self.send_tab)

        """ GET tab """
        self._define_tab_get(self.get_tab)

        """ SONGSDB tab """
        self._define_tab_songsdb(self.songDB_tab)
    #------------------------------------------------------------------------------------
    def _define_tab_get(self, parent):
        frames_get_definition = [
            ("leftdecksong_frame", "Left Deck - Song", lambda client: client.get_DeckSong_async("left")),
            ("leftdeckengine_frame", "Left Deck - Engine", lambda client: client.get_DeckEngine_async("left")),
            ("rightdecksong_frame", "Right Deck - Song", lambda client: client.get_DeckSong_async("right")),
            ("rightdeckengine_frame", "Rigth Deck - Engine", lambda client: client.get_DeckEngine_async("right")),
            ("mixer_frame", "Mixer", lambda client: client.get_Mixer_async()),
            ("browserfolder_frame", "Browser - Folder", lambda client: client.get_BrowserFolder_async()),
            ("browserfile_frame", "Browser - File", lambda client: client.get_BrowserFile_async()),
            ("automix_frame", "Automix", lambda client: client.get_Automix_async()),
            ("video_frame", "Video", lambda client: client.get_Video_async()),
        ]

        self.get_frames = {}
        for row, (frame_name, frame_title, frame_function) in enumerate(frames_get_definition):
            frame = ttk.LabelFrame(parent, text=frame_title)
            text = tk.Text(frame, height=1, state='disabled', font=("Consolas",10))
            text.pack(fill="both", expand=True)
            frame.text_widget = text
            parent.grid_rowconfigure(row, weight=1,minsize=0)
            parent.grid_columnconfigure(0,weight=1)
            frame.grid(row=row,column=0,sticky="nsew",padx=10,pady=5)
            self.get_frames[frame_name] = {"frame": frame, "function": frame_function}
    #------------------------------------------------------------------------------------
    def _define_tab_send(self, parent):
        vdjscript_frame = ttk.LabelFrame(parent, text="VdjScript")
        vdjscript_frame.pack(fill="x",padx=10,pady=5)
        self.vdjscript_entry = ttk.Entry(vdjscript_frame)
        self.vdjscript_entry.pack(side="left",fill="x",expand=True,padx=5,pady=5)
        send_button = ttk.Button(vdjscript_frame, text="Send", command=self._send_vdjscript)
        send_button.pack(side="right",padx=5,pady=5)

        browser_frame = ttk.LabelFrame(parent, text="Browser")
        browser_frame.pack(fill="both", padx=10, pady=5)
        browser_folders_button = ttk.Button(browser_frame, text="FOLDERS", command=lambda: self._send_command("browser_window 'folders'"))
        browser_folders_button.grid(row=0, column=0, padx=5,pady=5)
        browser_songs_button = ttk.Button(browser_frame, text="SONGS", command=lambda: self._send_command("browser_window 'songs'"))
        browser_songs_button.grid(row=0, column=1, padx=5,pady=5)
        browser_sidelist_button = ttk.Button(browser_frame, text="SIDELIST", command=lambda: self._send_command("browser_window 'sidelist'"))
        browser_sidelist_button.grid(row=0, column=2, padx=5,pady=5)
        browser_remixes_button = ttk.Button(browser_frame, text="REMIXES", command=lambda: self._send_command("browser_window 'remixes'"))
        browser_remixes_button.grid(row=0, column=3, padx=5, pady=5)
        browser_sampler_button = ttk.Button(browser_frame, text="SAMPLER", command=lambda: self._send_command("browser_window 'sampler'"))
        browser_sampler_button.grid(row=0, column=4, padx=5,pady=5)
        browser_automix_button = ttk.Button(browser_frame, text="AUTOMIX", command=lambda: self._send_command("browser_window 'automix'"))
        browser_automix_button.grid(row=0, column=5, padx=5,pady=5)
        browser_karaoke_button = ttk.Button(browser_frame, text="KARAOKE", command=lambda: self._send_command("browser_window 'karaoke'"))
        browser_karaoke_button.grid(row=0, column=6, padx=5,pady=5)
        browser_up_button = ttk.Button(browser_frame, text="UP", command=lambda: self._send_command("browser_scroll -1"))
        browser_up_button.grid(row=1, column=0, padx=5,pady=5)
        browser_down_button = ttk.Button(browser_frame, text="DOWN", command=lambda: self._send_command("browser_scroll +1"))
        browser_down_button.grid(row=1, column=1, padx=5,pady=5)
        browser_open_button = ttk.Button(browser_frame, text="OPEN/CLOSE\nFOLDER", command=lambda: self._send_command("browser_open_folder"))
        browser_open_button.grid(row=1, column=2, padx=5,pady=5)
        browser_load_button = ttk.Button(browser_frame, text="LOAD", command=lambda: self._send_command("load"))
        browser_load_button.grid(row=1, column=3, padx=5,pady=5)
        browser_analyse_button = ttk.Button(browser_frame, text="ANALYSE", command=lambda: self._send_command("browsed_file_analyze"))
        browser_analyse_button.grid(row=1, column=4, padx=5,pady=5)
        browser_analysefluid_button = ttk.Button(browser_frame, text="FLUID\nANALYSE", command=lambda: self._send_command("browsed_file_analyze fluid"))
        browser_analysefluid_button.grid(row=1, column=5, padx=5,pady=5)
        browser_preparestems_button = ttk.Button(browser_frame, text="PREPARE\nSTEMS", command=lambda: self._send_command("browsed_file_prepare_stems"))
        browser_preparestems_button.grid(row=1, column=6, padx=5,pady=5)

      

        frame_title = "Left Deck"
        deck = "left"
        frame = ttk.LabelFrame(parent, text=frame_title)
        frame.pack(fill="both", padx=10, pady=5)
        select_button = ttk.Button(frame, text="SELECT", command=lambda: self._send_command(f"deck {deck} select"))
        select_button.grid(row=0, column=0, padx=5,pady=5)
        pfl_button = ttk.Button(frame, text="PFL", command=lambda: self._send_command(f"deck {deck} pfl"))
        pfl_button.grid(row=0, column=1, padx=5,pady=5)
        cue_button = ttk.Button(frame, text="CUE", command=lambda: self._send_command(f"deck {deck} cue_button"))
        cue_button.grid(row=0, column=2, padx=5,pady=5)
        play_button = ttk.Button(frame, text="PLAY", command=lambda: print(f"{deck.upper()} BUTTON") or self._send_command(f"deck {deck} play_button"))
        play_button.grid(row=0, column=3, padx=5,pady=5)
        sync_button = ttk.Button(frame, text="SYNC", command=lambda: self._send_command(f"deck {deck} sync"))
        sync_button.grid(row=0, column=4, padx=5,pady=5)
        stop_button = ttk.Button(frame, text="STOP", command=lambda: self._send_command(f"deck {deck} stop_button"))
        stop_button.grid(row=0, column=5, padx=5,pady=5)
        unload_button = ttk.Button(frame, text="UNLOAD", command=lambda: self._send_command(f"deck {deck} unload"))
        unload_button.grid(row=0, column=6, padx=5,pady=5)

        frame_title = "Right Deck"
        deck = "right"
        frame = ttk.LabelFrame(parent, text=frame_title)
        frame.pack(fill="both", padx=10, pady=5)
        select_button = ttk.Button(frame, text="SELECT", command=lambda: self._send_command(f"deck {deck} select"))
        select_button.grid(row=0, column=0, padx=5,pady=5)
        pfl_button = ttk.Button(frame, text="PFL", command=lambda: self._send_command(f"deck {deck} pfl"))
        pfl_button.grid(row=0, column=1, padx=5,pady=5)
        cue_button = ttk.Button(frame, text="CUE", command=lambda: self._send_command(f"deck {deck} cue_button"))
        cue_button.grid(row=0, column=2, padx=5,pady=5)
        play_button = ttk.Button(frame, text="PLAY", command=lambda: print(f"{deck.upper()} BUTTON") or self._send_command(f"deck {deck} play_button"))
        play_button.grid(row=0, column=3, padx=5,pady=5)
        sync_button = ttk.Button(frame, text="SYNC", command=lambda: self._send_command(f"deck {deck} sync"))
        sync_button.grid(row=0, column=4, padx=5,pady=5)
        stop_button = ttk.Button(frame, text="STOP", command=lambda: self._send_command(f"deck {deck} stop_button"))
        stop_button.grid(row=0, column=5, padx=5,pady=5)
        unload_button = ttk.Button(frame, text="UNLOAD", command=lambda: self._send_command(f"deck {deck} unload"))
        unload_button.grid(row=0, column=6, padx=5,pady=5)
           
            

    #------------------------------------------------------------------------------------
    def _define_tab_songsdb(self, parent):
        database_list = self.songsDB.get_local_database_list()
        database_list_full = []
        for db_path in database_list:
            database_name = os.path.basename(db_path)
            if (database_name == self.songsDB.XML_DATABASE_NAME):
                db_path_ext = str(db_path)
                database_list_full.append(db_path_ext)
            elif (database_name == self.songsDB.SQLITE_CACHE_DB):
                db_path_ext = str(db_path) + ' [' + self.songsDB.SQLITE_CACHE_DB_WAVEFORMS + ']'
                database_list_full.append(db_path_ext)
            elif (database_name == self.songsDB.SQLITE_EXTRA_DB):
                db_path_ext1 = str(db_path) + ' [' + self.songsDB.SQLITE_EXTRA_DB_LYRICS + ']'
                database_list_full.append(db_path_ext1)
                db_path_ext2 = str(db_path) + ' [' + self.songsDB.SQLITE_EXTRA_DB_RELATED_TRACKS + ']'
                database_list_full.append(db_path_ext2)
                db_path_ext3 = str(db_path) + ' [' + self.songsDB.SQLITE_EXTRA_DB_TRACK_DATA + ']'
                database_list_full.append(db_path_ext3)

        database_list_comboDB = ["--- Select a data source ---"]
        database_list_comboDB.extend(database_list_full)
        
        self.choixDB = tk.StringVar()
        comboDB = ttk.Combobox(parent, textvariable=self.choixDB, values=database_list_comboDB, width=100)
        comboDB.grid(row=0, column=0, sticky="nw", padx=10,pady=10)
        comboDB.current(0)
        comboDB.bind("<<ComboboxSelected>>", self.on_selectDB)

        self.frameDBcount = ttk.LabelFrame(parent, text="Number of items")
        self.frameDBcount.grid(row=1,column=0, sticky="nsew",padx=10,pady=5)
        text = tk.Text(self.frameDBcount, height=1, state='disabled', font=("Consolas",10))
        text.pack(fill="both", expand=True)
        self.frameDBcount.text_widget = text

        self.frameDB = ttk.LabelFrame(parent, text="First item")
        self.frameDB.grid(row=2,column=0, sticky="nsew",padx=10,pady=5)
        text = tk.Text(self.frameDB, height=1, state='disabled', font=("Consolas",10))
        text.pack(fill="both", expand=True)
        self.frameDB.text_widget = text
    #------------------------------------------------------------------------------------
    def on_selectDB(self, event):
        self._update_frame_text(self.frameDBcount,"")
        self._update_frame_text(self.frameDB,"")

        db_path_ext = self.choixDB.get()
        if db_path_ext.endswith("]"):
            part1, part2 = db_path_ext.split(" [", 1)
            db_path = Path(part1)
            table_name = part2.rstrip("]")
        else:
            db_path = Path(db_path_ext)
            table_name = ""

        database_name = os.path.basename(db_path)

        if (database_name == self.songsDB.XML_DATABASE_NAME):
            songs_database = self.songsDB.read_local_xml_database(db_path, filepath_only=False)
            n = len(songs_database)
            total_items = {"total_items": n}
            self._update_frame_text(self.frameDBcount, total_items)
            if n >= 1:
                item_1 = songs_database[0]
                self._update_frame_text(self.frameDB,item_1)
        elif (database_name == self.songsDB.SQLITE_CACHE_DB and table_name == self.songsDB.SQLITE_CACHE_DB_WAVEFORMS):   
            result_list = self.songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            total_items = {"total_items": n}
            self._update_frame_text(self.frameDBcount, total_items)
            if n >= 1:
                item_1 = result_list[0]
                self._update_frame_text(self.frameDB,item_1)
        elif (database_name == self.songsDB.SQLITE_EXTRA_DB and table_name == self.songsDB.SQLITE_EXTRA_DB_LYRICS):
            result_list = self.songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            total_items = {"total_items": n}
            self._update_frame_text(self.frameDBcount, total_items)
            if n >= 1:
                item_1 = result_list[0]
                self._update_frame_text(self.frameDB,item_1)
        elif (database_name == self.songsDB.SQLITE_EXTRA_DB and table_name == self.songsDB.SQLITE_EXTRA_DB_RELATED_TRACKS):
            result_list = self.songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            total_items = {"total_items": n}
            self._update_frame_text(self.frameDBcount, total_items)
            if n >= 1:
                item_1 = result_list[0]
                self._update_frame_text(self.frameDB,item_1)
        elif (database_name == self.songsDB.SQLITE_EXTRA_DB and table_name == self.songsDB.SQLITE_EXTRA_DB_TRACK_DATA):
            result_list = self.songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            total_items = {"total_items": n}
            self._update_frame_text(self.frameDBcount, total_items)
            if n >= 1:
                item_1 = result_list[0]
                self._update_frame_text(self.frameDB,item_1)
    #------------------------------------------------------------------------------------
    def _send_command(self, vdjscript: str):
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
    def _send_vdjscript(self):
        vdjscript = self.vdjscript_entry.get().strip()
        self._send_command(vdjscript)
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
            tasks = []
            for name, config in self.get_frames.items():
                getter = config["function"]
                task = asyncio.create_task(self._poll_data(client, name, getter))
                tasks.append(task)
                   
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
            
            end_time1 = asyncio.get_running_loop().time()
            elapsed1_ms = int((end_time1 - start_time) * 1000)

            #print(f"elapsed1_ms = {elapsed1_ms}")

            result_dict = {"name": name, "value": value}
            self._result_queue.put(result_dict)

            end_time2 = asyncio.get_running_loop().time()

            elapsed2_ms = int((end_time2 - start_time) * 1000)
            delay_ms = max(0, self.interval_refresh - elapsed2_ms)

            #print(f"elapsed2_ms = {elapsed2_ms}")
            #print(f"delay_ms = {delay_ms}")

            if delay_ms > 0:
                timeout = delay_ms / 1000
                try:
                    await asyncio.wait_for(self._stopping.wait(), timeout=timeout)
                except asyncio.TimeoutError:
                    pass
    #------------------------------------------------------------------------------------
    def refresh_ui(self):
        try:
            while True:
                result = self._result_queue.get_nowait()
                name = result["name"]
                data = result["value"]
                config = self.get_frames.get(name)
                if config is not None:
                    frame = config["frame"]
                    self._update_frame_text(frame, data)
                 
        except queue.Empty:
            pass

        if not self._stopping.is_set():
            self.after(self.interval_refresh, self.refresh_ui)
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
            elif isinstance(vdjdata, dict):
                data = vdjdata
            elif isinstance(vdjdata, str):
                data = vdjdata
            else:
                data = vars(vdjdata)

            widget.insert("end", data)

        widget.configure(state="disabled")
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()