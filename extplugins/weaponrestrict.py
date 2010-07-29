# -*- coding: utf-8 -*-
# b3/plugins/weaponrestrict.py
#
# Based on antinoob.py by
# Gamers 4 Gamers (http://g4g.pl)
# Copyright (C) 2009 Anubis
# 
# Modified for BFBC2 by
# Durzo <durzo@badcompany2.com.au>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# CHANGELOG
#    27/07/2010 - 1.0.0 - Durzo
#    -- First revision

__version__ = '1.0.0'
__author__  = 'Durzo'
from b3 import clients
import b3, string, re, threading
import b3.events
import b3.plugin


class WeaponInfo:
    _weaponName = ""
    
#--------------------------------------------------------------------------------------------------
class WeaponrestrictPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    _restrictedweapons = []    
    _defaultkickmsg = 'Do not use restricted weapons'

    def onStartup(self):
        self.registerEvent(b3.events.EVT_CLIENT_KILL)
        self.registerEvent(b3.events.EVT_CLIENT_SPAWN)
        self._adminPlugin = self.console.getPlugin('admin')
        self.info('WARNING: The use of this plugin may violate EA\'s Rules of Conduct for server administrators, for more info see http://tinyurl.com/eabc2roc')

    def onLoadConfig(self):
        self.debug('Loading Configuration Started')
        self._kickmsg = self.config.get('settings', 'kick_message')
        if self._kickmsg == '':
            self._kickmsg = self._defaultkickmsg
        
        for e in self.config.get('restricted_weapons/weapon'):
            _wi = WeaponInfo()
            if e.text:
                _wi._weaponName = e.text
            else:
                _wi._weaponName = ""
            
            if (_wi._weaponName != ""):
                self.info('Restricted Weapon Loaded: >' + _wi._weaponName + '<')
                self._restrictedweapons.append(_wi)
            else:
                self.debug('Restricted Weapon - Empty definition ignored')                  
                
        self.debug('Loading Configuration Finished')
        return
                
    #--------------------------------------------------------------------------------------#          
    def checkSpawn(self, gadgetname, pistolname, weaponname, player):
        for weaponInfo in self._restrictedweapons:
                if weaponInfo._weaponName == weaponname or weaponInfo._weaponName == gadgetname or weaponInfo._weaponName == pistolname:
                    self.info('Restricted Weapon: ' + str(weaponInfo._weaponName) + ' equipped on ' + str(player.name))
                    player.message('[WARNING] Do not use the %s or you will be kicked' % weaponInfo._weaponName)
                    player.messagebig('[WARNING] Do not use the %s or you will be kicked' % weaponInfo._weaponName)

        return
     
    #--------------------------------------------------------------------------------------#
    def checkWeapon(self, weaponname, player):
        for weaponInfo in self._restrictedweapons:
                if weaponInfo._weaponName == weaponname:
                    self.info('Restricted Weapon: ' + str(weaponname) + ' used by ' + str(player.name))
                    self.kickPlayerForRestrictedWeapon(player)
                    return

        return
        
    #---------------------------------------------------------------------------#
    def kickPlayerForRestrictedWeapon(self, player):
        if player:
            warningmsg = self.getKickWarningForRestrictedWeapon()
            self.debug('player.kick: ' + str(player.name) + ' Warn: ' + str(warningmsg))
            player.kick(warningmsg)
        return

    #---------------------------------------------------------------------------#
    def getKickWarningForRestrictedWeapon(self):
        defwarning = "Do not use restricted weapons!"
        try:
            warning = self._kickmsg
        except:
            warning = defwarning
        
        return warning

    #---------------------------------------------------------------------------# 
    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_KILL or event.type == b3.events.EVT_CLIENT_KILL_TEAM:
            weaponname = event.data[1]
            self.checkWeapon(weaponname, event.client)
        elif event.type == b3.events.EVT_CLIENT_SPAWN:
            gadgetname = event.data[1]
            pistolname = event.data[2]
            weaponname = event.data[3]
            self.checkSpawn(gadgetname, pistolname, weaponname, event.client)
