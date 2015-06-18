# encoding: utf-8
"""
change.py

Created by Thomas Mangin on 2009-11-05.
Copyright (c) 2009-2015 Exa Networks. All rights reserved.
"""

from exabgp.protocol.family import AFI
from exabgp.protocol.family import SAFI

from exabgp.bgp.message.update.attribute import Attribute


class Source (object):
	UNSET         = 0
	CONFIGURATION = 1
	API           = 2
	NETWORK       = 3


class Change (object):
	SOURCE = Source.UNSET

	__slots__ = ['nlri','attributes']

	_add_family = (
		(AFI.ipv4,SAFI.unicast),
		(AFI.ipv4,SAFI.multicast),
		(AFI.l2vpn,SAFI.vpls)
	)

	def __init__ (self, nlri, attributes):
		self.nlri = nlri
		self.attributes = attributes

	def index (self):
		return '%02x%02x' % self.nlri.family() + self.nlri.index()

	def __eq__ (self, other):
		return self.nlri == other.nlri and self.attributes == other.attributes

	def __ne__ (self, other):
		return self.nlri != other.nlri or self.attributes != other.attributes

	def __lt__ (self, other):
		raise RuntimeError('comparing Change for ordering does not make sense')

	def __le__ (self, other):
		raise RuntimeError('comparing Change for ordering does not make sense')

	def __gt__ (self, other):
		raise RuntimeError('comparing Change for ordering does not make sense')

	def __ge__ (self, other):
		raise RuntimeError('comparing Change for ordering does not make sense')

	def extensive (self):
		# If you change this you must change as well extensive in Update
		return "%s%s" % (str(self.nlri),str(self.attributes))

	def add (self,attribute):

		if attribute.ID != Attribute.CODE.NEXT_HOP:
			return self.attributes.add(attribute)

		if (self.nlri.afi,self.nlri.safi) in self._add_family:
			self.attributes.add(attribute)
			self.nlri.nexthop = attribute

		return True

	def __repr__ (self):
		return self.extensive()


class ConfigurationChange (Change):
	SOURCE = Source.CONFIGURATION


class APIChange (Change):
	SOURCE = Source.API


class NetworkChange (Change):
	SOURCE = Source.NETWORK
