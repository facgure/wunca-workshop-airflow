-- U_MULTIRANK_RANKING.UM_GRADE definition

CREATE TABLE `UM_GRADE` (
  `RANK` int NOT NULL COMMENT 'เลขอ้างอิงเกรด',
  `GRADE` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'เกรด',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`RANK`) USING BTREE,
  KEY `grade` (`GRADE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='เกรด';


-- U_MULTIRANK_RANKING.UM_INDICATOR definition

CREATE TABLE `UM_INDICATOR` (
  `INID` int NOT NULL COMMENT 'เลขอ้างอิงตัวชี้วัดหลัก',
  `NAME` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'ชื่อตัวชี้วัดหลัก',
  `COLGROUP` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'ประเภทตัวชี้วัด',
  `SORT` int NOT NULL COMMENT 'ลำดับในการแสดงผลของตัวชี้วัดหลักที่หน้าเว็บไซต์',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`INID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='หัวข้อตัวชี้วัด';


-- U_MULTIRANK_RANKING.UM_SUBJECT definition

CREATE TABLE `UM_SUBJECT` (
  `SUBJECT_ID` int NOT NULL COMMENT 'เลขอ้างอิงสาขาวิชา',
  `NAME` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'ชื่อสาขาวิชา',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`SUBJECT_ID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='รายชื่อคณะ';


-- U_MULTIRANK_RANKING.UM_UNIVERSITY definition

CREATE TABLE `UM_UNIVERSITY` (
  `UID` int NOT NULL COMMENT 'เลขอ้างอิงมหาวิทยาลัย',
  `NAME` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'รายชื่อมหาวิทยาลัย',
  `SLUG` varchar(256) DEFAULT NULL COMMENT 'slug ของแต่ละมหาวิทยาลัย',
  `URL` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'url ของแต่ละมหาวิทยาลัย',
  `STREET` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'รายชื่อถนนที่ตั้ง',
  `CITY` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'รายชื่อเมือง',
  `COUNTRY` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'รายชื่อประเทศ',
  `PHONE` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'หมายเลขโทรศัพท์',
  `FAX` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'หมายเลขแฟกซ์',
  `POSTALCODE` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'รหัสไปรษณีย์',
  `REMARK` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'หมายเหตุ',
  `PROFILE` varchar(4096) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'โปรไฟล์ของมหาวิทยาลัย',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`UID`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='รายชื่อมหาวิทยาลัยของ U-multirank';


-- U_MULTIRANK_RANKING.UM_MAJOR definition

CREATE TABLE `UM_MAJOR` (
  `SUBJECT_ID` int NOT NULL COMMENT 'เลขอ้างอิงสาขาวิชา',
  `MAJOR_ID` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'เลขอ้างอิงวิชาเอก',
  `NAME` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'ชื่อวิชาเอก',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`MAJOR_ID`) USING BTREE,
  KEY `subject_id` (`SUBJECT_ID`),
  CONSTRAINT `UM_MAJOR_ibfk_1` FOREIGN KEY (`SUBJECT_ID`) REFERENCES `UM_SUBJECT` (`SUBJECT_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='รายชื่อสาขาวิชา';


-- U_MULTIRANK_RANKING.UM_SUB_INDICATOR definition

CREATE TABLE `UM_SUB_INDICATOR` (
  `INID` int NOT NULL COMMENT 'เลขอ้างอิงตัวชี้วัดหลัก',
  `SUBINID` int NOT NULL COMMENT 'เลขอ้างอิงตัวชี้วัดย่อย',
  `NAME` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'ชื่อตัวชี้วัดย่อย',
  `SORT` int DEFAULT NULL COMMENT 'ลำดับในการแสดงผลของตัวชี้วัดหลักที่หน้าเว็บไซต์',
  `MIN` int DEFAULT NULL COMMENT 'คะแนนต่ำสุด',
  `MAX` int DEFAULT NULL COMMENT 'คะแนนสูงสุด',
  `VALUE_TYPE` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'ชนิดของข้อมูล',
  `DESCRIPTION` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'คำอธิบายตัวชี้วัด',
  `LOWER_IS_BETTER` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'คะแนนต่ำดีกว่า',
  `DECIMAL` int DEFAULT NULL COMMENT 'จำนวนทศนิยม',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`SUBINID`) USING BTREE,
  KEY `inid` (`INID`),
  CONSTRAINT `UM_SUB_INDICATOR_ibfk_1` FOREIGN KEY (`INID`) REFERENCES `UM_INDICATOR` (`INID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='หัวข้อตัวชี้วัดย่อย';


-- U_MULTIRANK_RANKING.UM_RANK definition

CREATE TABLE `UM_RANK` (
  `UID` int NOT NULL COMMENT 'เลขอ้างอิงมหาวิทยาลัย',
  `INID` int NOT NULL COMMENT 'เลขอ้างอิงตัวชี้วัดหลัก',
  `SUBINID` int NOT NULL COMMENT 'เลขอ้างอิงตัวชี้วัดย่อย',
  `SUBJECT_ID` int NOT NULL COMMENT 'เลขอ้างอิงสาขาวิชา',
  `MAJOR_ID` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'เลขอ้างอิงวิชาเอก',
  `SCORE` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'คะแนน',
  `RANK_GROUP` int DEFAULT NULL COMMENT 'เลขอ้างอิงเกรด',
  `REMARK` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'คำอธิบายคะแนน',
  `ENTITY` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'คะแนนเต็ม',
  `VALUE_TYPE` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'ชนิดของคะแนน',
  `YEAR` year NOT NULL COMMENT 'ปีการจัดอันดับ',
  `LAST_UPDATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่ปรับปรุงข้อมูล',
  PRIMARY KEY (`UID`,`INID`,`SUBINID`,`SUBJECT_ID`,`MAJOR_ID`,`YEAR`) USING BTREE,
  KEY `uid` (`UID`),
  KEY `subinid` (`SUBINID`),
  KEY `inid` (`INID`),
  KEY `rank_fk_4` (`SUBJECT_ID`),
  KEY `rank_fk_5` (`MAJOR_ID`),
  KEY `rank_fk_8` (`RANK_GROUP`),
  CONSTRAINT `UM_RANK_ibfk_1` FOREIGN KEY (`UID`) REFERENCES `UM_UNIVERSITY` (`UID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UM_RANK_ibfk_2` FOREIGN KEY (`SUBINID`) REFERENCES `UM_SUB_INDICATOR` (`SUBINID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UM_RANK_ibfk_3` FOREIGN KEY (`INID`) REFERENCES `UM_INDICATOR` (`INID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UM_RANK_ibfk_4` FOREIGN KEY (`SUBJECT_ID`) REFERENCES `UM_SUBJECT` (`SUBJECT_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UM_RANK_ibfk_5` FOREIGN KEY (`MAJOR_ID`) REFERENCES `UM_MAJOR` (`MAJOR_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `UM_RANK_ibfk_6` FOREIGN KEY (`RANK_GROUP`) REFERENCES `UM_GRADE` (`RANK`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ข้อมูลคะแนนของแต่ละมหาวิทยาลัยตามหัวข้อตัวชี้วัด';