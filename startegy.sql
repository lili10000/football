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
DROP TABLE IF EXISTS `k_startegy`;
CREATE TABLE `k_startegy` (
  `type` varchar(255) NOT NULL,
  `time` int(11) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `small_do` varchar(255) DEFAULT '',
  `else_do` varchar(255) DEFAULT '',
  PRIMARY KEY (`type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of k_startegy
-- ----------------------------
INSERT INTO `k_startegy` VALUES ('西澳U20', '80', '3', '', '买大球');
INSERT INTO `k_startegy` VALUES ('美乙', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('哈萨甲', '80', '2', '', '>2.5买大球');
INSERT INTO `k_startegy` VALUES ('里约足联B', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('越VL', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('韩甲挑', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('智利乙', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('俄甲', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('南俱杯', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳昆士兰', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('西澳超', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳塔超', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳新联2', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳维超2', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳布甲', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('冰岛女甲', '80', '2', '买小球', '买大球');
INSERT INTO `k_startegy` VALUES ('墨女超', '80', '2', '买小球', '买大球');
INSERT INTO `k_startegy` VALUES ('印IFA盾', '80', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('日联杯', '75', '2', '', '买大球');
INSERT INTO `k_startegy` VALUES ('韩国女K', '80', '1', '', '买大球');
INSERT INTO `k_startegy` VALUES ('南澳女超', '80', '1', '', '买大球');
INSERT INTO `k_startegy` VALUES ('瑞典北甲', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('哈萨超', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('美职联', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('天皇杯', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('爱沙杯', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('菲足联', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳维女超', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('澳西甲', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('泰D3', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('奥地利杯', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('马来F杯', '80', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('南澳州联1', '75', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('英友谊', '75', '0', '', '买大球');
INSERT INTO `k_startegy` VALUES ('苏联杯', '75', '0', '买小球', '');
INSERT INTO `k_startegy` VALUES ('阿根廷杯', '75', '0', '买小球', '');
INSERT INTO `k_startegy` VALUES ('日职乙', '75', '0', '白名单', '白名单');
INSERT INTO `k_startegy` VALUES ('中甲', '75', '0', '白名单', '白名单');
INSERT INTO `k_startegy` VALUES ('泰超', '75', '0', '白名单', '白名单');
INSERT INTO `k_startegy` VALUES ('日职联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('墨秋联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳威北超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('南澳超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳新女', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('日女挑联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('欧洲友谊', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('日职丙', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('新加坡联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('奥地利A杯', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('捷U21', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('马来超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('丹超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('白俄后', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('泰乙', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('日足联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('赞比亚超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('巴圣SB', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('挪丙2', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('挪乙1', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('拉脱V', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('韩国K2', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('韩K联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('印尼超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('新加坡U19', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('瑞典超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('欧锦赛 U19', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('冰岛超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('厄瓜锦', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('欧罗巴', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('印尼杯', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('中超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('越V2联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('斐济杯', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('印尼L2', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('加尔联', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳维超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('巴西乙', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('智利甲', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳昆U20', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳布超后', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('中甲', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳洲特区超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('捷2L', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('澳亚布超', '75', '0', '', '');
INSERT INTO `k_startegy` VALUES ('马来总统杯', '75', '0', '', '');
