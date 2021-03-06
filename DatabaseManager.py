import TransactionManager
import SiteManager
import Timer

class DatabaseManager:
	TM = TransactionManager.TransactionManager
	SM = SiteManager.SiteManager

	def printState():
		print('\n=============================System State=============================')
		print('Current Time =', Timer.CURRENT_TIME)
		TM = DatabaseManager.TM
		SM = DatabaseManager.SM
		TM.print()
		SM.print()
		print('======================================================================')

	def siteStrKey(siteStr):
		return int(siteStr)

	def siteObjKey(siteObj):
		return int(siteObj.site)

	def init(time):
		DatabaseManager.SM.init(time)

	def dumpAll():
		sitesUnordered = DatabaseManager.SM.sites.keys()
		sitesOrdered = sorted(sitesUnordered, key=DatabaseManager.siteStrKey)
		for site in sitesOrdered:
			DatabaseManager.SM.sites[site]['site'].DM.dump()

	def dumpKey(key):
		key_index = int(key[1:])
		sitesUnordered = DatabaseManager.SM.findSitesForKeyIndex(key_index)
		sitesOrdered = sorted(sitesUnordered, key=DatabaseManager.siteObjKey)
		for site in sitesOrdered:
			site.DM.dumpKey(key)
