BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "record" (
	"datetime"	TEXT,
	"port"	TEXT,
	"r1"	TEXT,
	"r2"	TEXT,
	"r3"	TEXT,
	"r4"	TEXT,
	"r5"	TEXT,
	"r6"	TEXT,
	"r7"	TEXT,
	"r8"	TEXT,
	"r9"	TEXT,
	"r10"	TEXT,
	"r11"	TEXT,
	"r12"	TEXT,
	"r13"	TEXT,
	"r14"	TEXT,
	"r15"	TEXT,
	"r16"	TEXT,
	"r17"	TEXT,
	"r18"	TEXT,
	"r19"	TEXT,
	"r20"	TEXT,
	"r21"	TEXT,
	"r22"	TEXT,
	"r23"	TEXT,
	"r24"	TEXT,
	"r25"	TEXT,
	"r26"	TEXT,
	"r27"	TEXT,
	"r28"	TEXT,
	"r29"	TEXT,
	"r30"	TEXT,
	"r31"	TEXT,
	"r32"	TEXT,
	"r33"	TEXT,
	"r34"	TEXT,
	"r35"	TEXT,
	"r36"	TEXT,
	"r37"	TEXT,
	"r38"	TEXT,
	"r39"	TEXT,
	"r40"	TEXT,
	"r41"	TEXT,
	"r42"	TEXT,
	"r43"	TEXT,
	"r44"	TEXT,
	"r45"	TEXT,
	"r46"	TEXT,
	"r47"	TEXT,
	"r48"	TEXT,
	"r49"	TEXT,
	"r50"	TEXT,
	"r51"	TEXT,
	"r52"	TEXT,
	"r53"	TEXT,
	"r54"	TEXT,
	"r55"	TEXT,
	"r56"	TEXT,
	"r57"	TEXT,
	"r58"	TEXT,
	"r59"	TEXT,
	"r60"	TEXT,
	"r61"	TEXT,
	"r62"	TEXT,
	"r63"	TEXT,
	"r64"	TEXT,
	"r65"	TEXT,
	"r66"	TEXT,
	"r67"	TEXT,
	"r68"	TEXT,
	"r69"	TEXT,
	"r70"	TEXT,
	"r71"	TEXT
);
CREATE TABLE IF NOT EXISTS "colname" (
	"datetime"	TEXT,
	"port"	TEXT,
	"r1"	TEXT,
	"r2"	TEXT,
	"r3"	TEXT,
	"r4"	TEXT,
	"r5"	TEXT,
	"r6"	TEXT,
	"r7"	TEXT,
	"r8"	TEXT,
	"r9"	TEXT,
	"r10"	TEXT,
	"r11"	TEXT,
	"r12"	TEXT,
	"r13"	TEXT,
	"r14"	TEXT,
	"r15"	TEXT,
	"r16"	TEXT,
	"r17"	TEXT,
	"r18"	TEXT,
	"r19"	TEXT,
	"r20"	TEXT,
	"r21"	TEXT,
	"r22"	TEXT,
	"r23"	TEXT,
	"r24"	TEXT,
	"r25"	TEXT,
	"r26"	TEXT,
	"r27"	TEXT,
	"r28"	TEXT,
	"r29"	TEXT,
	"r30"	TEXT,
	"r31"	TEXT,
	"r32"	TEXT,
	"r33"	TEXT,
	"r34"	TEXT,
	"r35"	TEXT,
	"r36"	TEXT,
	"r37"	TEXT,
	"r38"	TEXT,
	"r39"	TEXT,
	"r40"	TEXT,
	"r41"	TEXT,
	"r42"	TEXT,
	"r43"	TEXT,
	"r44"	TEXT,
	"r45"	TEXT,
	"r46"	TEXT,
	"r47"	TEXT,
	"r48"	TEXT,
	"r49"	TEXT,
	"r50"	TEXT,
	"r51"	TEXT,
	"r52"	TEXT,
	"r53"	TEXT,
	"r54"	TEXT,
	"r55"	TEXT,
	"r56"	TEXT,
	"r57"	TEXT,
	"r58"	TEXT,
	"r59"	TEXT,
	"r60"	TEXT,
	"r61"	TEXT,
	"r62"	TEXT,
	"r63"	TEXT,
	"r64"	TEXT,
	"r65"	TEXT,
	"r66"	TEXT,
	"r67"	TEXT,
	"r68"	TEXT,
	"r69"	TEXT,
	"r70"	TEXT,
	"r71"	TEXT
);
CREATE TABLE IF NOT EXISTS "record_simple" (
	"datetime"	TEXT,
	"port"	TEXT,
	"ivoltage"	TEXT,
	"icurrent"	TEXT,
	"ovoltage"	TEXT,
	"ocurrent"	TEXT
);
CREATE TABLE IF NOT EXISTS "control_history" (
	"datetime"	TEXT,
	"num"	TEXT,
	"voltage"	TEXT,
	"current"	TEXT,
	"operation"	TEXT
);
CREATE TABLE IF NOT EXISTS "control" (
	"num"	INTEGER,
	"voltage_max"	TEXT,
	"voltage_min"	TEXT,
	"starttime"	TEXT,
	"duration"	TEXT,
	"relay1"	TEXT,
	"relay2"	TEXT,
	"relay3"	TEXT
);
COMMIT;
