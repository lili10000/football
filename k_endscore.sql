/*
Navicat MySQL Data Transfer

Source Server         : football
Source Server Version : 80015
Source Host           : localhost:3306
Source Database       : football

Target Server Type    : MYSQL
Target Server Version : 80015
File Encoding         : 65001

Date: 2019-06-20 20:34:28
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
  PRIMARY KEY (`id_game`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of k_checkrate
-- ----------------------------
INSERT INTO `k_checkrate` VALUES ('630648', '3.000', '2.750', null);
INSERT INTO `k_checkrate` VALUES ('630805', '3.000', '3.250', null);
INSERT INTO `k_checkrate` VALUES ('632146', '3.250', '3.000', null);
INSERT INTO `k_checkrate` VALUES ('632361', '3.250', '3.000', null);
INSERT INTO `k_checkrate` VALUES ('632364', '3.250', '3.000', '-1');
INSERT INTO `k_checkrate` VALUES ('632481', '2.750', '3.000', null);
INSERT INTO `k_checkrate` VALUES ('632509', '2.750', '2.500', null);
INSERT INTO `k_checkrate` VALUES ('632511', '3.750', '3.500', null);
INSERT INTO `k_checkrate` VALUES ('632618', '3.500', '3.750', '-1');
