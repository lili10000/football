/*
Navicat MySQL Data Transfer

Source Server         : football
Source Server Version : 80015
Source Host           : localhost:3306
Source Database       : football

Target Server Type    : MYSQL
Target Server Version : 80015
File Encoding         : 65001

Date: 2019-06-21 18:52:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `k_checkrate`
-- ----------------------------
DROP TABLE IF EXISTS `k_checkrate`;
CREATE TABLE `k_checkrate` (
  `id_game` int(11) NOT NULL,
  `newRate` float(6,3) DEFAULT NULL,
  `oldRate` float(6,3) DEFAULT NULL,
  `score` int(3) DEFAULT NULL,
  `createTime` int(11) DEFAULT NULL,
  `updateTime` int(11) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_game`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of k_checkrate
-- ----------------------------
INSERT INTO `k_checkrate` VALUES ('631010', '3.250', '3.000', '-1', '1561113710', '0', '江苏苏宁 vs 上海申花');
INSERT INTO `k_checkrate` VALUES ('632238', '3.750', '4.000', '4', '1561082410', '1561091760', null);
INSERT INTO `k_checkrate` VALUES ('632544', '3.250', '3.000', '-1', '1561108814', '0', '苏黎世 vs 温特图尔');
INSERT INTO `k_checkrate` VALUES ('632711', '3.250', '3.500', '1', '1561100436', '1561109329', null);
INSERT INTO `k_checkrate` VALUES ('632723', '5.250', '4.500', '5', '1561102155', '1561114220', null);
INSERT INTO `k_checkrate` VALUES ('632733', '3.750', '3.500', '0', '1561107862', '1561114250', '梅特罗联 女子 vs 富勒姆联 女子');
INSERT INTO `k_checkrate` VALUES ('632747', '5.250', '5.500', '-1', '1561103277', '0', null);
INSERT INTO `k_checkrate` VALUES ('632782', '4.000', '4.250', '0', '1561112680', '1561114363', '安纳利 vs 北极星');
