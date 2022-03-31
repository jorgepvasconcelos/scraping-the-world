SCHEMA_DDL = """
create table if not exists configs
(
	id int auto_increment
		primary key,
	name varchar(50) null,
	value varchar(50) null
);

|

create table if not exists logs
(
	id int auto_increment
		primary key,
	log_text text null,
	log_type varchar(50) null,
	log_date datetime default current_timestamp() null
);

|

create table if not exists sites_data
(
	id int auto_increment
		primary key,
	titulo text null,
	preco varchar(50) null,
	imagem text null,
	descricao text null,
	url_recebida text null,
	data_verificado datetime default current_timestamp() null,
	url_site text null
);
"""
