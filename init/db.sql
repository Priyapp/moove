CREATE TABLE `moove`.`vehicle` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `license_plate` VARCHAR(45) NOT NULL,
  `geotab_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `license_plate_UNIQUE` (`license_plate` ASC) VISIBLE);

INSERT INTO `moove`.`vehicle` (`name`, `license_plate`, `geotab_id`) VALUES ('Renault Twingo', 'JL-433-K', 'b8');
INSERT INTO `moove`.`vehicle` (`name`, `license_plate`, `geotab_id`) VALUES ('Volvo XC60', 'KS476X', 'b25');


CREATE TABLE `moove`.`trips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `vehicle_id` INT NOT NULL,
  `start` TIMESTAMP(3) NOT NULL,
  `stop` TIMESTAMP(3) NOT NULL,
  `distance` VARCHAR(45) NOT NULL,
  `maxspeed` VARCHAR(45) NOT NULL,
  `driver_id` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `id_idx` (`vehicle_id` ASC) VISIBLE,
  CONSTRAINT `id`
    FOREIGN KEY (`vehicle_id`)
    REFERENCES `moove`.`vehicle` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);



CREATE TABLE `moove`.`driving_exceptions1` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `rule_id` VARCHAR(50) NOT NULL,
  `trip_id` INT NOT NULL,
   `active_from` TIMESTAMP(3) NOT NULL,
  `active_to` TIMESTAMP(3) NOT NULL,
  `duration` TIME(7) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `trip_id_idx` (`trip_id` ASC) VISIBLE,
  CONSTRAINT `trip_id`
    FOREIGN KEY (`trip_id`)
    REFERENCES `moove`.`trips` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
