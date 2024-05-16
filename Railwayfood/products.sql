BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER,
	"name"	TEXT,
	"description"	TEXT,
	PRIMARY KEY("id")
);



INSERT INTO "products" VALUES (0,'Wanpaku Sandhwich','tasty');
INSERT INTO "products" VALUES (1,'Wanpaku Sandwhich','tasty');
INSERT INTO "products" VALUES (3,'Wanpaku Sandwhich','tasty');
INSERT INTO "products" VALUES (5,'Wanpaku Sandwhich','tasty');
INSERT INTO "products" VALUES (68,'Honey BBQ Boneless Chicken','yummy');
INSERT INTO "products" VALUES (77,'Wanpaku Sandwhich','tasty');


COMMIT;