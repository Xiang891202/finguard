INSERT INTO genetic_markers (id, marker_code, marker_name, related_diseases, related_body_parts, risk_level_high, display_order) VALUES
(gen_random_uuid()::text, 'BRCA1', 'BRCA1 基因', '["乳癌","卵巢癌"]'::jsonb, '["reproductive"]'::jsonb, 3.0, 1),
(gen_random_uuid()::text, 'BRCA2', 'BRCA2 基因', '["乳癌","卵巢癌","胰臟癌"]'::jsonb, '["reproductive"]'::jsonb, 3.0, 2),
(gen_random_uuid()::text, 'APOE', 'APOE 基因', '["阿茲海默症"]'::jsonb, '["brain"]'::jsonb, 2.5, 3),
(gen_random_uuid()::text, 'LDLR', 'LDLR 基因', '["家族性高膽固醇","心血管疾病"]'::jsonb, '["heart"]'::jsonb, 2.0, 4),
(gen_random_uuid()::text, 'TP53', 'TP53 基因', '["多種癌症"]'::jsonb, '["reproductive","lungs"]'::jsonb, 3.0, 5),
(gen_random_uuid()::text, 'HFE', 'HFE 基因', '["血色素沉著症"]'::jsonb, '["liver"]'::jsonb, 2.0, 6),
(gen_random_uuid()::text, 'MTHFR', 'MTHFR 基因', '["血栓","葉酸代謝異常"]'::jsonb, '["heart"]'::jsonb, 1.5, 7),
(gen_random_uuid()::text, 'ALDH2', 'ALDH2 基因', '["酒精代謝異常","食道癌"]'::jsonb, '["liver"]'::jsonb, 1.8, 8)
ON CONFLICT (marker_code) DO NOTHING;