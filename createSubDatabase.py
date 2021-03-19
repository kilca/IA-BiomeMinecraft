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
nbrows = 1_000_000
cursor = sourceDB.execute(f"SELECT U.user, B.action, M.material, B.data, B.x, B.y, B.z, B.time\
						  FROM co_block AS B, co_user AS U , co_material_map AS M\
						  WHERE B.user == U.id \
						  AND B.type == M.id\
						  AND B.wid == 1 \
						  AND B.rolled_back == 0 \
						  AND B.Meta IS NULL \
						  AND B.Action != 2 \
						  AND U.uuid NOT NULL \
						  LIMIT {nbrows}")
# for row in cursor:
	# for index, name in enumerate(cursor.description):
		# print(name + ' : ' + str(row[index]))
	# print()

start = time.time()
cursor.arraysize = nbrows // 100
total = rows = cursor.fetchmany()
while rows:
	rows = cursor.fetchmany()
	total += rows
	print(f"{len(total)} : {len(total)/nbrows * 100:.2f}%...")
print(f"Fetched {nbrows} rows in {time.time() - start}s.")



for row in total:
	action = ""
	if row[1] == 1:
		action = "placed"
	else:
		action = "broke"
	print(f"{row[0]} {action} {row[2]}:{row[3]} at X={row[4]} Y={row[5]} Z={row[6]} time={row[7]}")
