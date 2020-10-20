-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema quote_dash_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema quote_dash_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `quote_dash_db` DEFAULT CHARACTER SET utf8 ;
USE `quote_dash_db` ;

-- -----------------------------------------------------
-- Table `quote_dash_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quote_dash_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quote_dash_db`.`quotes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `quote_dash_db`.`quotes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `author` VARCHAR(255) NULL,
  `quote` TEXT(1000) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_quotes_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_quotes_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `quote_dash_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
