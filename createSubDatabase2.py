import sqlite3 as sql
import time

sourceDB = sql.connect(r'C:\Users\kilca\Documents\ApprentissageAuto\Projet\IA-BiomeMinecraft\map\findTheBiomeV1.db')
destDB = sql.connect(r'findTheBiomeBV1.db')

# main query :
# only overworld
# no rolled back blocks
# no blocks with tile entities
# only placed and breaked actions
# only real players
# coordinates less than 1_000_000
nbrows = 5_000_000
cursor = sourceDB.execute(f"SELECT * \
						  FROM Event \
						  WHERE Event.Material IN \
						  (\'minecraft:dirt\',\'minecraft:long_grass\',\'minecraft:sand\',\
						  \'minecraft:leaves\',\'minecraft:log\',\'minecraft:sandstone\',\
						  \'minecraft:grass\',\'minecraft:water\',\'minecraft:snow\',\
						  \'minecraft:cactus\') \
						  AND Event.Y > 40 \
						  AND Event.X < -320000\
						  AND Event.X > -380000\
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
destDB.execute("DROP TABLE EVENT;")
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
	#print("VAL ROW 2",row[2])
	destDB.execute(f"INSERT INTO Event VALUES({row[0]}, '{row[1]}', {row[2]}, '{row[3]}', {row[4]}, {row[5]}, {row[6]}, {row[7]},{row[8]})")
	index += 1
print("Done writing")
destDB.commit()
destDB.close()
sourceDB.close()
