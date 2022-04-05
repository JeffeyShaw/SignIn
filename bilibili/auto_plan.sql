/*
 Navicat Premium Data Transfer

 Source Server         : 本地数据库
 Source Server Type    : MySQL
 Source Server Version : 80024
 Source Host           : 192.168.123.165:3306
 Source Schema         : auto_plan

 Target Server Type    : MySQL
 Target Server Version : 80024
 File Encoding         : 65001

 Date: 30/12/2021 22:22:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auto_bilibili
-- ----------------------------
DROP TABLE IF EXISTS `auto_bilibili`;
CREATE TABLE `auto_bilibili`
(
    `id`                         int                                                           NOT NULL AUTO_INCREMENT,
    `userid`                     int                                                           NOT NULL,
    `name`                       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '创建的任务名',
    `sessdata`                   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NOT NULL,
    `bili_jct`                   longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NOT NULL,
    `dedeuserid`                 longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NOT NULL,
    `taskIntervalTime`           int                                                           NOT NULL DEFAULT 10 COMMENT '任务之间的执行间隔',
    `numberOfCoins`              int                                                           NOT NULL DEFAULT 5 COMMENT '每日投币数量',
    `reserveCoins`               int                                                           NOT NULL DEFAULT 50 COMMENT '预留的硬币数',
    `selectLike`                 int                                                           NOT NULL DEFAULT 0 COMMENT '投币时是否点赞，默认 0, 0：否 1：是',
    `monthEndAutoCharge`         varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT 'true' COMMENT '年度大会员月底是否用 B 币券给自己充电，默认 true，即充电对象是你本人。',
    `giveGift`                   varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT 'true' COMMENT '直播送出即将过期的礼物，默认开启',
    `upLive`                     varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '直播送出即将过期的礼物，指定 up 主，为 0 时则随随机选取一个 up 主',
    `chargeForLove`              varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0' COMMENT '给指定 up 主充电，值为 0 或者充电对象的 uid，默认为 0，即给自己充电',
    `devicePlatform`             varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT 'ios' COMMENT '手机端漫画签到时的平台，建议选择你设备的平台 ，默认 ios',
    `coinAddPriority`            int                                                           NOT NULL DEFAULT 1 COMMENT '0：优先给热榜视频投币，1：优先给关注的 up 投币',
    `userAgent`                  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 Edg/86.0.622.69' COMMENT '浏览器 UA',
    `skipDailyTask`              varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT 'false' COMMENT '是否跳过每日任务',
    `webhook`                    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL     DEFAULT NULL COMMENT '推送地址',
    `enddate`                    datetime                                                      NULL     DEFAULT NULL,
    `match_enable`               varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL DEFAULT 'false' COMMENT '预测是否开启',
    `match_predictNumberOfCoins` int                                                           NOT NULL DEFAULT 10 COMMENT '单次预测投注硬币',
    `match_minimumNumberOfCoins` int                                                           NOT NULL DEFAULT 200 COMMENT '预测保留硬币',
    `match_showHandModel`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'false' COMMENT '押注形式',
    `other`                      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL     DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    INDEX `userid` (`userid`) USING BTREE,
    CONSTRAINT `auto_bilibili_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 7
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auto_bilibili
-- ----------------------------

-- ----------------------------
-- Table structure for auto_log
-- ----------------------------
DROP TABLE IF EXISTS `auto_log`;
CREATE TABLE `auto_log`
(
    `id`      bigint                                                        NOT NULL AUTO_INCREMENT,
    `auto_id` int                                                           NULL DEFAULT NULL,
    `name`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `type`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `status`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `userid`  int                                                           NULL DEFAULT NULL,
    `date`    datetime                                                      NULL DEFAULT CURRENT_TIMESTAMP,
    `text`    longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NULL,
    `other`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    INDEX `userid` (`userid`) USING BTREE,
    CONSTRAINT `auto_log_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 114
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auto_log
-- ----------------------------

-- ----------------------------
-- Table structure for auto_mihayou
-- ----------------------------
DROP TABLE IF EXISTS `auto_mihayou`;
CREATE TABLE `auto_mihayou`
(
    `id`          int                                                           NOT NULL AUTO_INCREMENT,
    `name`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `cookie`      longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NULL,
    `suid`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `stoken`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `other_key`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `user_id`     int                                                           NULL DEFAULT NULL,
    `genshin_uid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `server`      varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NULL DEFAULT 'cn_gf01',
    `mi_name`     varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `enable`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT 'true',
    `status`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '100',
    `endate`      datetime                                                      NULL DEFAULT NULL,
    `webhook`     varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `other`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `suid` (`suid`) USING BTREE,
    INDEX `user_id` (`user_id`) USING BTREE,
    CONSTRAINT `auto_mihayou_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 13
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auto_mihayou
-- ----------------------------

-- ----------------------------
-- Table structure for auto_netmusic
-- ----------------------------
DROP TABLE IF EXISTS `auto_netmusic`;
CREATE TABLE `auto_netmusic`
(
    `id`                   int                                                           NOT NULL AUTO_INCREMENT,
    `phone`                varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '登录手机号',
    `password`             varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NOT NULL COMMENT '登录密码md5',
    `countrycode`          varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NULL DEFAULT '86' COMMENT '手机号国家代码',
    `userid`               int                                                           NULL DEFAULT NULL COMMENT '外键约束user_id',
    `netmusic_id`          varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '网易云id',
    `netmusic_name`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '网易云昵称',
    `netmusic_level`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '网易云等级',
    `netmusic_need_day`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '升级所需天数',
    `netmusic_need_listen` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '升级所需听歌数',
    `name`                 varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务名',
    `cookie`               longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NULL COMMENT '登录cookie',
    `status`               varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '100',
    `enable`               varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NULL DEFAULT 'true',
    `enddate`              datetime                                                      NULL DEFAULT NULL,
    `webhook`              varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `other`                varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `netmusic_id` (`netmusic_id`) USING BTREE,
    INDEX `userid` (`userid`) USING BTREE,
    CONSTRAINT `auto_netmusic_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 4
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auto_netmusic
-- ----------------------------

-- ----------------------------
-- Table structure for bili_user
-- ----------------------------
DROP TABLE IF EXISTS `bili_user`;
CREATE TABLE `bili_user`
(
    `id`           int                                                           NOT NULL AUTO_INCREMENT,
    `auto_id`      int                                                           NULL DEFAULT NULL,
    `uid`          bigint                                                        NULL DEFAULT NULL,
    `bili_name`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `bili_coin`    decimal(10, 2)                                                NULL DEFAULT NULL,
    `bili_exp`     bigint                                                        NULL DEFAULT NULL,
    `bili_upexp`   bigint                                                        NULL DEFAULT NULL,
    `bili_level`   int                                                           NULL DEFAULT NULL,
    `face_img`     longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci     NULL,
    `is_vip`       varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci  NULL DEFAULT NULL,
    `vip_due_date` datetime                                                      NULL DEFAULT NULL,
    `status`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '100',
    `enddate`      datetime                                                      NULL DEFAULT NULL,
    `other`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `uid` (`uid`) USING BTREE,
    INDEX `auto_id` (`auto_id`) USING BTREE,
    CONSTRAINT `bili_user_ibfk_1` FOREIGN KEY (`auto_id`) REFERENCES `auto_bilibili` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 7
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of bili_user
-- ----------------------------

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`
(
    `id`   int                                                           NOT NULL AUTO_INCREMENT,
    `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 3
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role`
VALUES (1, 'ROLE_ADMIN');
INSERT INTO `sys_role`
VALUES (2, 'ROLE_USER');

-- ----------------------------
-- Table structure for sys_role_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_user`;
CREATE TABLE `sys_role_user`
(
    `id`          int NOT NULL AUTO_INCREMENT,
    `sys_user_id` int NULL DEFAULT NULL,
    `sys_role_id` int NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `sys_user_id` (`sys_user_id`) USING BTREE,
    INDEX `sys_role_id` (`sys_role_id`) USING BTREE,
    CONSTRAINT `sys_role_user_ibfk_1` FOREIGN KEY (`sys_user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT `sys_role_user_ibfk_2` FOREIGN KEY (`sys_role_id`) REFERENCES `sys_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 7
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_role_user
-- ----------------------------

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`
(
    `id`       int                                                           NOT NULL AUTO_INCREMENT,
    `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `status`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `regdate`  datetime                                                      NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `username` (`username`) USING BTREE
) ENGINE = InnoDB
  AUTO_INCREMENT = 15
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_user
-- ----------------------------

-- ----------------------------
-- Table structure for sys_user_info
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_info`;
CREATE TABLE `sys_user_info`
(
    `id`      int                                                           NOT NULL AUTO_INCREMENT,
    `user_id` int                                                           NOT NULL,
    `webhook` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    `other`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    UNIQUE INDEX `user_id` (`user_id`) USING BTREE,
    CONSTRAINT `sys_user_info_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB
  AUTO_INCREMENT = 3
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_user_info
-- ----------------------------

-- ----------------------------
-- Table structure for t_sys_quartz_job
-- ----------------------------
DROP TABLE IF EXISTS `t_sys_quartz_job`;
CREATE TABLE `t_sys_quartz_job`
(
    `id`              varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '日志id',
    `job_name`        varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务名称',
    `job_group`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务组名',
    `invoke_target`   varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '调用目标字符串',
    `cron_expression` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'cron执行表达式',
    `misfire_policy`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'cron计划策略',
    `concurrent`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '是否并发执行（0允许 1禁止）',
    `status`          int                                                           NULL DEFAULT NULL COMMENT '任务状态（0正常 1暂停）',
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT = '定时任务调度表'
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_sys_quartz_job
-- ----------------------------
INSERT INTO `t_sys_quartz_job`
VALUES ('590854946858078208', 'b站自动任务', 'DEFAULT', 'biliTask.doAutoCheck()', '0 0 8 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('590884423877136384', 'b站定时重置任务标识', 'DEFAULT', 'biliTask.resetStatus()', '0 0 0 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('591255386712051712', '网易云自动任务', 'DEFAULT', 'netTask.doAutoCheck()', '0 0 8 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('591479208484671488', '网易云定时重置任务状态', 'DEFAULT', 'netTask.resetStatus()', '0 0 0 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('591479486176956416', '网易云定时刷新用户信息', 'DEFAULT', 'netTask.refreshUserInfo()', '0 0 12 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('592293890904690688', '米游社自动任务', 'DEFAULT', 'mihuyouTask.doAutoCheck()', '0 0 8 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('592295794938351616', '米游社自动重置任务状态', 'DEFAULT', 'mihuyouTask.resetStatus()', '0 0 0 * * ? *', '3', '1', 0);
INSERT INTO `t_sys_quartz_job`
VALUES ('592295794938351617', '米游社更新个人信息', 'DEFAULT', 'mihuyouTask.updateAvatar()', '0 15 0 ? * MON', '3', '1', 0);


-- ----------------------------
-- Table structure for t_sys_quartz_job_log
-- ----------------------------
DROP TABLE IF EXISTS `t_sys_quartz_job_log`;
CREATE TABLE `t_sys_quartz_job_log`
(
    `id`             varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '主键',
    `job_name`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务名称',
    `job_group`      varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务组名',
    `invoke_target`  varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '调用目标字符串',
    `job_message`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '日志信息',
    `status`         int                                                           NULL DEFAULT NULL COMMENT '执行状态（0正常 1失败）',
    `exception_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '异常信息',
    `start_time`     datetime                                                      NULL DEFAULT NULL COMMENT '开始时间',
    `end_time`       datetime                                                      NULL DEFAULT NULL COMMENT '结束时间',
    PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT = '定时任务调度日志表'
  ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of t_sys_quartz_job_log
-- ----------------------------

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`  (
                               `id` int NOT NULL AUTO_INCREMENT,
                               `value` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT 'value',
                               `bond` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'key',
                               PRIMARY KEY (`id`) USING BTREE,
                               UNIQUE INDEX `INDEX_UNIQUE_bond`(`bond`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_config
-- ----------------------------
INSERT INTO `sys_config` VALUES (1, '<p class=\"red\">警告！！</p>\r\n<p>1.3版本的更新重构了推送部分的代码，之前设置的推送地址会全部失效</p>\r\n<p>目前推送部分代码为json字符串形式传入</p>\r\n<p>\r\n在填写webhook的页面中已经给出了\r\n<a style=\"color: blue\" lay-href=\"/webhook-generate\">生成器</a>\r\n按钮\r\n</p>\r\n<p>\r\n请使用\r\n<a style=\"color: blue\" lay-href=\"/webhook-generate\">生成器</a>\r\n生成之后复制到webhook一栏更新配置！！\r\n</p>', 'system_notice_content');


SET FOREIGN_KEY_CHECKS = 1;
