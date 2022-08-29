CREATE TABLE `moove`.`vehicle` (
  `geotab_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `license_plate` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`geotab_id`),
  UNIQUE INDEX `geotab_id_UNIQUE` (`geotab_id` ASC) VISIBLE,
  UNIQUE INDEX `license_plate_UNIQUE` (`license_plate` ASC) VISIBLE);




CREATE TABLE `moove`.`trips` (
  `id` VARCHAR(45) NOT NULL,
  `geotab_id_trip` VARCHAR(45) NOT NULL,
  `start` VARCHAR(45) NOT NULL,
  `stop` VARCHAR(45) NOT NULL,
  `distance` VARCHAR(45) NOT NULL,
  `maxspeed` VARCHAR(45) NOT NULL,
  `driver_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `geotab_id_idx` (`geotab_id_trip` ASC) VISIBLE,
  CONSTRAINT `geotab_id_trip`
    FOREIGN KEY (`geotab_id_trip`)
    REFERENCES `moove`.`vehicle` (`geotab_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);


CREATE TABLE `moove`.`driving_exceptions` (
  `id` VARCHAR(60) NOT NULL,
  `rule_id` VARCHAR(50) NOT NULL,
  `geotab_id_exptn` VARCHAR(45) NOT NULL,
  `active_from` TIMESTAMP(3) NOT NULL,
  `active_to` TIMESTAMP(3) NOT NULL,
  `duration` TIME NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `geotab_id_idx` (`geotab_id_exptn` ASC) VISIBLE,
  CONSTRAINT `geotab_id_exptn`
    FOREIGN KEY (`geotab_id_exptn`)
    REFERENCES `moove`.`vehicle` (`geotab_id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT);
