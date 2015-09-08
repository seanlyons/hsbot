USE seandb;

CREATE TABLE IF NOT EXISTS `cards_trie` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `word1` VARCHAR(30) DEFAULT "",
    `word2` VARCHAR(30) DEFAULT "",
    `word3` VARCHAR(30) DEFAULT "",
    `word4` VARCHAR(30) DEFAULT "",
    `url` VARCHAR(100),
    `disabled` TINYINT DEFAULT 0,
    PRIMARY KEY `id` (`id`),
    UNIQUE `name` (`word1`, `word2`, `word3`, `word4`)
) ENGINE=InnoDB;

/*
    * the bot will not post info for the same card twice in the same thread
*/
CREATE TABLE IF NOT EXISTS `threads` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `thread_id` VARCHAR(10) DEFAULT "",
    `card_ids_json` VARCHAR(4000) DEFAULT "",
    `last_update` INT(11),
    `url` VARCHAR(100),
    PRIMARY KEY `id` (`id`),
    KEY `thread_id` (`thread_id`)
) ENGINE=InnoDB;

/*
    * the bot will not examine the same post twice, regardless of whether it posted on it or not.
*/

CREATE TABLE IF NOT EXISTS `posts` (
    `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    `thread_id` VARCHAR(10) DEFAULT "",
    `post_id` VARCHAR(10) DEFAULT "",
    `last_update` INT(11),
    PRIMARY KEY `id` (`id`),
    KEY `thread_id` (`thread_id`),
    KEY `post_id` (`post_id`)
) ENGINE=InnoDB;