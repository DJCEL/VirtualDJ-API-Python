#------------------------------------------------------------------------------------
# VirtualDJ settings
#------------------------------------------------------------------------------------
__version__ = '1.0.1'

import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .client_utils import VirtualDJUtils
from .client_config import VDJ_PROCESS_SETTINGS

#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsAudioConfigSetupAudio:
    soundcard: Optional[str] = None
    leftChannel: Optional[str] = None
    rightChannel: Optional[str] = None
    source: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsAudioConfigSetup:
    name: Optional[str] = None
    audio: Optional[list[VdjSettingsAudioConfigSetupAudio]] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsAudioConfig:
    current: Optional[str] = None
    setup: Optional[list[VdjSettingsAudioConfigSetup]] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsAutomation:
    autoBPMMatch: Optional[str] = None
    autoPitchLock: Optional[str] = None
    autoGain: Optional[str] = None
    autoKey: Optional[str] = None
    autoCue: Optional[str] = None
    smartPlay: Optional[str] = None
    smartPlayLimitPitchRange: Optional[str] = None
    smartCue: Optional[str] = None
    smartLoop: Optional[str] = None
    quantizeLoop: Optional[str] = None
    quantizeSetCue: Optional[str] = None
    globalQuantize: Optional[str] = None
    smartScratch: Optional[str] = None
    cueLoopAutoSync: Optional[str] = None
    resetPitchOnLoad: Optional[str] = None
    resetEqOnLoad: Optional[str] = None
    resetStemsOnLoad: Optional[str] = None
    resetFXOnLoad: Optional[str] = None
    resetKeyOnLoad: Optional[str] = None
    autoHeadphones: Optional[str] = None
    pflOnSelect: Optional[str] = None
    keyMatching: Optional[str] = None
    resetGainOnLoad: Optional[str] = None
    quantizeScratch: Optional[str] = None
    autoFluidGridSync: Optional[str] = None
    fluidSync: Optional[str] = None
    autoFluidLockOnSync: Optional[str] = None
    autoFluidLock: Optional[str] = None
    autoFluidLockKeepBpmOnExit: Optional[str] = None
    autoBpmStabilizer: Optional[str] = None
    autoBpmStabilizerKeepBpmOnExit: Optional[str] = None
    experimentalVariableBpm: Optional[str] = None
    autoBpmStabilizerMaxRange: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsControls:
    playMode: Optional[str] = None
    cueMode: Optional[str] = None
    hotcueMode: Optional[str] = None
    updateHotCueOnCueCombo: Optional[str] = None
    loopBackMode: Optional[str] = None
    loopAutoMove: Optional[str] = None
    loopDefault: Optional[str] = None
    loopRollDefault: Optional[str] = None
    beatjump: Optional[str] = None
    keepPlayingPastEnd: Optional[str] = None
    keepPlayStatusOnLoadSong: Optional[str] = None
    eqMode: Optional[str] = None
    eqModeDual: Optional[str] = None
    stemsBleedMuteVocal: Optional[str] = None
    stemsBleedMuteInstru: Optional[str] = None
    stemsBleedOnlyVocal: Optional[str] = None
    stemsBleedOnlyInstru: Optional[str] = None
    stemsSplitLeftRight: Optional[str] = None
    vinylMode: Optional[str] = None
    masterTempo: Optional[str] = None
    pitchRange: Optional[str] = None
    autoPitchRange: Optional[str] = None
    pitchResetSpeed: Optional[str] = None
    faderStart: Optional[str] = None
    faderStartStop: Optional[str] = None
    crossfaderCurve: Optional[str] = None
    crossfaderDisable: Optional[str] = None
    crossfaderCustom: Optional[str] = None
    crossfaderHamster: Optional[str] = None
    levelfaderHamster: Optional[str] = None
    effects: Optional[str] = None
    internalPluginLocations: Optional[str] = None
    masterEffects: Optional[str] = None
    mixFx: Optional[str] = None
    pluginBanks: Optional[str] = None
    padsPagesOrder: Optional[str] = None
    padsPagesHidden: Optional[str] = None
    sixteenPadsMode: Optional[str] = None
    padsPagesChanged: Optional[str] = None
    padsSkinIndependent: Optional[str] = None
    loopPadPage: Optional[str] = None
    autoSortCues: Optional[str] = None
    autoBpmTransitionLength: Optional[str] = None
    hotcueSavesLoop: Optional[str] = None
    defaultStemsEqMode: Optional[str] = None
    fxStyle: Optional[str] = None
    fxLists: Optional[str] = None
    fxListsCurrent: Optional[str] = None
    fxShowLegacyIgnore: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsSkins:
    skinWaveformType: Optional[str] = None
    skinOverviewType: Optional[str] = None
    skinWaveformScratchType: Optional[str] = None
    coloredWaveforms: Optional[str] = None
    waveUseFrequency: Optional[str] = None
    waveGrayOnKill: Optional[str] = None
    waveformCenter: Optional[str] = None
    skinPlayheadShadow: Optional[str] = None
    showGridLines: Optional[str] = None
    beatCounterRange: Optional[str] = None
    rhythmZoom: Optional[str] = None
    scratchZoomVertical: Optional[str] = None
    rhythmZoomSaved: Optional[str] = None
    scratchZoomSaved: Optional[str] = None
    touchScreenMode: Optional[str] = None
    multiTouchTwoFingerScroll: Optional[str] = None
    onScreenKeyboard: Optional[str] = None
    keyboardShowKeymapOverlay: Optional[str] = None
    keyboardKeymapOverlayOnStickyKeys: Optional[str] = None
    skinEmptyButtons: Optional[str] = None
    customButtons: Optional[str] = None
    skin3FxLayout: Optional[str] = None
    skin6FxLayout: Optional[str] = None
    vuMeter: Optional[str] = None
    clockDisplay: Optional[str] = None
    dateFormat: Optional[str] = None
    cueDisplay: Optional[str] = None
    savedLoopDisplay: Optional[str] = None
    displayTime: Optional[str] = None
    keyDisplay: Optional[str] = None
    cpuMeter: Optional[str] = None
    hideSongInfo: Optional[str] = None
    tooltip: Optional[str] = None
    tooltipDelay: Optional[str] = None
    showCoverForDragDrop: Optional[str] = None
    RPM: Optional[str] = None
    dialogsColorTheme: Optional[str] = None
    cleartype: Optional[str] = None
    maximized: Optional[str] = None
    skin: Optional[str] = None
    skinLoaded: Optional[str] = None
    skinPosition: Optional[str] = None
    skinWindows: Optional[str] = None
    skinPanels: Optional[str] = None
    skinTextzones: Optional[str] = None
    skinSplitState: Optional[str] = None
    skinRacks: Optional[str] = None
    skinFPS: Optional[str] = None
    showLyrics: Optional[str] = None
    getLyrics: Optional[str] = None
    lyricsCensoredWords: Optional[str] = None
    lyricsWaveformSize: Optional[str] = None
    showFluidGridLines: Optional[str] = None
    showFluidMarkers: Optional[str] = None
    showFluidMarkersSensitivity: Optional[str] = None
    showBpmChangesAbove: Optional[str] = None
    coloredWaveformsDynamicStems: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsAudio:
    audioAutoDetect: Optional[str] = None
    exclusiveAudioAccess: Optional[str] = None
    splitHeadphones: Optional[str] = None
    equalizerInHeadphones: Optional[str] = None
    headphonesGain: Optional[str] = None
    prelistenOutput: Optional[str] = None
    boothMicrophone: Optional[str] = None
    microphoneToMaster: Optional[str] = None
    metronomeVolume: Optional[str] = None
    gainSliderIncludesAutoGain: Optional[str] = None
    faderCurve: Optional[str] = None
    zeroDB: Optional[str] = None
    rampStartTime: Optional[str] = None
    rampStopTime: Optional[str] = None
    rampScratchTime: Optional[str] = None
    equalizerFrequencySpread: Optional[str] = None
    equalizerLowFrequency: Optional[str] = None
    equalizerMidFrequency: Optional[str] = None
    equalizerHighFrequency: Optional[str] = None
    filterDefaultResonance: Optional[str] = None
    fxProcessing: Optional[str] = None
    autoCue: Optional[str] = None
    autoBPMMatch: Optional[str] = None
    autoGain: Optional[str] = None
    autoKey: Optional[str] = None
    keyDetection: Optional[str] = None
    resetPitchOnLoad: Optional[str] = None
    resetEqOnLoad: Optional[str] = None
    resetFXOnLoad: Optional[str] = None
    resetKeyOnLoad: Optional[str] = None
    pitchRange: Optional[str] = None
    autoPitchLock: Optional[str] = None
    pitchResetSpeed: Optional[str] = None
    crossfaderCurve: Optional[str] = None
    crossfaderDisable: Optional[str] = None
    crossfaderCustom: Optional[str] = None
    crossfaderHamster: Optional[str] = None
    vinylMode: Optional[str] = None
    equalizerMode: Optional[str] = None
    effects: Optional[str] = None
    internalPluginLocations: Optional[str] = None
    masterEffects: Optional[str] = None
    mixFx: Optional[str] = None
    pluginBanks: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsVideo:
    useVideoSkin: Optional[str] = None
    videoSkin: Optional[str] = None
    showVideoSkinOnPreview: Optional[str] = None
    videoLogo: Optional[str] = None
    videoLogoImage: Optional[str] = None
    videoLogoSize: Optional[str] = None
    videoLogoPosition: Optional[str] = None
    videoCrossfader: Optional[str] = None
    videoVolumeLink: Optional[str] = None
    videoTransition: Optional[str] = None
    videoRandomTransition: Optional[str] = None
    videoFx: Optional[str] = None
    videoAudioOnlyVisualisation: Optional[str] = None
    letterBoxing: Optional[str] = None
    videoFPS: Optional[str] = None
    videoMicroFrames: Optional[str] = None
    videoResampleQuality: Optional[str] = None
    videoShaderQuality: Optional[str] = None
    videoUseDXVA: Optional[str] = None
    videoDriver: Optional[str] = None
    videoMaxMemory: Optional[str] = None
    videoForceFullscreen: Optional[str] = None
    videoDelay: Optional[str] = None
    videoWindowAlwaysOnTop: Optional[str] = None
    videoWindowPosition: Optional[str] = None
    videoCreateLinkOnDrop: Optional[str] = None
    startVideoOnLoad: Optional[str] = None
    showVideoskinWarning: Optional[str] = None
    videoTransitionList: Optional[str] = None
    lyricsCensoredWords: Optional[str] = None
    lyricsCensorAlsoAudio: Optional[str] = None
    lyricsCensorMatching: Optional[str] = None
    lyricsCensorVideo: Optional[str] = None
    lyricsCensorAudio: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsKaraoke:
    karaokeBackground: Optional[str] = None
    karaokeBackgroundMusic: Optional[str] = None
    karaokeBackgroundImage: Optional[str] = None
    karaokeBackgroundVolume: Optional[str] = None
    karaokeVideoSkin: Optional[str] = None
    karaokeSkipSilence: Optional[str] = None
    karaokeAutoRemovePlayed: Optional[str] = None
    karaokeDualDeck: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsControllers:
    mixerOrder: Optional[str] = None
    controllerTakeoverMode: Optional[str] = None
    controllerTakeoverModePitch: Optional[str] = None
    touchWheelBackspin: Optional[str] = None
    touchWheelForwardspin: Optional[str] = None
    touchWheelSpinThreshold: Optional[str] = None
    jogSensitivityScratch: Optional[str] = None
    jogSensitivityCue: Optional[str] = None
    jogSensitivityBend: Optional[str] = None
    jogVibrationProtection: Optional[str] = None
    motorWheelInstantPlay: Optional[str] = None
    motorWheelInstantStop: Optional[str] = None
    motorWheelSmoothPercent: Optional[str] = None
    motorWheelLockTime: Optional[str] = None
    controllerRefreshRate: Optional[str] = None
    controllerWaveFormZoom: Optional[str] = None
    disableBuiltInDefinitions: Optional[str] = None
    createMidiLog: Optional[str] = None
    midiLogLevel: Optional[str] = None
    controllersCustomization: Optional[str] = None
    djcButtons: Optional[str] = None
    controllerState: Optional[str] = None
    controllerMenu: Optional[str] = None
    showControllersSubDevices: Optional[str] = None
    iRemote: Optional[str] = None
    iRemoteList: Optional[str] = None
    iRemoteDefaultPort: Optional[str] = None
    vdjRemoteDevices: Optional[str] = None
    os2l: Optional[str] = None
    os2lDirectIp: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsTimecode:
    timecodeMode: Optional[str] = None
    timecodeType: Optional[str] = None
    timecodeLeadInTime: Optional[str] = None
    timecodeAntiSkip: Optional[str] = None
    timecodeNeedleDropSync: Optional[str] = None
    timecodePitchSliderIgnoreBend: Optional[str] = None
    timecodeSilence: Optional[str] = None
    timecodeCalibrationVolume: Optional[str] = None
    timecodeCalibrationPhase: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsSampler:
    samplerBank: Optional[str] = None
    samplerTriggerMode: Optional[str] = None
    samplerDefaultLoopMode: Optional[str] = None
    samplerForceNbColumns: Optional[str] = None
    samplerExportLossless: Optional[str] = None
    samplerDontSaveSource: Optional[str] = None
    samplerOutputToTriggerDeck: Optional[str] = None
    samplerRootFolder: Optional[str] = None
    samplerOutputDeck: Optional[str] = None
    samplerApplyEffectsOnDeckOutput: Optional[str] = None
    samplerVideoVolumeLink: Optional[str] = None
    autoSideview: Optional[str] = None
    samplerImageSize: Optional[str] = None
    samplerHeadphones: Optional[str] = None
    samplerShowEffects: Optional[str] = None
    samplerShowWaveform: Optional[str] = None
    samplerIndependentDeckBanks: Optional[str] = None
    samplerRecordStems: Optional[str] = None
    samplerSwapStems: Optional[str] = None
    samplerRecordLength: Optional[str] = None
    samplerAudioOutputMaster: Optional[str] = None
    samplerAudioOutputPads: Optional[str] = None
    samplerRecordStemsPads: Optional[str] = None
    samplerSpanAcrossDecks: Optional[str] = None
    samplerHideDefaultBanks: Optional[str] = None
    samplerHideLegacyBanks: Optional[str] = None
    shoutoutStyle: Optional[str] = None
    shoutoutVoice: Optional[str] = None
    shoutoutOver: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsBrowser:
    fileFormats: Optional[str] = None
    rootFoldersLocation: Optional[str] = None
    iTunesDatabaseFile: Optional[str] = None
    seratoFolder: Optional[str] = None
    traktorFolder: Optional[str] = None
    rekordboxFolder: Optional[str] = None
    importV7Databases: Optional[str] = None
    ignoreDrives: Optional[str] = None
    readOnly: Optional[str] = None
    searchInFolder: Optional[str] = None
    searchInDB: Optional[str] = None
    searchInContentUnlimited: Optional[str] = None
    searchInOnlineCatalogs: Optional[str] = None
    ContentUnlimitedWhenEmpty: Optional[str] = None
    OnlineCatalogsWhenEmpty: Optional[str] = None
    ContentUnlimitedCatalogs: Optional[str] = None
    OnlineCatalogs: Optional[str] = None
    onlineCatalogsContentPreference: Optional[str] = None
    showMusic: Optional[str] = None
    showVideo: Optional[str] = None
    showKaraoke: Optional[str] = None
    searchFields: Optional[str] = None
    browserColumns: Optional[str] = None
    browserSort: Optional[str] = None
    browserGridColumns: Optional[str] = None
    infoviewColumns: Optional[str] = None
    showHorizontalSideList: Optional[str] = None
    lockFolderOrder: Optional[str] = None
    keepSortOrder: Optional[str] = None
    rememberRecurse: Optional[str] = None
    browserSearchByFirstLetter: Optional[str] = None
    lastSelectedFolder: Optional[str] = None
    coverFlow: Optional[str] = None
    lastTrackListDate: Optional[str] = None
    historyDelay: Optional[str] = None
    writeHistory: Optional[str] = None
    prelistenVisible: Optional[str] = None
    prelistenStopOnChange: Optional[str] = None
    prelistenStartPos: Optional[str] = None
    autoSearchDB: Optional[str] = None
    showZipKaraoke: Optional[str] = None
    showM3UAsFolders: Optional[str] = None
    fontSize: Optional[str] = None
    browserPadding: Optional[str] = None
    browserBPMDigits: Optional[str] = None
    savePlaylist: Optional[str] = None
    saveUnplayedToSidelist: Optional[str] = None
    removePlayedFromSidelist: Optional[str] = None
    browserTextFit: Optional[str] = None
    tracklistFormat: Optional[str] = None
    shellIcons: Optional[str] = None
    sideviewShortcuts: Optional[str] = None
    sideViewShortcutsHidden: Optional[str] = None
    sideView: Optional[str] = None
    gridView: Optional[str] = None
    triggerPadView: Optional[str] = None
    sideViewReco: Optional[str] = None
    RemixesViewProvider: Optional[str] = None
    liveFeedbackProviders: Optional[str] = None
    logUnsuccessfulSearches: Optional[str] = None
    shazam: Optional[str] = None
    chartsCountry: Optional[str] = None
    filterFolderSplitGenreBySlash: Optional[str] = None
    browserAutoZoom: Optional[str] = None
    browserFontSizeButtons: Optional[str] = None
    browserDaysSongsAreNew: Optional[str] = None
    browserAutoOpenNewDrive: Optional[str] = None
    cdjExportStemsConfig: Optional[str] = None
    cdjExportStems: Optional[str] = None
    cdjExportCompatibility: Optional[str] = None
    cdjExportShowAllDrives: Optional[str] = None
    cdjExportAutoSyncCues: Optional[str] = None
    cdjExportCuesAsMemoryPoints: Optional[str] = None
    quickFilters: Optional[str] = None
    colorRules: Optional[str] = None
    user1FieldName: Optional[str] = None
    user2FieldName: Optional[str] = None
    favoriteGenres: Optional[str] = None
    favoriteTags1: Optional[str] = None
    favoriteTags2: Optional[str] = None
    getTagsAuto: Optional[str] = None
    setTagsAuto: Optional[str] = None
    coverDownload: Optional[str] = None
    getTitleFromTags: Optional[str] = None
    getRatingFromTags: Optional[str] = None
    getCommentFromTags: Optional[str] = None
    getCuesFromTags: Optional[str] = None
    getTagFromZip: Optional[str] = None
    getRemixWhenParsingFilenames: Optional[str] = None
    useKeyFromTag: Optional[str] = None
    keyDisplay: Optional[str] = None
    cleanTagsInDeckDisplay: Optional[str] = None
    onScreenKeyboard: Optional[str] = None
    multiTouchTwoFingerScroll: Optional[str] = None
    startOfDayHour: Optional[str] = None
    askTheDJMonitoring: Optional[str] = None
    askTheDJFrequency: Optional[str] = None
    askTheDJTwitterHashtag: Optional[str] = None
    showTipOfTheDay: Optional[str] = None
    tipOfTheDayAlreadySeen: Optional[str] = None
    limitedEdition: Optional[str] = None
    eventSchedule: Optional[str] = None
    browserShortcuts: Optional[str] = None
    browserShortcutsIcons: Optional[str] = None
    browserShortcutsCustomIconFile: Optional[str] = None
    browserShowSideviewInLists: Optional[str] = None
    disableHotplugForNewLists: Optional[str] = None
    browserShortcutsDefaultIcon: Optional[str] = None
    browserPreviousFoldersButton: Optional[str] = None
    browserAutoExportM3U: Optional[str] = None
    browserAutoExportM3UShowPlaylists: Optional[str] = None
    disableDuplicateForNewLists: Optional[str] = None
    browserShowLegacyM3UPlaylists: Optional[str] = None
    folderSearch: Optional[str] = None
    folderSearchOptions: Optional[str] = None
    folderSearchAdditionalListFolders: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsTags:
    getTagsAuto: Optional[str] = None
    setTagsAuto: Optional[str] = None
    coverDownload: Optional[str] = None
    getTitleFromTags: Optional[str] = None
    getRatingFromTags: Optional[str] = None
    getCommentFromTags: Optional[str] = None
    getCuesFromTags: Optional[str] = None
    getTagFromZip: Optional[str] = None
    getRemixWhenParsingFilenames: Optional[str] = None
    useKeyFromTag: Optional[str] = None
    cleanTagsInDeckDisplay: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsAutomix:
    automixMode: Optional[str] = None
    fadeLength: Optional[str] = None
    automixRepeat: Optional[str] = None
    automixAutoRemovePlayed: Optional[str] = None
    automixDualDeck: Optional[str] = None
    autoMixBeatMatchOnFade: Optional[str] = None
    automixSkipLength: Optional[str] = None
    automixMaxLength: Optional[str] = None
    automixDoubleClick: Optional[str] = None
    automixTempoMode: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsInternet:
    internetProxyURL: Optional[str] = None
    internetProxyPort: Optional[str] = None
    internetProxyUsername: Optional[str] = None
    internetProxyPassword: Optional[str] = None
    internetLogin: Optional[str] = None
    stayLoggedIn: Optional[str] = None
    dontLogin: Optional[str] = None
    oneTimeMsg: Optional[int] = None
    checkUpdates: Optional[str] = None
    earlyAccessUpdates: Optional[str] = None
    sendHistory: Optional[str] = None
    sendAnonymousStats: Optional[str] = None
    autoRefreshDRM: Optional[str] = None
    liveFeedback: Optional[str] = None
    liveFeedbackExperimental: Optional[str] = None
    usageStats: Optional[str] = None
    netsearchVideoQuality: Optional[str] = None
    netsearchAudioQuality: Optional[str] = None
    xiamiLogin: Optional[str] = None
    deezerAccessCode: Optional[str] = None
    deezerLoginStatus: Optional[str] = None
    soundcloudRefreshCode: Optional[str] = None
    soundcloudAccessCode2: Optional[str] = None
    tidalRefreshCode: Optional[str] = None
    iRemote: Optional[str] = None
    iRemoteList: Optional[str] = None
    iRemoteDefaultPort: Optional[int] = None
    vdjRemoteDevices: Optional[str] = None
    os2l: Optional[str] = None
    os2lDirectIp: Optional[str] = None
    askTheDJMonitoring: Optional[str] = None
    askTheDJFrequency: Optional[int] = None
    askTheDJTwitterHashtag: Optional[str] = None
    tidalAccessCode2: Optional[str] = None
    vdjRemoteIPs: Optional[str] = None
    soundcloudAccessCode: Optional[str] = None
    gdriveRefreshCode: Optional[str] = None
    dropboxRefreshCode: Optional[str] = None
    onedriveRefreshCode: Optional[str] = None
    icloudRefreshCode: Optional[str] = None
    cloudDriveEngine: Optional[str] = None
    cloudDriveFullAccess: Optional[str] = None
    cloudDriveSync: Optional[str] = None
    cloudDriveSynchronization: Optional[str] = None
    cloudDrivePauseSync: Optional[str] = None
    liveFeedbackUseBpm: Optional[str] = None
    os2lBeatOffset: Optional[float] = None
    oscPort: Optional[int] = None
    oscPortBack: Optional[int] = None
    oscInitSubscribe: Optional[str] = None
    geminiKey: Optional[str] = None
    spotifyAudioQuality: Optional[str] = None
    sprftk: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsRecord:
    recordFile: Optional[str] = None
    recordFormat: Optional[str] = None
    recordQuality: Optional[str] = None
    recordAutoStart: Optional[str] = None
    recordWaitForSound: Optional[str] = None
    recordOverwrite: Optional[str] = None
    recordAutoSplit: Optional[str] = None
    recordWriteCueFile: Optional[str] = None
    recordVideoResolution: Optional[str] = None
    recordVideoHardwareAcceleration: Optional[str] = None
    recordMicrophone: Optional[str] = None
    recordBitDepth: Optional[str] = None
    recordVideoFps: Optional[str] = None
    recordVideoCodec: Optional[str] = None
    recordPauseOnSilence: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsBroadcast:
    broadcastMode: Optional[str] = None
    broadcastVideoQuality: Optional[str] = None
    broadcastVideoQualityCustom: Optional[str] = None
    broadcastServers: Optional[str] = None
    broadcastServer: Optional[str] = None
    broadcastDirectFormat: Optional[str] = None
    broadcastDirectPort: Optional[str] = None
    broadcastDirectQuality: Optional[str] = None
    broadcastDirectMaxClients: Optional[str] = None
    broadcastDirectName: Optional[str] = None
    broadcastSongInfo: Optional[str] = None
    broadcastSongInfoFormat: Optional[str] = None
    podcastName: Optional[str] = None
    broadcastVideoProvider: Optional[str] = None
    broadcastVideoURL: Optional[str] = None
    broadcastVideoKey: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsOptions:
    language: Optional[str] = None
    loadSecurity: Optional[str] = None
    endOfSongWarning: Optional[int] = None
    autoDiscMarker: Optional[str] = None
    sandboxSplitHeadphones: Optional[str] = None
    sandboxPreviewOnly: Optional[str] = None
    VDJScriptGlobalVariables: Optional[str] = None
    crashGuard: Optional[str] = None
    crashReportLevel: Optional[int] = None
    poiEditorShowAll: Optional[str] = None
    poiEditorSnap: Optional[str] = None
    database: Optional[int] = None
    lastUsedBuild: Optional[int] = None
    lastUse: Optional[int] = None
    timestamp: Optional[int] = None
    nonColoredPoi: Optional[str] = None
    colorPicker: Optional[str] = None
    colorPickersystemCustom: Optional[str] = None
    lightShowProgram: Optional[str] = None
    settingPage: Optional[str] = None
    showTutorials: Optional[str] = None
    shopDemoMode: Optional[str] = None
    dontShowAgain: Optional[str] = None
    autoUpdateFailedCount: Optional[int] = None
    autoUpdateFailedSvn: Optional[int] = None
    autoUpdateFailedTime: Optional[int] = None
    vstFxFolder: Optional[str] = None
    showTipOfTheDay: Optional[str] = None
    tipOfTheDayAlreadySeen: Optional[str] = None
    skinStarterTip: Optional[int] = None
    limitedEdition: Optional[str] = None
    startOfDayHour: Optional[int] = None
    eventSchedule: Optional[str] = None
    automaticDatabaseBackupPeriod: Optional[str] = None
    databaseBackupLast: Optional[int] = None
    databaseBackupLocation: Optional[str] = None
    watchFolders: Optional[str] = None
    ABtesting: Optional[str] = None
    playMode: Optional[str] = None
    cueMode: Optional[str] = None
    hotcueMode: Optional[str] = None
    cueDisplay: Optional[str] = None
    savedLoopDisplay: Optional[str] = None
    smartPlay: Optional[str] = None
    smartPlayLimitPitchRange: Optional[str] = None
    smartLoop: Optional[str] = None
    smartCue: Optional[str] = None
    quantizeLoop: Optional[str] = None
    quantizeSetCue: Optional[str] = None
    globalQuantize: Optional[int] = None
    smartScratch: Optional[str] = None
    cueLoopAutoSync: Optional[str] = None
    masterTempo: Optional[str] = None
    updateHotCueOnCueCombo: Optional[str] = None
    autoSortCues: Optional[str] = None
    autoPitchRange: Optional[str] = None
    faderStart: Optional[str] = None
    faderStartStop: Optional[str] = None
    autoHeadphones: Optional[str] = None
    pflOnSelect: Optional[str] = None
    RPM: Optional[str] = None
    rhythmZoom: Optional[float] = None
    scratchZoomVertical: Optional[float] = None
    rhythmZoomSaved: Optional[float] = None
    scratchZoomSaved: Optional[float] = None
    loopBackMode: Optional[str] = None
    loopAutoMove: Optional[str] = None
    loopDefault: Optional[float] = None
    loopRollDefault: Optional[float] = None
    displayTime: Optional[str] = None
    hideSongInfo: Optional[str] = None
    tooltip: Optional[str] = None
    tooltipDelay: Optional[int] = None
    showCoverForDragDrop: Optional[str] = None
    showAdvancedConfig: Optional[str] = None
    padsPages: Optional[str] = None
    padsPagesHidden: Optional[str] = None
    sixteenPadsMode: Optional[str] = None
    padsPagesFavorite: Optional[str] = None
    loopPadPage: Optional[int] = None
    autoSyncSettingsOverride: Optional[str] = None
    forceLite: Optional[str] = None
    guid: Optional[str] = None
    variableBpmRange: Optional[str] = None
    variableBpmSensitivity: Optional[int] = None
    variableBpmDownbeatSensitivity: Optional[int] = None
    fluidAnalysis: Optional[str] = None
    fluidRange: Optional[str] = None
    fluidSensitivity: Optional[int] = None
    fluidDownbeatSensitivity: Optional[int] = None
    actionEditorDefaultView: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsPerformance:
    stemsRealtimeSeparation: Optional[str] = None
    stemsSavedStems: Optional[str] = None
    stemsGPU: Optional[str] = None
    stemsFix: Optional[str] = None
    stemsSavedFolder: Optional[str] = None
    stemsFixExtra: Optional[str] = None
    stemsSpeed: Optional[str] = None
    skinUseLowPowerGPU: Optional[str] = None
    skinFPS: Optional[int] = None
    sampleRate: Optional[int] = None
    latency: Optional[int] = None
    ultraLatency: Optional[str] = None
    maxPreloadLength: Optional[int] = None
    maxStemLength: Optional[int] = None
    pitchQuality: Optional[int] = None
    scratchFilterQuality: Optional[int] = None
    songLoadPriority: Optional[str] = None
    experimentalBeatAnalyzer: Optional[str] = None
    experimentalSkinEngine: Optional[str] = None
    experimentalWaveColors: Optional[str] = None
    safeVideoDecode: Optional[str] = None
    analyzeSongsOnView: Optional[str] = None
    keepBPMonAnalyzerUpdate: Optional[str] = None
    peakAudioCpu: Optional[float] = None
    peakAudioCpuStems: Optional[float] = None
    cpuMeter: Optional[str] = None
    clockDisplay: Optional[str] = None
    experimentalFluidAlgo: Optional[str] = None
    disableMidi2: Optional[str] = None
    experimentalFasterStartup: Optional[str] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettingsSkin:
    skinStarterTip: Optional[int] = None
#------------------------------------------------------------------------------------
@dataclass
class VdjSettings:
    audioConfig: Optional[VdjSettingsAudioConfig] = None
    automation: Optional[VdjSettingsAutomation] = None
    controls: Optional[VdjSettingsControls] = None
    skins: Optional[VdjSettingsSkins] = None
    audio: Optional[VdjSettingsAudio] = None
    video: Optional[VdjSettingsVideo] = None
    karaoke: Optional[VdjSettingsKaraoke] = None
    controllers: Optional[VdjSettingsControllers] = None
    timecode: Optional[VdjSettingsTimecode] = None
    sampler: Optional[VdjSettingsSampler] = None
    browser: Optional[VdjSettingsBrowser] = None
    tags: Optional[VdjSettingsTags] = None
    automix: Optional[VdjSettingsAutomix] = None
    internet: Optional[VdjSettingsInternet] = None
    record: Optional[VdjSettingsRecord] = None
    broadcast: Optional[VdjSettingsBroadcast] = None
    options: Optional[VdjSettingsOptions] = None
    performance: Optional[VdjSettingsPerformance] = None
    skin: Optional[VdjSettingsSkin] = None
#------------------------------------------------------------------------------------------------------------------------------------
class VirtualDJSettings():
    def __init__(self):
        self.vdj_utils = VirtualDJUtils()
        self.SETTINGS_FILENAME = VDJ_PROCESS_SETTINGS
    #------------------------------------------------------------------------------------
    def get_local_settings_path_list(self) -> list[Path]:
        settings_path_list : list[Path]= []
        vdj_home_list = self.vdj_utils.get_virtualdj_home_list()
        for vdj_home in vdj_home_list:
            settings_path = vdj_home / self.SETTINGS_FILENAME
            if settings_path.exists():
                settings_path_list.append(settings_path)

        settings_path_list_noduplicates = list(dict.fromkeys(settings_path_list))

        return settings_path_list_noduplicates
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_float(value: Optional[str]) -> Optional[float]:
        try:
            return float(value) if value is not None else None
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_int(value: Optional[str]) -> Optional[int]:
        try:
            return int(value) if value is not None else None
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    @staticmethod
    def _to_strftime(value: Optional[str]) -> Optional[str]:
        try:
            date_value = int(value) if value is not None else None
            if date_value is None:
                return None
            date_time = datetime.fromtimestamp(date_value)
            return date_time.strftime("%Y/%m/%d %H:%M:%S%z")
        except ValueError:
            return None
    #------------------------------------------------------------------------------------
    def read_local_xml_settings(self, settings_path: Path) -> VdjSettings:
        try:
            tree = ET.parse(settings_path)
        except ET.ParseError as exc:
            print(f"VirtualDJ settings reading {settings_path} => Invalid XML file")
            self.vdj_utils.SaveClientLog(f"VirtualDJ database reading {settings_path} => Invalid XML file")
            return None
        except OSError as exc:
            print(f"VirtualDJ settings reading {settings_path} => Cannot read the file")
            self.vdj_utils.SaveClientLog(f"VirtualDJ settings reading {settings_path} => Cannot read the file")
            return None

        root = tree.getroot()
        root_tag = root.tag
        root_attrib = root.attrib
        if root_tag != "settings":
            print(f"VirtualDJ settings reading {settings_path} => Not a VirtualDJ settings file")
            self.vdj_utils.SaveClientLog(f"VirtualDJ settings reading {settings_path} => Not a VirtualDJ settings file")
            return None


        settings = VdjSettings()
        settings.audioConfig = VdjSettingsAudioConfig()
        settings.audioConfig.setup = [VdjSettingsAudioConfigSetup()]
        settings.automation = VdjSettingsAutomation()
        settings.controls = VdjSettingsControls()
        settings.skins = VdjSettingsSkins()
        settings.audio = VdjSettingsAudio()
        settings.video = VdjSettingsVideo()
        settings.karaoke = VdjSettingsKaraoke()
        settings.controllers = VdjSettingsControllers()
        settings.timecode = VdjSettingsTimecode()
        settings.sampler = VdjSettingsSampler()
        settings.browser = VdjSettingsBrowser()
        settings.tags = VdjSettingsTags()
        settings.automix = VdjSettingsAutomix()
        settings.internet = VdjSettingsInternet()
        settings.record = VdjSettingsRecord()
        settings.broadcast = VdjSettingsBroadcast()
        settings.options = VdjSettingsOptions()
        settings.performance = VdjSettingsPerformance()
        settings.skin = VdjSettingsSkin()

        for child in root:
            child_tag = child.tag
            child_attrib = child.attrib
            child_text = child.text
            settings = self._parse_settings(settings, child, child_tag, child_attrib)

        return settings
    #------------------------------------------------------------------------------------
    def _parse_settings(self, settings, child: ET.Element, child_tag: str, child_attrib: str) -> VdjSettings:

        for subchild in child:
                subchild_tag = subchild.tag
                subchild_attrib = subchild.attrib
                subchild_text = subchild.text

                if child_tag == "audioConfig":
                    a = 0
                elif child_tag == "automation":
                    a = 0
                elif child_tag == "controls":
                    a = 0
                elif child_tag == "skins":
                    a = 0
                elif child_tag == "audio":
                    a = 0
                elif child_tag == "video":
                    a = 0
                elif child_tag == "karaoke":
                    a = 0
                elif child_tag == "controllers":
                    a = 0
                elif child_tag == "timecode":
                    a = 0
                elif child_tag == "sampler":
                    a = 0
                elif child_tag == "browser":
                    a = 0
                elif child_tag == "tags":
                    a = 0
                elif child_tag == "automix":
                    a = 0
                elif child_tag == "internet":
                    if subchild_tag == "checkUpdates":
                        settings.internet.checkUpdates = subchild_text
                elif child_tag == "record":
                    a = 0
                elif child_tag == "broadcast":
                    a = 0
                elif child_tag == "options":
                    if subchild_tag == "language":
                        settings.options.language = subchild_text
                    elif subchild_tag == "loadSecurity":
                        settings.options.loadSecurity = subchild_text
                    elif subchild_tag == "endOfSongWarning":
                        settings.options.endOfSongWarning = self._to_int(subchild_text)
                    elif subchild_tag == "autoDiscMarker":
                        settings.options.autoDiscMarker = subchild_text
                    elif subchild_tag == "sandboxSplitHeadphones":
                        settings.options.sandboxSplitHeadphones = subchild_text
                    elif subchild_tag == "sandboxPreviewOnly":
                        settings.options.sandboxPreviewOnly = subchild_text
                    elif subchild_tag == "VDJScriptGlobalVariables":
                        settings.options.VDJScriptGlobalVariables = subchild_text
                    elif subchild_tag == "crashGuard":
                        settings.options.crashGuard = subchild_text
                    elif subchild_tag == "crashReportLevel":
                        settings.options.crashReportLevel = self._to_int(subchild_text)
                    elif subchild_tag == "autoUpdateFailedCount":
                        settings.options.autoUpdateFailedCount = self._to_int(subchild_text)
                    elif subchild_tag == "autoUpdateFailedSvn":
                        settings.options.autoUpdateFailedSvn = subchild_text
                elif child_tag == "performance":
                    if subchild_tag == "stemsRealtimeSeparation":
                        settings.performance.stemsRealtimeSeparation = subchild_text
                elif child_tag == "skin":
                    if subchild_tag == "skinStarterTip":
                        settings.skin.skinStarterTip = self._to_int(subchild_text)
                else:
                    print(f"child_tag < {child_tag} > not defined")
                    self.vdj_utils.SaveClientLog(f"child_tag < {child_tag} > not defined")
            
        return settings