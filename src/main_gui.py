import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import dataclasses
import queue
import sys
import os
from pathlib import Path
from functools import partial
import struct

__version__ = "1.0.11"

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
    VdjSong,
    VdjWaveform
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
        self.configure(bg="#1e1e1e")
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

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
        send_button = ttk.Button(vdjscript_frame, text="Send", command=self._send_vdjscript_input)
        send_button.pack(side="right",padx=5,pady=5)

        decks_frame_list = [
            ("Left Deck","left"),
            ("Right Deck","right")
            ]

        for row, (frame_title,deck) in enumerate(decks_frame_list):
            frame = ttk.LabelFrame(parent, text=frame_title)
            frame.pack(fill="x", padx=10, pady=5)
            select_button = ttk.Button(frame, text="SELECT", command=partial(self._send_command_deck,"select",deck))
            select_button.grid(row=0, column=0, padx=5,pady=5)
            pfl_button = ttk.Button(frame, text="PFL", command=partial(self._send_command_deck,"pfl",deck))
            pfl_button.grid(row=0, column=1, padx=5,pady=5)
            cue_button = ttk.Button(frame, text="CUE", command=partial(self._send_command_deck,"cue_button",deck))
            cue_button.grid(row=0, column=2, padx=5,pady=5)
            play_button = ttk.Button(frame, text="PLAY", command=partial(self._send_command_deck,"play_button",deck))
            play_button.grid(row=0, column=3, padx=5,pady=5)
            sync_button = ttk.Button(frame, text="SYNC", command=partial(self._send_command_deck,"sync",deck))
            sync_button.grid(row=0, column=4, padx=5,pady=5)
            stop_button = ttk.Button(frame, text="STOP", command=partial(self._send_command_deck,"stop_button",deck))
            stop_button.grid(row=0, column=5, padx=5,pady=5)
            unload_button = ttk.Button(frame, text="UNLOAD", command=partial(self._send_command_deck,"unload",deck))
            unload_button.grid(row=0, column=6, padx=5,pady=5)
            loop_button = ttk.Button(frame, text="LOOP", command=partial(self._send_command_deck,"loop",deck))
            loop_button.grid(row=0, column=7, padx=5,pady=5)
            loop_half_button = ttk.Button(frame, text="LOOP-", command=partial(self._send_command_deck,"loop_half",deck))
            loop_half_button.grid(row=0, column=8, padx=5,pady=5)
            loop_double_button = ttk.Button(frame, text="LOOP+", command=partial(self._send_command_deck,"loop_double",deck))
            loop_double_button.grid(row=0, column=9, padx=5,pady=5)

        
        mixer_frame = ttk.LabelFrame(parent, text="Mixer")
        mixer_frame.pack(fill="x", padx=10, pady=5)
        crossfader = ttk.Scale(mixer_frame,from_=0.0,to=1.0,orient="horizontal", command=partial(self._send_command,"crossfader"))
        crossfader.grid(row=0, column=0, padx=5,pady=5)

        browser_frame = ttk.LabelFrame(parent, text="Browser")
        browser_frame.pack(fill="x", padx=10, pady=5)
        browser_folders_button = ttk.Button(browser_frame, text="FOLDERS", command=partial(self._send_command,"browser_window 'folders'"))
        browser_folders_button.grid(row=0, column=0, padx=5,pady=5)
        browser_songs_button = ttk.Button(browser_frame, text="SONGS", command=partial(self._send_command,"browser_window 'songs'"))
        browser_songs_button.grid(row=0, column=1, padx=5,pady=5)
        browser_sidelist_button = ttk.Button(browser_frame, text="SIDELIST", command=partial(self._send_command,"browser_window 'sidelist'"))
        browser_sidelist_button.grid(row=0, column=2, padx=5,pady=5)
        browser_remixes_button = ttk.Button(browser_frame, text="REMIXES", command=partial(self._send_command,"browser_window 'remixes'"))
        browser_remixes_button.grid(row=0, column=3, padx=5, pady=5)
        browser_sampler_button = ttk.Button(browser_frame, text="SAMPLER", command=partial(self._send_command,"browser_window 'sampler'"))
        browser_sampler_button.grid(row=0, column=4, padx=5,pady=5)
        browser_automix_button = ttk.Button(browser_frame, text="AUTOMIX", command=partial(self._send_command,"browser_window 'automix'"))
        browser_automix_button.grid(row=0, column=5, padx=5,pady=5)
        browser_karaoke_button = ttk.Button(browser_frame, text="KARAOKE", command=partial(self._send_command,"browser_window 'karaoke'"))
        browser_karaoke_button.grid(row=0, column=6, padx=5,pady=5)
        browser_up_button = ttk.Button(browser_frame, text="UP", command=partial(self._send_command,"browser_scroll -1"))
        browser_up_button.grid(row=1, column=0, padx=5,pady=5)
        browser_down_button = ttk.Button(browser_frame, text="DOWN", command=partial(self._send_command,"browser_scroll +1"))
        browser_down_button.grid(row=1, column=1, padx=5,pady=5)
        browser_open_button = ttk.Button(browser_frame, text="OPEN/CLOSE\nFOLDER", command=partial(self._send_command,"browser_open_folder"))
        browser_open_button.grid(row=1, column=2, padx=5,pady=5)
        browser_load_button = ttk.Button(browser_frame, text="LOAD", command=partial(self._send_command,"load"))
        browser_load_button.grid(row=1, column=3, padx=5,pady=5)
        browser_analyse_button = ttk.Button(browser_frame, text="ANALYSE", command=partial(self._send_command,"browsed_file_analyze"))
        browser_analyse_button.grid(row=1, column=4, padx=5,pady=5)
        browser_analysefluid_button = ttk.Button(browser_frame, text="FLUID\nANALYSE", command=partial(self._send_command,"browsed_file_analyze fluid"))
        browser_analysefluid_button.grid(row=1, column=5, padx=5,pady=5)
        browser_preparestems_button = ttk.Button(browser_frame, text="PREPARE\nSTEMS", command=partial(self._send_command,"browsed_file_prepare_stems"))
        browser_preparestems_button.grid(row=1, column=6, padx=5,pady=5)

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

        self.waveform_frame = ttk.LabelFrame(parent, text="Waveform")
        self.waveform_frame.grid(row=3,column=0, sticky="nsew",padx=10,pady=5)
        self.waveform_viewer = WaveformViewer(self.waveform_frame)

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
                item_1 = songs_database[0] # type: VdjSong
                self._update_frame_text(self.frameDB,item_1)
        elif (database_name == self.songsDB.SQLITE_CACHE_DB and table_name == self.songsDB.SQLITE_CACHE_DB_WAVEFORMS):   
            result_list = self.songsDB.read_local_sqlite_database(db_path,database_name,table_name)
            n = len(result_list)
            total_items = {"total_items": n}
            self._update_frame_text(self.frameDBcount, total_items)
            if n >= 1:
                item_1 = result_list[0] # tyoe: VdjWaveform
                self._update_frame_text(self.frameDB,item_1)
                waveform = item_1["waveform"]
                valuesPerSecond = item_1["valuesPerSecond"]
                self.waveform_viewer.draw_waveform(waveform, valuesPerSecond)
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
    def _send_command(self, vdjverb: str, value: float = None):
        if not vdjverb:
            return
        if self.client is None:
            return
        if self._loop is None:
            return

        if value is None:
            vdjscript = f"{vdjverb}"
        else:
            vdjscript = f"{vdjverb} {value}"

        try:
            future = asyncio.run_coroutine_threadsafe(self.client.send_async(vdjscript), self._loop)
            future.add_done_callback(self._vdjscript_done)
        except Exception as e:
            pass
    #------------------------------------------------------------------------------------
    def _send_command_deck(self, vdjverb: str, deck:str, value: float = None):
        if not vdjverb:
            return
        if not deck:
            return
        if self.client is None:
            return
        if self._loop is None:
            return

        if value is None:
            vdjscript = f"deck {deck} {vdjverb}"
        else:
            vdjscript = f"deck {deck} {vdjverb} {value}"

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
    def _send_vdjscript_input(self):
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
            elif isinstance(vdjdata, (bytes, bytearray)):
                data = vdjdata
            else:
                data = vars(vdjdata)

            widget.insert("end", data)

        widget.configure(state="disabled")
#------------------------------------------------------------------------------------------------------------------------------------
class WaveformViewer(ttk.Frame):
    def __init__(self, parent_frame):
        super().__init__(parent_frame)
        self.parent_frame = parent_frame
        self.bar_width = 4
        self.gap = 1
        self.max_height = 260
        self._build_ui(parent_frame)

        # A distinct color per band (v0, v1, v2, ...). Extend if you have more bands.
        self.BAND_COLORS = [
            "#4FC3F7",  # light blue
            "#81C784",  # green
            "#FFD54F",  # yellow
            "#FF8A65",  # orange
            "#BA68C8",  # purple
            "#4DB6AC",  # teal
            "#F06292",  # pink
            "#A1887F",  # brown
            "#90A4AE",  # gray-blue
        ]
        self.CENTER_LINE_COLOR = "#3a3a3a"
        self.RULER_COLOR = "#5a5a5a"
        self.RULER_TEXT_COLOR = "#9a9a9a"
        self.PLAYHEAD_COLOR = "#ffffff"
        self.RULER_HEIGHT = 24  # px reserved at the bottom for the time ruler


    def draw_waveform(self, waveform, valuesPerSecond): 
        samples = self._decode_vdj_waveform(waveform)
        self.keys = sorted(samples[0].keys(), key=lambda k: int("".join(ch for ch in k if ch.isdigit()) or 0),)
        self.duration = len(samples) / valuesPerSecond
        self.values_per_second = valuesPerSecond
        self.seconds_per_sample = 1 / valuesPerSecond

        # Normalize against the global max across all bands/samples so bar heights are comparable sample-to-sample.
        self.global_max = max((v for s in samples for v in s.values() if isinstance(v, (int, float))), default=1,) or 1

        self.toobar_text_data.set(f"valuesPerSecond={self.values_per_second} / Duration={self.duration} seconds / {len(samples)} samples")
        self._draw(samples)

    def _decode_vdj_waveform(self, waveformDB):
        waveform = waveformDB.hex()
        if isinstance(waveform, str):
            waveform = waveform.strip()

            # Remove optional 0x prefix
            if waveform.startswith("0x"):
                waveform = waveform[2:]

            data = bytes.fromhex(waveform)

        elif isinstance(waveform, bytes):
            data = waveform

        elif isinstance(waveform, bytearray):
            data = bytes(waveform)

        else:
            raise TypeError(f"Unsupported waveform type: {type(waveform).__name__}")

        if len(data) % 28:
            raise ValueError(f"Invalid waveform size: {len(data)} bytes")

        samples = []

        for offset in range(0, len(data), 28):
            v0, v1, v2, v3, v4, v5, v6 = struct.unpack_from("<7I", data, offset)

            samples.append({
                "v0": v0 / 2**24,
                "v1": v1 / 2**24,
                "v2": v2 / 2**24,
                "v3": v3 / 2**24,
                "v4": v4 / 2**24,
                "v5": v5 / 2**24,
                "v6": v6,
            })

        return samples

    def _build_ui(self, parent_frame):
        toolbar = ttk.Frame(parent_frame)
        toolbar.pack(side="top", fill="x", padx=6, pady=6)
       
        self.toobar_text_data = tk.StringVar(value="")
        toobar_text = ttk.Label(toolbar, textvariable=self.toobar_text_data)
        toobar_text.pack(side="left")

        canvas_frame = ttk.Frame(parent_frame)
        canvas_frame.pack(side="top", fill="x", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#1e1e1e", highlightthickness=0)
        hscroll = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=hscroll.set)
        self.canvas.pack(side="top", fill="x", expand=True)
        hscroll.pack(side="bottom", fill="x")

        # Mouse wheel horizontal scroll (Shift+wheel on most platforms, plain wheel on trackpads)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", lambda e: self.canvas.xview_scroll(-3, "units"))
        self.canvas.bind("<Button-5>", lambda e: self.canvas.xview_scroll(3, "units"))
        self.pack(fill="both", expand=True)

    def _on_mousewheel(self, event):
        delta = -1 if event.delta > 0 else 1
        self.canvas.xview_scroll(delta * 3, "units")

    def _draw(self, samples):
        self.canvas.delete("all")
        n = len(samples)
        step = self.bar_width + self.gap
        total_width = max(n * step, 1)
        ruler_h = self.RULER_HEIGHT if self.seconds_per_sample is not None else 0
        self.canvas.configure(scrollregion=(0, 0, total_width, self.max_height + 40 + ruler_h))

        center_y = (self.max_height // 2) + 20
        self.canvas.create_line(0, center_y, total_width, center_y, fill=self.CENTER_LINE_COLOR)

        self._draw_curve(step, center_y, samples)

        if self.seconds_per_sample is not None:
            self._draw_ruler(step, total_width, self.max_height + 40)

    def _draw_curve(self, step, center_y, samples):
        """Each sample = one x position, bands stacked as mirrored segments."""
        half_h = (self.max_height // 2)
        n_bands = len(self.keys)
        for i, sample in enumerate(samples):
            x0 = i * step
            x1 = x0 + self.bar_width
            # allocate height per band proportional to its share of a
            # per-sample max, scaled against the global max
            values = [max(0.0, float(sample.get(k, 0) or 0)) for k in self.keys]
            total = sum(values) or 1
            sample_scale = min(sum(values) / (n_bands * self.global_max), 1.0)
            y_top = center_y
            for v, color in zip(values, self.BAND_COLORS):
                if v <= 0:
                    continue
                seg_h = (v / total) * sample_scale * half_h
                y_new_top = y_top - seg_h
                self.canvas.create_rectangle(
                    x0, y_new_top, x1, y_top, fill=color, width=0
                )
                y_top = y_new_top
            # mirror below the center line for a classic waveform silhouette
            y_bot = center_y
            for v, color in zip(values, self.BAND_COLORS):
                if v <= 0:
                    continue
                seg_h = (v / total) * sample_scale * half_h
                y_new_bot = y_bot + seg_h
                self.canvas.create_rectangle(
                    x0, y_bot, x1, y_new_bot, fill=color, width=0, stipple="gray50"
                )
                y_bot = y_new_bot

    def _draw_ruler(self, step, total_width, y):
        """Draw a time axis (mm:ss ticks) below the waveform."""
        self.canvas.create_line(0, y, total_width, y, fill=self.RULER_COLOR)

        # Pick a tick spacing that yields a reasonable number of on-screen
        # labels regardless of zoom level (bar width / sample count).
        px_per_second = step / self.seconds_per_sample if self.seconds_per_sample else 1
        target_seconds_per_tick = 80 / max(px_per_second, 0.001)  # ~80px between labels
        tick_seconds = self._nice_tick_seconds(target_seconds_per_tick)

        t = 0.0
        while t <= self.duration:
            x = (t / self.seconds_per_sample) * step
            self.canvas.create_line(x, y, x, y + 5, fill=self.RULER_COLOR)
            self.canvas.create_text(
                x + 2, y + 7, text=self.format_time(t), fill=self.RULER_TEXT_COLOR,
                anchor="nw", font=("TkDefaultFont", 8)
            )
            t += tick_seconds

    def format_time(self,seconds):
        seconds = max(0, seconds)
        m = int(seconds // 60)
        s = seconds - m * 60
        if seconds < 60:
            return f"{s:.1f}s"
        return f"{m}:{s:04.1f}"


    def _nice_tick_seconds(self,target):
        """Round `target` seconds up to a 'nice' tick interval (1,2,5,10,15,30,60...)."""
        nice_steps = [0.1, 0.2, 0.5, 1, 2, 5, 10, 15, 30, 60, 120, 300, 600]
        for step in nice_steps:
            if step >= target:
                return step
        return nice_steps[-1]
#------------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = VirtualDJMonitor()
    app.mainloop()