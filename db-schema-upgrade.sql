ALTER TABLE `deploys`
  ADD COLUMN `package_name` varchar(200) DEFAULT NULL COMMENT '更新包文件' AFTER `updated_at`,
  ADD COLUMN `deploy_status` int(11) NOT NULL DEFAULT '0' COMMENT ' 0 -uploaded, 1 - pushed, 2 - rollbacked, 99 - cancelled' AFTER `updated_at`,
  ADD COLUMN `package_path` varchar(200) DEFAULT NULL AFTER `updated_at`;

ALTER TABLE `projects`
  ADD COLUMN `prefix` varchar(50) DEFAULT NULL COMMENT '项目文件前缀名字' AFTER `name`,
  ADD COLUMN `status` int(11) NOT NULL DEFAULT '0' COMMENT '0' AFTER `name`;