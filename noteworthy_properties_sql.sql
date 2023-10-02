-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema noteworthy_properties_schema
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `noteworthy_properties_schema` ;

-- -----------------------------------------------------
-- Schema noteworthy_properties_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `noteworthy_properties_schema` DEFAULT CHARACTER SET utf8 ;
USE `noteworthy_properties_schema` ;

-- -----------------------------------------------------
-- Table `noteworthy_properties_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `noteworthy_properties_schema`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `noteworthy_properties_schema`.`buyers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `noteworthy_properties_schema`.`buyers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `status` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_buyers_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_buyers_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `noteworthy_properties_schema`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `noteworthy_properties_schema`.`addresses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `noteworthy_properties_schema`.`addresses` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `street` VARCHAR(255) NOT NULL,
  `city` VARCHAR(255) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  `zipcode` VARCHAR(10) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `buyer_id` INT NOT NULL,
  `buyer_user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_addresses_buyers1_idx` (`buyer_id` ASC, `buyer_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_addresses_buyers1`
    FOREIGN KEY (`buyer_id` , `buyer_user_id`)
    REFERENCES `noteworthy_properties_schema`.`buyers` (`id` , `user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `noteworthy_properties_schema`.`properties`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `noteworthy_properties_schema`.`properties` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(255) NOT NULL,
  `client_ranking` INT NOT NULL,
  `property_type` VARCHAR(255) NOT NULL,
  `year_constructed` INT NOT NULL,
  `list_price` INT NOT NULL,
  `positives` TEXT NOT NULL,
  `negatives` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT NOW(),
  `updated_at` DATETIME NOT NULL DEFAULT NOW() ON UPDATE NOW(),
  `address_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_properties_addresses1_idx` (`address_id` ASC) VISIBLE,
  CONSTRAINT `fk_properties_addresses1`
    FOREIGN KEY (`address_id`)
    REFERENCES `noteworthy_properties_schema`.`addresses` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
