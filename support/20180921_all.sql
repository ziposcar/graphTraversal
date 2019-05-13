DROP TABLE IF EXISTS cms_article
CREATE TABLE `cms_article` (  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '文章ID',  `cid` int(11) NOT NULL COMMENT '所属栏目ID',  `title` varchar(200) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '标题',  `subtitle` varchar(200) COLLATE utf8_unicode_ci DEFAULT '',  `att` set('a','b','c','d','e','f','g') COLLATE utf8_unicode_ci DEFAULT '' COMMENT '属性',  `pic` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '缩略图',  `source` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '来源',  `author` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '作者',  `resume` varchar(500) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '摘要',  `pubdate` varchar(40) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '发表日期',  `content` text COLLATE utf8_unicode_ci COMMENT '文章内容',  `hits` int(11) NOT NULL DEFAULT '0' COMMENT '点击次数',  `created_by` int(11) NOT NULL COMMENT '创建者',  `created_date` datetime NOT NULL COMMENT '创建时间',  `delete_session_id` int(11) DEFAULT NULL COMMENT '删除人ID',  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
INSERT INTO cms_article VALUES('1','1','AACMS V0.1发布','','','','http://www.phpaa.cn','phpaa','phpaaCMS 	\r\n','2009-04-02 10:32:31','<p>AACMS是一个非常简单易用的内容管理系统，适合做一些功能简单的站点！</p>\r\n<p>现在发布的是第一个版本，可能有些很多地方不是很稳定，欢迎大家提出修改意见。</p>','0','1','2009-04-02 10:32:31','0')
INSERT INTO cms_article VALUES('2','1','AACMS V0.1.1发布','','','data/attachment/image/thumbnails/200906/2009060209121790.gif','http://www.phpaa.cn','phpaa','系统更新','2009-06-02 09:12:17','<p>系统更新</p>\r\n<p>将系统中的短标记全部改成php5中默认的php标准标记</p>\r\n<p>修正点击用户名，不能修改的bug</p>\r\n<p>系统增加一个简单的说明文件,根目录 《说明.txt》</p>\r\n<p>调整部分页面</p>\r\n<p>&nbsp;</p>','0','1','2009-06-02 09:12:17','0')
INSERT INTO cms_article VALUES('12','16','测试数据2','','','','','',' ','2009-04-09 01:01:25','<p>afsafa</p>','0','1','2009-04-09 01:01:25','0')
INSERT INTO cms_article VALUES('9','16','测试数据1','','','','','',' ','2009-04-04 00:45:00','','0','1','2009-04-04 00:45:00','0')
INSERT INTO cms_article VALUES('13','16','测试数据3','','','','','',' ','2009-04-09 01:12:43','<p>afdsfdsa</p>','0','1','2009-04-09 01:12:43','0')
INSERT INTO cms_article VALUES('14','16','测试数据4','','','data/attachment/image/thumbnails/200904/2009040911140798.jpg','','',' ','2009-04-09 11:14:12','<p><img height=\"421\" alt=\"\" width=\"337\" src=\"/liuenyi/AACMS/data/attachment/image/0904090232343125039jnid20ffnmi.jpg\" /></p>','0','1','2009-04-09 11:14:12','0')
INSERT INTO cms_article VALUES('15','16','测试数据5','','','','','',' ','2009-04-09 11:15:09','','0','1','2009-04-09 11:15:09','0')
INSERT INTO cms_article VALUES('16','16','测试数据6','','a,b,d','data/attachment/image/thumbnails/200904/2009040911202864.jpg','','',' ','2009-04-15 09:37:26','<p>sss</p>','0','1','2009-04-15 09:37:26','0')
INSERT INTO cms_article VALUES('17','16','测试数据7','','b,d,f','','','',' ','2009-04-15 09:38:02','<p>fsd</p>','0','1','2009-04-15 09:38:02','0')
INSERT INTO cms_article VALUES('18','16','测试数据8','sddsafds','b','data/attachment/image/thumbnails/200904/2009041509383862.jpg','dss','ffff','sfddsaffsad','2009-04-15 10:06:27','<p>sadfdsadsaf<img height=\"421\" alt=\"\" width=\"337\" src=\"/liuenyi/phpaaCMS/data/attachment/image/0904090232343125039jnid20ffnmi.jpg\" /></p>','0','1','2009-04-15 10:06:27','0')
INSERT INTO cms_article VALUES('19','16','测试数据9','副标题发生的的','a,d','data/attachment/image/thumbnails/200904/2009042022273733.gif','出处','作者','摘要','2009-04-20 22:27:54','<p>阿方索高盛公司</p>','0','1','2009-04-20 22:27:54','0')
INSERT INTO cms_article VALUES('20','16','测试数据10','','','','','','','2009-04-20 22:28:19','<p>我热惹我</p>','0','1','2009-04-20 22:28:19','0')
INSERT INTO cms_article VALUES('21','16','测试数据11','','','','','','','2009-04-20 22:28:32','','0','1','2009-04-20 22:28:32','0')
INSERT INTO cms_article VALUES('22','16','测试数据12','','','','','','','2009-04-20 22:28:39','','0','1','2009-04-20 22:28:39','0')
INSERT INTO cms_article VALUES('23','16','测试数据13','','','','','','','2009-04-20 22:28:49','','0','1','2009-04-20 22:28:49','0')
INSERT INTO cms_article VALUES('24','16','测试数据14','','','','','','','2009-04-20 22:29:34','','0','1','2009-04-20 22:29:34','0')
INSERT INTO cms_article VALUES('25','16','测试数据15','','','','','','','2009-04-20 22:29:51','','0','1','2009-04-20 22:29:51','0')
INSERT INTO cms_article VALUES('26','16','测试数据16','','','','','','','2009-04-20 22:29:54','','0','1','2009-04-20 22:29:54','0')
INSERT INTO cms_article VALUES('27','16','测试数据17','','','','','','','2009-04-20 22:29:58','','0','1','2009-04-20 22:29:58','0')
INSERT INTO cms_article VALUES('28','16','测试数据18','','','','','','','2009-04-20 22:30:03','','0','1','2009-04-20 22:30:03','0')
INSERT INTO cms_article VALUES('29','16','测试数据19','','','data/attachment/200906/20090604120007_69.jpg','','','','2009-06-04 12:00:07','','0','1','2009-06-04 12:00:07','0')
INSERT INTO cms_article VALUES('30','16','测试数据20','','','data/attachment/200906/20090604131438_69.gif','','','','2009-06-04 13:14:38','','0','1','2009-06-04 13:14:38','0')
INSERT INTO cms_article VALUES('31','1','phpAA文章管理系统V0.3 UTF-8 发布','','','','','','','2009-06-04 14:24:03','<p><span style=\"font-size: x-large\"><span><span><strong>新增加功能</strong></span></span></span></p>\r\n<p>页面管理</p>\r\n<p>文件管理</p>','0','1','2009-06-04 14:24:03','0')
INSERT INTO cms_article VALUES('32','16','123','','b','','111','','','2018-09-18 17:11:23','','0','0','2018-09-18 17:11:23','0')
INSERT INTO cms_article VALUES('33','16','13334','gfgf','a,b','data/attachment/201809/20180918171307_16.png','gff','gggg','gggg','2018-09-18 17:13:07','','0','0','2018-09-18 17:13:07','0')
INSERT INTO cms_article VALUES('34','1','1234','','','','1324','','','2018-09-18 18:34:14','','0','0','2018-09-18 18:34:14','0')
INSERT INTO cms_article VALUES('35','1','y','y','d','','y','y','y','2018-09-18 18:49:18','','0','0','2018-09-18 18:49:18','0')
INSERT INTO cms_article VALUES('36','1','20Ch59','EqaXMJ','','data/attachment/201809/20180921193021_53.png','6xWe1H','4OQtYs','MQDD6T','2018-09-21 19:30:21','','0','0','2018-09-21 19:30:21','')
INSERT INTO cms_article VALUES('37','1','20Ch59','EqaXMJ','','data/attachment/201809/20180921193538_48.png','6xWe1H','4OQtYs','MQDD6T','2018-09-21 19:35:38','','0','0','2018-09-21 19:35:38','')
INSERT INTO cms_article VALUES('38','1','pAoNWy','dEL70i','','data/attachment/201809/20180921193543_12.png','hJ5i7H','8f3Or2','832NaK','2018-09-21 19:35:43','','0','0','2018-09-21 19:35:43','')
INSERT INTO cms_article VALUES('39','1','20Ch59','EqaXMJ','','data/attachment/201809/20180921194321_22.png','6xWe1H','4OQtYs','MQDD6T','2018-09-21 19:43:21','','0','0','2018-09-21 19:43:21','')
INSERT INTO cms_article VALUES('40','1','pAoNWy','dEL70i','','data/attachment/201809/20180921194325_94.png','hJ5i7H','8f3Or2','832NaK','2018-09-21 19:43:25','','0','0','2018-09-21 19:43:25','')
DROP TABLE IF EXISTS cms_category
CREATE TABLE `cms_category` (  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '栏目ID',  `pid` int(11) NOT NULL DEFAULT '0' COMMENT '父栏目ID',  `name` varchar(50) COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '栏目名称',  `description` text COLLATE utf8_unicode_ci,  `seq` int(11) NOT NULL DEFAULT '0' COMMENT '栏目排序',  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
INSERT INTO cms_category VALUES('1','0','最新动态','','0')
INSERT INTO cms_category VALUES('16','0','科技新闻','','0')
INSERT INTO cms_category VALUES('23','1','456','','6')
DROP TABLE IF EXISTS cms_file
CREATE TABLE `cms_file` (  `id` int(11) NOT NULL AUTO_INCREMENT,  `filename` varchar(200) DEFAULT NULL,  `ffilename` varchar(200) DEFAULT NULL,  `path` varchar(250) DEFAULT NULL,  `ext` varchar(10) DEFAULT NULL,  `size` int(11) DEFAULT NULL,  `upload_date` datetime DEFAULT NULL,  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8
INSERT INTO cms_file VALUES('1','20180921193021_53.png','888.png','data/attachment/201809/20180921193021_53.png','png','65417','2018-09-21 19:30:21')
INSERT INTO cms_file VALUES('2','20180921193538_48.png','888.png','data/attachment/201809/20180921193538_48.png','png','65417','2018-09-21 19:35:38')
INSERT INTO cms_file VALUES('3','20180921193543_12.png','888.png','data/attachment/201809/20180921193543_12.png','png','65417','2018-09-21 19:35:43')
INSERT INTO cms_file VALUES('4','20180921194321_22.png','888.png','data/attachment/201809/20180921194321_22.png','png','65417','2018-09-21 19:43:21')
INSERT INTO cms_file VALUES('5','20180921194325_94.png','888.png','data/attachment/201809/20180921194325_94.png','png','65417','2018-09-21 19:43:25')
DROP TABLE IF EXISTS cms_friendlink
CREATE TABLE `cms_friendlink` (  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',  `name` varchar(200) NOT NULL COMMENT '网站名称',  `url` varchar(200) NOT NULL COMMENT '网址',  `description` varchar(400) NOT NULL COMMENT '站点简介',  `logo` varchar(200) NOT NULL COMMENT '网站LOGO',  `seq` int(11) NOT NULL DEFAULT '0' COMMENT '排列顺序',  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8
INSERT INTO cms_friendlink VALUES('1','PHPAA.CN','http://www.phpaa.cn','AACMS 文章管理系统','http://localhost:9090/liuenyi/phpAA_CMS/images/logo.gif','0')
INSERT INTO cms_friendlink VALUES('3','phpChina','http://www.phpchina.com','','','0')
DROP TABLE IF EXISTS cms_message
CREATE TABLE `cms_message` (  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',  `title` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '标题',  `name` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '称呼',  `qq` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'QQ',  `email` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'Email or MSN',  `content` text COLLATE utf8_unicode_ci COMMENT '内容',  `reply` text COLLATE utf8_unicode_ci COMMENT '回复',  `ip` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '留言人IP',  `validate` int(11) DEFAULT '0' COMMENT '0为验证 1已验证',  `created_date` datetime DEFAULT NULL COMMENT '留言日期',  `reply_date` datetime DEFAULT NULL COMMENT '回复日期',  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci
INSERT INTO cms_message VALUES('14','这个系统免费吗？','phper','9999999','phpaa.cn@gmail.com','这个系统可以免费使用吗？','可以，系统是开源的，可以任意使用，但不可以重新发布.gfgfgdgdfggsdgfsdgsg','127.0.0.1','1','2009-05-15 00:26:53','0000-00-00 00:00:00')
DROP TABLE IF EXISTS cms_notice
CREATE TABLE `cms_notice` (  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',  `title` varchar(200) NOT NULL COMMENT '公告标题',  `content` text NOT NULL COMMENT '公告内容',  `state` int(11) NOT NULL DEFAULT '0' COMMENT '状态（0 发布 1 禁用）',  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8
INSERT INTO cms_notice VALUES('6','phpaa 0.1版本发布','非常简易的文章管理系统，适合建立一些功能要求不高的公司、企业、政府网站','0')
INSERT INTO cms_notice VALUES('9','phpaa 0.2 版本发布','更换了网站后台皮肤，修改部分bug','0')
INSERT INTO cms_notice VALUES('10','add','aaa','0')
DROP TABLE IF EXISTS cms_page
CREATE TABLE `cms_page` (  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',  `code` varchar(20) DEFAULT NULL COMMENT '别名',  `title` varchar(100) DEFAULT NULL COMMENT '名称',  `content` text COMMENT '内容',  `created_date` datetime DEFAULT NULL COMMENT '创建日期',  PRIMARY KEY (`id`)) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8
INSERT INTO cms_page VALUES('2','contact','联系方式','<p>QQ：176759617 <br />\r\n邮箱： phpaa.cn@gmail.com <br />\r\n网址：<a class=\"hui12\" href=\"#\">http://www.phpaa.cn</a></p>','2009-05-15 11:47:21')
INSERT INTO cms_page VALUES('3','introduce','网站介绍','<p>一个简易的开源的文章管理系统</p>','2009-05-15 23:50:13')
DROP TABLE IF EXISTS cms_users
CREATE TABLE `cms_users` (  `userid` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',  `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '用户名',  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '' COMMENT '密码',  PRIMARY KEY (`userid`)) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=utf8
INSERT INTO cms_users VALUES('1','admin','21232f297a57a5a743894a0e4a801fc3')
INSERT INTO cms_users VALUES('28','r','0cc175b9c0f1b6a831c399e269772661')
INSERT INTO cms_users VALUES('29','1','c4ca4238a0b923820dcc509a6f75849b')
