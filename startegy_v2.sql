/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : football

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-07-23 08:59:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `k_startegy`
-- ----------------------------
DROP TABLE IF EXISTS `k_startegy_v2`;
CREATE TABLE `k_startegy_v2` (
  `type` varchar(255) NOT NULL,
  `rate` float(11) DEFAULT 0,
  `score` int(11) DEFAULT 0,
  `small_do` varchar(255) DEFAULT '',
  `else_do` varchar(255) DEFAULT '',
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of k_startegy
-- ----------------------------
INSERT INTO `k_startegy_v2` VALUES ('印尼L2', '1.5', '2', '买小', '');
INSERT INTO `k_startegy_v2` VALUES ('中超女联', '1.4', '2', '买小', '买大');
INSERT INTO `k_startegy_v2` VALUES ('南韩杯', '1.4', '2', '', '买大');
INSERT INTO `k_startegy_v2` VALUES ('日职乙', '1.4', '2', '买小', '');
INSERT INTO `k_startegy_v2` VALUES ('中协杯', '1.9', '2', '买小', '');
INSERT INTO `k_startegy_v2` VALUES ('柬超', '1.75', '2', '买大', '买小');
INSERT INTO `k_startegy_v2` VALUES ('澳维U20', '2', '2', '买小', '');
INSERT INTO `k_startegy_v2` VALUES ('印尼超', '1.4', '2', '买小', '买大');
INSERT INTO `k_startegy_v2` VALUES ('南澳女超', '1.9', '2', '', '买小');
INSERT INTO `k_startegy_v2` VALUES ('泰丁', '1.5', '2', '', '买大');
