# -*- coding: UTF-8 -*-
# Name: choose_topic.py
# Porpose: shows the topics available in the program
# Compatibility: Python3, wxPython Phoenix
# Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2021 Gianluca Pernigotto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: Jan.28.2021
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
import wx
from videomass3.vdms_utils.get_bmpfromsvg import get_bmp
import wx.lib.agw.hyperlink as hpl
from videomass3.vdms_io import IO_tools
from videomass3.vdms_sys.msg_info import current_release
import os
import sys


def ydl_latest():
    """
    check for new releases of youtube-dl from
    """
    url = ("https://api.github.com/repos/ytdl-org/youtube-dl"
           "/releases/latest")
    latest = IO_tools.get_github_releases(url, "tag_name")

    if latest[0] in ['request error:', 'response error:']:
        wx.MessageBox("%s %s" % (latest[0], latest[1]),
                      "%s" % latest[0], wx.ICON_ERROR, self)
        return None

    return latest
# -----------------------------------------------------------------#


class Choose_Topic(wx.Panel):
    """
    Helps to choose a topic.
    """
    def __init__(self, parent, OS, videoconv_icn, youtube_icn, prstmng_icn):
        """
        This is a home panel shown when start Videomass to choose the
        appropriate contextual panel.
        """
        self.parent = parent
        self.oS = OS
        version = current_release()

        get = wx.GetApp()  # get videomass wx.App attribute
        self.PYLIB_YDL = get.pylibYdl  # None if used else 'string error'
        self.EXEC_YDL = get.execYdl  # /path/youtube-dl if used else False
        self.YDL_PREF = get.YDL_pref

        PRST_MNG = _('  Presets Manager - Create, edit and use quickly your '
                     'favorite\n  FFmpeg presets and profiles with full '
                     'formats support and codecs. ')

        AV_CONV = _('  A set of useful tools for audio and video conversions.'
                    '\n  Save your profiles and reuse them with Presets '
                    'Manager. ')

        YOUTUBE_DL = _('  Easily download videos and audio in different '
                       'formats\n  and quality from YouTube, Facebook and '
                       'more sites. ')

        if 'wx.svg' in sys.modules:  # available only in wx version 4.1 to up
            bmpAVconv = get_bmp(videoconv_icn, ((48, 48)))
            bmpPrstmng = get_bmp(prstmng_icn, ((48, 48)))
            bmpYdl = get_bmp(youtube_icn, ((48, 48)))
        else:
            bmpAVconv = wx.Bitmap(videoconv_icn, wx.BITMAP_TYPE_ANY)
            bmpPrstmng = wx.Bitmap(prstmng_icn, wx.BITMAP_TYPE_ANY)
            bmpYdl = wx.Bitmap(youtube_icn, wx.BITMAP_TYPE_ANY)

        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)

        welcome = wx.StaticText(self, wx.ID_ANY, (_("Welcome to Videomass")))
        version = wx.StaticText(self, wx.ID_ANY, (_('Version {}'
                                                    ).format(version[2])))
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_buttons = wx.FlexGridSizer(5, 0, 20, 20)
        grid_base = wx.GridSizer(1, 1, 0, 0)

        if self.oS == 'Windows':
            style = wx.BU_LEFT | wx.BORDER_NONE
        else:
            style = wx.BU_LEFT

        self.presets_mng = wx.Button(self, wx.ID_ANY, PRST_MNG, size=(-1, -1),
                                     style=style
                                     )
        self.presets_mng.SetBitmap(bmpPrstmng, wx.LEFT)
        self.avconv = wx.Button(self, wx.ID_ANY, AV_CONV,
                                size=(-1, -1), style=style
                                )
        self.avconv.SetBitmap(bmpAVconv, wx.LEFT)
        self.youtube = wx.Button(self, wx.ID_ANY, YOUTUBE_DL,
                                 size=(-1, -1), style=style
                                 )
        self.youtube.SetBitmap(bmpYdl, wx.LEFT)

        grid_buttons.AddMany([(welcome, 0, wx.ALIGN_CENTER_VERTICAL |
                               wx.ALIGN_CENTER_HORIZONTAL, 0),
                              (version, 0, wx.BOTTOM |
                               wx.ALIGN_CENTER_VERTICAL |
                               wx.ALIGN_CENTER_HORIZONTAL, 20),
                              (self.presets_mng, 0, wx.EXPAND, 5),
                              (self.avconv, 0, wx.EXPAND, 5),
                              (self.youtube, 0, wx.EXPAND, 5),
                              ])
        grid_base.Add(grid_buttons, 0, wx.ALIGN_CENTER_VERTICAL |
                      wx.ALIGN_CENTER_HORIZONTAL, 5
                      )
        sizer_base.Add(grid_base, 1, wx.EXPAND, 5)
        sizer_hpl = wx.BoxSizer(wx.HORIZONTAL)
        sizer_base.Add(sizer_hpl, 0, wx.ALL |
                       wx.ALIGN_CENTER_VERTICAL |
                       wx.ALIGN_CENTER_HORIZONTAL, 15
                       )
        sizer_trad = wx.BoxSizer(wx.HORIZONTAL)
        sizer_base.Add(sizer_trad, 0, wx.ALL |
                       wx.ALIGN_CENTER_VERTICAL |
                       wx.ALIGN_CENTER_HORIZONTAL, 15
                       )

        txt_trad = wx.StaticText(self,
                                 label=_('Videomass would need volunteer '
                                         'translators. If you are interested '
                                         'you could take a look at the '))
        lnk = ("https://github.com/jeanslack/Videomass/blob/"
               "master/docs/localization_guidelines.md")
        link_trad = hpl.HyperLinkCtrl(self, -1, _("Localization guidelines"),
                                      URL=lnk)
        sizer_trad.Add(txt_trad)
        sizer_trad.Add(link_trad)
        self.SetSizerAndFit(sizer_base)

        if self.oS == 'Darwin':
            welcome.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
            version.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))
        else:
            welcome.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
            version.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.LIGHT))
        '''
        if get.THEME == 'Videomass-Colours':
            self.SetBackgroundColour('#85d7a8')  # green marine medium
            welcome.SetForegroundColour('#ff3779')  # fuxia
            version.SetForegroundColour('#ff3779')  # fuxia
            txt_trad.SetForegroundColour('#ff3779')  # fuxia

        elif get.THEME == 'Breeze-Blues':
            self.SetBackgroundColour('#d8bfd8')  # cardo
            welcome.SetForegroundColour('#171b12')  # black
            version.SetForegroundColour('#171b12')  # black
            txt_trad.SetForegroundColour('#171b12')  # black

        elif get.THEME in ('Breeze-Dark', 'Videomass-Dark'):
            self.SetBackgroundColour('#00121f')  # dark blue
            welcome.SetForegroundColour('#b0e0e6')  # light
            version.SetForegroundColour('#b0e0e6')  # light
            txt_trad.SetForegroundColour('#b0e0e6')  # light
        else:
            self.SetBackgroundColour('#add8e6')  # light azure
            welcome.SetForegroundColour('#171b12')  # black
            version.SetForegroundColour('#171b12')  # black
            txt_trad.SetForegroundColour('#171b12')  # black
        '''

        self.Bind(wx.EVT_BUTTON, self.on_Video, self.avconv)
        self.Bind(wx.EVT_BUTTON, self.on_Prst_mng, self.presets_mng)
        self.Bind(wx.EVT_BUTTON, self.on_YoutubeDL, self.youtube)
    # ------------------------------------------------------------------#

    def on_Prst_mng(self, event):
        """
        Open drag N drop interface to switch on Presets Manager panel
        """
        self.parent.switch_file_import(self, 'Presets Manager')
    # ------------------------------------------------------------------#

    def on_Video(self, event):
        """
        Open drag N drop interface to switch on AVconversions panel
        """
        self.parent.switch_file_import(self, 'Audio/Video Conversions')
    # ------------------------------------------------------------------#

    def on_YoutubeDL(self, event):
        """
        Check the existence of youtube-dl based on the set attributes
        of the bootstrap, then open the text interface, otherwise it
        requires installation.

        """
        if self.oS == 'Windows':
            msg_windows = (_(
                        '- Requires: Microsoft Visual C++ 2010 '
                        'Redistributable Package (x86)\n\nfor major '
                        'information visit: <http://ytdl-org.github.io'
                        '/youtube-dl/download.html>\n\n'
                        ))
        else:
            msg_windows = ''

        msg_required = (_(
                 'To download videos from YouTube.com and other video sites, '
                 'you need an updated version of youtube-dl.\n\n'
                 '{}'
                 '...Do you want to download youtube-dl locally now?'
                 )).format(msg_windows)

        msg_ready = (_(
                    'Successful! \n\n'
                    'youtube-dl is very often updated, make sure you always '
                    'use the latest version available: menu bar > Tools > '
                    'Update youtube-dl.'
                    ))
        if self.YDL_PREF == 'disabled':
            wx.MessageBox(_("youtube-dl is disabled. Check your preferences."),
                          "Videomass", wx.ICON_INFORMATION, self)
            return

        elif self.YDL_PREF == 'system':
            if self.PYLIB_YDL is None:
                self.parent.switch_text_import(self, 'Youtube Downloader')
                return
            else:
                wx.MessageBox(_("ERROR: {}\n\nyoutube-dl is not installed, "
                                "use your package manager to install "
                                "it.").format(self.PYLIB_YDL),
                              "Videomass", wx.ICON_ERROR, self)
                return

        elif self.YDL_PREF == 'local':
            if os.path.isfile(self.EXEC_YDL):
                self.parent.switch_text_import(self, 'Youtube Downloader')
                return
            else:
                if wx.MessageBox(msg_required, _("Please confirm"),
                                 wx.ICON_QUESTION |
                                 wx.YES_NO, self) == wx.NO:
                    return

                latest = ydl_latest()
                if not latest:
                    return
                else:
                    upgrade = IO_tools.youtubedl_upgrade(latest[0],
                                                         self.EXEC_YDL)
                if upgrade[1]:  # failed
                    wx.MessageBox("%s" % (upgrade[1]),
                                  "Videomass", wx.ICON_ERROR, self)
                    return
                else:
                    wx.MessageBox(msg_ready, "Videomass", wx.ICON_INFORMATION,
                                  self)
                    self.parent.ydlused.Enable(True)
                    self.parent.ydlupdate.Enable(True)
                    return
                return
