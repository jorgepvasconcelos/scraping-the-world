SCHEMA_DDL = """
create table if not exists planets
(
	id_planet int auto_increment
		primary key,
	name varchar(45) null,
	climate varchar(45) null,
	terrain varchar(45) null
)
charset=utf8mb4;



"""
