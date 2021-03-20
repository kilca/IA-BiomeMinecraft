import sqlite3 as sql
import time

sourceDB = sql.connect('/home/nonoreve/Downloads/coreProtectSalc1.db')
destDB = sql.connect('findTheBiome.db')

# main query :
# only overworld
# no rolled back blocks
# no blocks with tile entities
# only placed and breaked actions
# only real players
# coordinates less than 1_000_000
nbrows = 5_000_000
cursor = sourceDB.execute(f"SELECT U.user, B.action, M.material, B.data, B.x, B.y, B.z, B.time \
						  FROM co_block AS B, co_user AS U , co_material_map AS M \
						  WHERE B.user == U.id \
						  AND B.type == M.id \
						  AND B.wid == 1 \
						  AND B.rolled_back == 0 \
						  AND B.Meta IS NULL \
						  AND B.Action != 2 \
						  AND U.uuid NOT NULL \
						  AND B.x < 1000000 \
						  AND B.z < 1000000 \
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

destDB.execute("CREATE TABLE Event( \
					Id INTEGER PRIMARY KEY NOT NULL, \
					User TEXT, \
					Action INT NOT NULL, \
					Material TEXT NOT NULL, \
					Data INTEGER, \
					X INTEGER NOT NULL, \
					Y INTEGER NOT NULL, \
					Z INTEGER NOT NULL, \
					Time INTEGER NOT NULL\
				);")

index = 1
for row in total:
	destDB.execute(f"INSERT INTO Event VALUES({index}, '{row[0]}', {row[1]}, '{row[2]}', {row[3]}, {row[4]}, {row[5]}, {row[6]}, {row[7]})")
	index += 1
print("Done writing")
destDB.commit()
destDB.close()
sourceDB.close()
