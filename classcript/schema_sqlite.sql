CREATE TABLE `notes` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `created` TIMESTAMP NOT NULL DEFAULT (strftime('%m-%d-%Y', 'now', 'localtime')),
  `updated` TIMESTAMP NOT NULL DEFAULT (strftime('%m-%d-%Y', 'now', 'localtime')),
  `note_title` VARCHAR(255),
  `note` TEXT,
  `note_markdown` TEXT,
  `user_id` INTEGER,
  FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TRIGGER `triggerDate` AFTER UPDATE ON `notes`
BEGIN
   update `notes` SET `updated` = (strftime('%m-%d-%Y', 'now', 'localtime')) WHERE id = NEW.id;
END;

CREATE TABLE `users` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `registered_at` TIMESTAMP NOT NULL DEFAULT (strftime('%m-%d-%Y', 'now', 'localtime')),
  `last_login` TIMESTAMP NOT NULL DEFAULT (strftime('%m-%d-%Y', 'now', 'localtime')),
  `username` VARCHAR(255),
  `password` VARCHAR(200),
  `email` VARCHAR(200)
);

CREATE TRIGGER `triggerUserLogin` AFTER UPDATE ON `users`
BEGIN
   update `users` SET `last_login` = (strftime('%m-%d-%Y', 'now', 'localtime')) WHERE id = NEW.id;
END;
