/* remove not null constraint from password column in table fats */
alter table fats alter column password drop not null;