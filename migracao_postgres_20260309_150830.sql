-- Migração de dados SQLite para PostgreSQL
-- Gerado em: 2026-03-09 15:08:30


-- Tabela: anos_div
DELETE FROM anos_div;
INSERT INTO anos_div (id, ano) VALUES (1, 2026);
INSERT INTO anos_div (id, ano) VALUES (2, 2025);
INSERT INTO anos_div (id, ano) VALUES (3, 2024);
SELECT setval(pg_get_serial_sequence('anos_div', 'id'), COALESCE((SELECT MAX(id) FROM anos_div), 1));
