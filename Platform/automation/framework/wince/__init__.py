"""WinCE / GFTS device helpers (Translink ETM and siblings).

The Windows-Embedded-Compact devices run the GFTS / .NET Compact Framework
stack and expose **no command shell** — the only transport is a Rebex SFTP
file server. So, unlike the Android helpers which drive `content query` over
`adb shell`, these helpers read device state by *pulling SD-card files* and
parsing them. See `framework/wince/events.py` and `framework/wince/dm_parameters.py`.
"""
