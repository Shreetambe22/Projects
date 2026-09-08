SELECT * 
FROM layoffs;

create table world_layoff_staging 
like layoffs;

Insert into world_layoff_staging 
select *
from layoffs;
SELECT * 
FROM world_layoff_staging;

SELECT *
FROM world_layoff_staging
;

SELECT company, industry, total_laid_off,`date`,
		ROW_NUMBER() OVER (
			PARTITION BY company, industry, total_laid_off,`date`) AS row_num
	FROM 
       world_layoff_staging
       
SELECT *
from world_layoff_staging ;


SELECT *
FROM (
	SELECT company, location, industry, total_laid_off,percentage_laid_off,`date`, stage, country, funds_raised_millions,
		ROW_NUMBER() OVER (
			PARTITION BY company, location, industry, total_laid_off,percentage_laid_off,`date`, stage, country, funds_raised_millions
			) AS row_num
	FROM 
		world_layoffs.layoffs_staging
) duplicates
WHERE 
	row_num > 1;


CREATE TABLE `world_layoffs`.`layoffs_staging2` (
`company` text,
`location`text,
`industry`text,
`total_laid_off` INT,
`percentage_laid_off` text,
`date` text,
`stage`text,
`country` text,
`funds_raised_millions` int,
row_num INT
);

INSERT INTO `world_layoffs`.`layoffs_staging2`
(`company`,
`location`,
`industry`,
`total_laid_off`,
`percentage_laid_off`,
`date`,
`stage`,
`country`,
`funds_raised_millions`,
`row_num`)
SELECT `company`,
`location`,
`industry`,
`total_laid_off`,
`percentage_laid_off`,
`date`,
`stage`,
`country`,
`funds_raised_millions`,
		ROW_NUMBER() OVER (
			PARTITION BY company, location, industry, total_laid_off,percentage_laid_off,`date`, stage, country, funds_raised_millions
			) AS row_num
	FROM 
		world_layoffs.layoffs_staging;
        
        
select * 
from layoffs_staging2 ;

DELETE FROM world_layoffs.layoffs_staging2
WHERE row_num >= 2;

select * from world_layoffs.layoffs_staging2
WHERE row_num >= 2;


-- Standarzing Data --

select distinct Company  
from layoffs_staging2 ;

update layoffs_staging2 
set company = Trim(Company );

SELECT distinct Industry
From layoffs_staging2 
order by 1 ;

select * 
From layoffs_staging2 
where Industry like 'Crypto%'; 

Update layoffs_staging2 
set Industry = 'Crypto'
where Industry like 'Crypto%';

select distinct Industry
from layoffs_staging2 
order by 1;

select distinct Country , TRIM(TRAILING '.' FROM Country)
From layoffs_staging2 
order by 1;

update layoffs_staging2 
set country = TRIM(TRAILING '.' FROM Country)
where Country like 'United States%';

SELECT `Date`
FROM layoffs_staging2;

update layoffs_staging2
set `Date`= STR_TO_DATE(`Date`, '%m/%d/%Y');

Alter table layoffs_staging2
modify column `Date` DATE ; 

SELECT *
FROM layoffs_staging2
WHERE total_laid_off IS NULL
  AND percentage_laid_off IS NULL;
  
Delete
FROM layoffs_staging2
WHERE total_laid_off IS NULL
  AND percentage_laid_off IS NULL;
  
ALTER TABLE layoffs_staging2
DROP COLUMN row_num;


SELECT * 
FROM world_layoffs.layoffs_staging2;
