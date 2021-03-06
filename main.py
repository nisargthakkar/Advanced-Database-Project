import sys
import DatabaseManager
import Timer

DEADLOCK_DETECTION_PERIOD = 10

def bootstrap(DBM):
	# Set up all objects and data in all sites
	DBM.init(Timer.CURRENT_TIME)

if __name__ == '__main__':

	inputSource = sys.stdin

	if len(sys.argv) > 1:
		f = open(sys.argv[1], 'r')
		if f.mode == 'r':
			inputSource = f.readlines()

	DBM = DatabaseManager.DatabaseManager
	TM = DBM.TM
	SM = DBM.SM

	bootstrap(DBM)

	for originalLine in inputSource:
		line = ''.join(filter(lambda c: c != ' ' and c != '\t' and c != '\n' and c is not None, originalLine))
		# print(originalLine.strip())

		indexOfCommentStart = line.find('//')

		if indexOfCommentStart != -1:
			line = line[:indexOfCommentStart]

		# Was a comment line
		if line == '' and indexOfCommentStart != -1:
			continue


		elif line.startswith('querystate()'):
			DBM.printState()
			continue


		elif line.startswith('quit'):
			break


		Timer.CURRENT_TIME = Timer.CURRENT_TIME + 1
		if Timer.CURRENT_TIME % DEADLOCK_DETECTION_PERIOD == 0:
			TM.detectDeadlock()

		if len(line) == 0:
			continue


		elif line.startswith('beginRO'):
			transaction = line[8:-1]
			TM.beginTransaction(transaction, Timer.CURRENT_TIME, True)


		elif line.startswith('begin'):
			transaction = line[6:-1]
			TM.beginTransaction(transaction, Timer.CURRENT_TIME, False)


		elif line.startswith('W'):
			write_tuple = line[2:-1]
			write_list = write_tuple.split(',')
			transaction = write_list[0].strip()
			key = write_list[1].strip()
			value = write_list[2].strip()
			TM.writeValue(transaction, key, value)


		elif line.startswith('R'):
			write_tuple = line[2:-1]
			write_list = write_tuple.split(',')
			transaction = write_list[0].strip()
			key = write_list[1].strip()
			TM.readValue(transaction, key)


		elif line.startswith('fail'):
			site = line[5:-1]
			SM.fail(site)


		elif line.startswith('recover'):
			site = line[8:-1]
			SM.recover(site, Timer.CURRENT_TIME)


		elif line.startswith('end'):
			transaction = line[4:-1]
			TM.endTransaction(transaction, Timer.CURRENT_TIME)


		elif line.startswith('dump(x'):
			key = line[5:-1]
			DBM.dumpKey(key)


		elif line.startswith('dump()'):
			DBM.dumpAll()


		elif line.startswith('dump'):
			site = line[5:-1]
			SM.dumpSite(site)

		else:
			Timer.CURRENT_TIME -= 1
			print('Invalid Command')

		# print()

	# DBM.printState()