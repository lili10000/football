/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : football

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2019-02-21 16:23:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `k_endscore`
-- ----------------------------
DROP TABLE IF EXISTS `k_endscore`;
CREATE TABLE `k_endscore` (
  `key` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `rate` float(3,3) DEFAULT NULL,
  `hostScore` int(11) DEFAULT NULL,
  `guestScore` int(11) DEFAULT NULL,
  `haveScore` tinyint(4) DEFAULT NULL,
  `mainRate` float(3,3) DEFAULT NULL,
  `clientRate` float(3,3) DEFAULT NULL,
  `scoreTime` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
