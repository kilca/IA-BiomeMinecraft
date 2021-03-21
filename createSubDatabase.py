import sqlite3 as sql
import time

sourceDB = sql.connect('/home/nonoreve/Downloads/coreProtectSalc1.db')
destDB = sql.connect('findTheBiomeV2.db')

# main query :
# only overworld
# no rolled back blocks
# no blocks with tile entities
# only placed and breaked actions
# only real players
# coordinates less than 50_000
nbrows = 1_000_000
cursor = sourceDB.execute(f"SELECT B.user, B.action, B.type, B.data, B.x, B.y, B.z, B.time \
						  FROM co_block AS B, co_user AS U \
						  WHERE B.user == U.id \
						  AND B.wid == 1 \
						  AND B.rolled_back == 0 \
						  AND B.Meta IS NULL \
						  AND B.Action != 2 \
						  AND U.uuid NOT NULL \
						  AND B.x < 50000 \
						  AND B.x > -50000 \
						  AND B.z < 50000 \
						  AND B.z > -50000 \
						  LIMIT {nbrows}")
# for row in cursor:
	# for index, name in enumerate(cursor.description):
		# print(name + ' : ' + str(row[index]))
	# print()

start = time.time()
cursor.arraysize = 1000
total = rows = cursor.fetchmany()
while rows:
	print(f"{len(total)} rows loaded : {len(total)/nbrows * 100:.2f}% ... [{time.strftime('%H:%M:%S')}]")
	rows = cursor.fetchmany()
	total += rows
print(f"Fetched {nbrows} rows in {(time.time() - start)/60:.1f}min.")

users = [row[0] for row in total]
individual_users = set(users)
for user in individual_users:
	print(user, end=' ')
print(f"Found {len(individual_users)} individual users ({len(individual_users)/len(users) * 100:.3f}% of total)")

for row in total[:10]:
	action = ""
	if row[1] == 1:
		action = "placed"
	else:
		action = "broke"
	print(f"{row[0]} {action} {row[2]}:{row[3]} at X={row[4]} Y={row[5]} Z={row[6]} time={row[7]}")
print()

destDB.execute("DROP TABLE IF EXISTS Event")
destDB.execute("CREATE TABLE Event( \
					Id INTEGER PRIMARY KEY NOT NULL, \
					User INTEGER NOT NULL, \
					Action INTEGER NOT NULL, \
					Material INTEGER NOT NULL, \
					Data INTEGER, \
					X INTEGER NOT NULL, \
					Y INTEGER NOT NULL, \
					Z INTEGER NOT NULL, \
					Time INTEGER NOT NULL\
				);")

index = 1
for row in total:
	destDB.execute(f"INSERT INTO Event VALUES({index}, {row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]})")
	index += 1
destDB.commit()
print("Done writing Events")
print()



# Material map query
cursor = sourceDB.execute(f"SELECT * \
						  FROM co_material_map ")

# start = time.time()
# total = cursor.fetchmany()
# print(f"Fetched {len(total)} rows in {(time.time() - start)/60:.1f}min.")

destDB.execute("DROP TABLE IF EXISTS Material")
destDB.execute("CREATE TABLE Material( \
					Id INTEGER PRIMARY KEY NOT NULL, \
					Material TEXT NOT NULL \
				);")

for row in cursor:
	destDB.execute(f"INSERT INTO Material VALUES({row[0]}, '{row[1]}')")
destDB.commit()
print("Done writing Materials")
print()



# User query
cursor = sourceDB.execute(f"SELECT * \
						  FROM co_user ")

# start = time.time()
# total = cursor.fetchmany()
# print(f"Fetched {len(total)} rows in {(time.time() - start)/60:.1f}min.")

destDB.execute("DROP TABLE IF EXISTS User")
destDB.execute("CREATE TABLE User( \
					Id INTEGER PRIMARY KEY NOT NULL, \
					Time INTEGER NOT NULL, \
					User TEXT NOT NULL, \
					Uuid TEXT \
				);")

for row in cursor:
	if row[3] is None:
		destDB.execute(f"INSERT INTO User VALUES({row[0]}, {row[1]}, '{row[2]}', NULL)")
	else:
		destDB.execute(f"INSERT INTO User VALUES({row[0]}, {row[1]}, '{row[2]}', '{row[3]}')")
destDB.commit()
print("Done writing User")
print()

destDB.close()
sourceDB.close()
