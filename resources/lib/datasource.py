# -*- coding: utf-8 -*-
# 
# Massengeschmack XBMC add-on
# Copyright (C) 2013 by Janek Bevendorff
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import xbmcgui
import urllib
from globalvars import *
import resources.lib
from resources.lib.listing import *

class DataSource:
    def getListItems(self):
        """
        Generate a list of ListeItem objects for the current data source.
        """
        return [
            # Fernsehkritik-TV
            ListItem(
                ADDON.getLocalizedString(30200),
                resources.lib.assembleListURL('fktv'),
                ADDON_BASE_PATH + '/resources/assets/banner-fktv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30200),
                    'Director':'Holger Kreymeier, Nils Beckmann, Daniel Gusy',
                    'Genre': ADDON.getLocalizedString(30201),
                    'Premiered':'07.04.2007',
                    'Country': ADDON.getLocalizedString(30202),
                    'Plot': ADDON.getLocalizedString(30203)
                }
            ),
            # Pantoffel-TV
            ListItem(
                ADDON.getLocalizedString(30210),
                resources.lib.assembleListURL('ptv'),
                ADDON_BASE_PATH + '/resources/assets/banner-ptv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-ptv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30210),
                    'Director':'Holger Kreymeier, Jenny von Gagern, Steven Gräwe, Michael Stock',
                    'Genre': ADDON.getLocalizedString(30211),
                    'Premiered':'17.06.2013',
                    'Country': ADDON.getLocalizedString(30212),
                    'Plot': ADDON.getLocalizedString(30213)
                }
            ),
            # Pressesch(l)au
            ListItem(
                ADDON.getLocalizedString(30220),
                resources.lib.assembleListURL('ps'),
                ADDON_BASE_PATH + '/resources/assets/banner-ps.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-ps.jpg',
                {
                    'Title': ADDON.getLocalizedString(30220),
                    'Director':'Holger Kreymeier, Steven Gräwe, Daniel Gusy',
                    'Genre': ADDON.getLocalizedString(30221),
                    'Premiered':'01.08.2013',
                    'Country': ADDON.getLocalizedString(30222),
                    'Plot': ADDON.getLocalizedString(30223)
                }
            ),
            # Massengeschmack-TV
            ListItem(
                ADDON.getLocalizedString(30230),
                resources.lib.assembleListURL('mgtv'),
                ADDON_BASE_PATH + '/resources/assets/banner-mgtv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-mgtv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30230),
                    'Director':'Holger Kreymeier',
                    'Genre': ADDON.getLocalizedString(30231),
                    'Premiered':'05.08.2013',
                    'Country': ADDON.getLocalizedString(30232),
                    'Plot': ADDON.getLocalizedString(30233)
                }
            ),
        ]
    
    def getContentMode(self):
        """
        Get the view mode for the listing content.
        
        Content mode is usually either 'tvshows' or 'episodes', but can
        also be any other valid value for xbmcplugin.setContent().
        
        @return content mode
        """
        return 'tvshows'


class FKTVDataSource(DataSource):
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'best'
            else:
                quality = 'mobile'
        
        submodule = None
        if 'submodule' in ADDON_ARGS and ADDON_ARGS['submodule'] in self.__urls[quality]:
            submodule = ADDON_ARGS['submodule']
        
        if None == submodule:
            return self.__getBaseList()
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality][submodule], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30201),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        if 'submodule' in ADDON_ARGS:
            return 'episodes'
        
        return 'tvshows'
    
    def __getThumbnailURL(self, guid):
        basePath1 = 'http://fernsehkritik.tv/images/magazin/'
        basePath2 = 'http://massengeschmack.tv/img/mag/'
        
        if 'fktv' == guid[0:4]:
            return basePath1 + 'folge' + guid[4:] + '@2x.jpg'
        if 'postecke' == guid[0:8]:
            return basePath2 + 'postecke.jpg'
        if 'interview-' == guid[0:10]:
            if 'remote' == guid[10:]:
                # ugly fix for single episode
                return basePath2 + 'remotecontrol.jpg'
            
            return basePath2 + guid[10:] + '.jpg'
        
        return basePath2 + guid + '.jpg'
    
    def __getBaseList(self):
        return [
            # All
            ListItem(
                ADDON.getLocalizedString(30300),
                resources.lib.assembleListURL('fktv', 'all'),
                ADDON_BASE_PATH + '/resources/assets/banner-fktv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30300),
                    'Plot': ADDON.getLocalizedString(30350)
                }
            ),
            # Episodes
            ListItem(
                ADDON.getLocalizedString(30301),
                resources.lib.assembleListURL('fktv', 'episodes'),
                ADDON_BASE_PATH + '/resources/assets/banner-fktv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30301),
                    'Plot': ADDON.getLocalizedString(30351)
                }
            ),
            # Postecke
            ListItem(
                ADDON.getLocalizedString(30352),
                resources.lib.assembleListURL('fktv', 'postecke'),
                ADDON_BASE_PATH + '/resources/assets/banner-fktv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30352),
                    'Plot': ADDON.getLocalizedString(30353)
                }
            ),
            # Interviews
            ListItem(
                ADDON.getLocalizedString(30302),
                resources.lib.assembleListURL('fktv', 'interviews'),
                ADDON_BASE_PATH + '/resources/assets/banner-fktv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30302),
                    'Plot': ADDON.getLocalizedString(30354)
                }
            ),
            # Extras
            ListItem(
                ADDON.getLocalizedString(30303),
                resources.lib.assembleListURL('fktv', 'extras') ,
                ADDON_BASE_PATH + '/resources/assets/banner-fktv.png',
                ADDON_BASE_PATH + '/resources/assets/fanart-fktv.jpg',
                {
                    'Title': ADDON.getLocalizedString(30303),
                    'Plot': ADDON.getLocalizedString(30355)
                }
            )
        ]
    
    __urls = {
        'best' : {
            'all'        : HTTP_BASE_URI + 'feed/1-1x1-2x1-3x1-4/hd.xml',
            'episodes'   : HTTP_BASE_URI + 'feed/1-1/hd.xml',
            'postecke'   : HTTP_BASE_URI + 'feed/1-2/hd.xml',
            'interviews' : HTTP_BASE_URI + 'feed/1-3/hd.xml',
            'extras'     : HTTP_BASE_URI + 'feed/1-4/hd.xml'
        },
        'mobile' : {
            'all'        : HTTP_BASE_URI + 'feed/1-1x1-2x1-3x1-4/mobile.xml',
            'episodes'   : HTTP_BASE_URI + 'feed/1-1/mobile.xml',
            'postecke'   : HTTP_BASE_URI + 'feed/1-2/mobile.xml',
            'interviews' : HTTP_BASE_URI + 'feed/1-3/mobile.xml',
            'extras'     : HTTP_BASE_URI + 'feed/1-4/mobile.xml'
        },
        'audio' : {
            'all'        : HTTP_BASE_URI + 'feed/1-1x1-2x1-3x1-4/audio.xml',
            'episodes'   : HTTP_BASE_URI + 'feed/1-1/audio.xml',
            'postecke'   : HTTP_BASE_URI + 'feed/1-2/audio.xml',
            'interviews' : HTTP_BASE_URI + 'feed/1-3/audio.xml',
            'extras'     : HTTP_BASE_URI + 'feed/1-4/audio.xml'
        }
    }


class PTVDataSource(DataSource):
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'best'
            else:
                quality = 'mobile'
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality]['all'], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30211),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/assets/fanart-ptv.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        return 'episodes'
    
    def __getThumbnailURL(self, guid):
        episodeNumber = '1'
        if 'ptv-pilot' == guid[:9]:
            if 'ptv-pilot' != guid:
                # if not very first episode
                episodeNumber= guid[9:]
        else:
            episodeNumber = guid[4:]
            
        return 'http://pantoffel.tv/img/thumbs/ptv' + episodeNumber + '_shot1@2x.jpg'
    
    __urls = {
        'best' : {
            'all' : HTTP_BASE_URI + 'feed/2-1/hd.xml'
        },
        'mobile' : {
            'all' : HTTP_BASE_URI + 'feed/2-1/mobile.xml'
        },
        'audio' : {
            'all' : HTTP_BASE_URI + 'feed/2-1/audio.xml'
        }
    }


class PSDataSource(DataSource):
    def getListItems(self):
        audioOnly = ADDON.getSetting('content.audioOnly')
        
        quality = None
        if 'true' == audioOnly:
            quality = 'audio'
        else:
            if 0 == int(ADDON.getSetting('content.quality')):
                quality = 'best'
            else:
                quality = 'mobile'
        
        data      = resources.lib.parseRSSFeed(self.__urls[quality]['all'], True)
        listItems = []
        
        for i in data:
            iconimage = self.__getThumbnailURL(i['guid'])
            date      = resources.lib.parseUTCDateString(i['pubdate']).strftime('%d.%m.%Y')
            metaData  = {
                'Title'     : i['title'],
                'Genre'     : ADDON.getLocalizedString(30221),
                'Date'      : date,
                'Premiered' : date,
                'Country'   : ADDON.getLocalizedString(30232),
                'Plot'      : i['description'],
                'Duration'  : int(i['duration']) / 60
            }
            streamInfo = {
                'duration' : i['duration']
            }
            
            listItems.append(
                ListItem(
                    i['title'],
                    resources.lib.assemblePlayURL(i['url'], i['title'], iconimage, metaData, streamInfo),
                    iconimage,
                    ADDON_BASE_PATH + '/resources/assets/fanart-ps.jpg',
                    metaData,
                    streamInfo,
                    False
                )
            )
        
        return listItems
    
    def getContentMode(self):
        return 'episodes'
    
    def __getThumbnailURL(self, guid):
        if 'ps-pilot' == guid:
            guid = 'ps1'
        return 'http://massengeschmack.tv/img/ps/' + guid + '.jpg'
    
    __urls = {
        'best' : {
            'all' : HTTP_BASE_URI + 'feed/3-1/hd.xml'
        },
        'mobile' : {
            'all' : HTTP_BASE_URI + 'feed/3-1/mobile.xml'
        },
        'audio' : {
            'all' : HTTP_BASE_URI + 'feed/3-1/audio.xml'
        }
    }


def createDataSource(module=''):
    """
    Create a data source object based on the magazine name.
    If left empty, an overview data source will be generated.
    
    @type module: str
    @keyword module: the magazine name (fktv, ptv, pschlau, mgtv, ...)
    @return: DataSource instance
    """
    if 'fktv' == module:
        return FKTVDataSource()
    elif 'ptv' == module:
        return PTVDataSource()
    elif 'ps' == module:
        return PSDataSource()
    else:
        return DataSource()