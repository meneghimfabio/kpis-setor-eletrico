# Diretrizes de Contribuição 🤝

Agradecemos o interesse em contribuir com o **Painel do Setor Elétrico Brasileiro & Data Lakehouse ANEEL**!

---

## 🧭 Como Contribuir

1. **Faça um Fork do Projeto**:
   Acesse `https://github.com/meneghimfabio/kpis-setor-eletrico` e clique em **Fork**.

2. **Crie uma Branch Temática**:
   ```bash
   git checkout -b feature/minha-nova-funcionalidade
   # ou para correções
   git checkout -b fix/ajuste-tarifa-aneel
   ```

3. **Padronização de Código**:
   - **Backend (Python)**:
     - Utilize type hints em todas as funções e modelos Pydantic.
     - Siga a PEP 8.
     - Valide as tipagens com `flake8` ou `black` se aplicável.
   - **Frontend (TypeScript / React)**:
     - Siga convenções de componentes funcionais React com TypeScript estrito.
     - Não utilize imports não utilizados (`noUnusedLocals`).
     - Execute `npm run build` na pasta `frontend/` antes de comitar para garantir que não há erros de tipagem.
   - **Pipelines (SQLX / Airflow)**:
     - Mantenha queries SQL idempotentes (`MERGE` ou `CREATE OR REPLACE`).
     - Inclua testes/assertions de qualidade no Dataform (`nonNull`, `uniqueKey`).

4. **Commits Semânticos**:
   - `feat:` Nova funcionalidade (ex: nova tabela Gold ou componente no dashboard).
   - `fix:` Correção de bug regulatório ou de interface.
   - `docs:` Atualizações na documentação.
   - `refactor:` Refatoração de código sem alteração comportamental.
   - `perf:` Otimizações de performance (ex: queries BigQuery BI Engine).

5. **Envie um Pull Request**:
   Abra o PR descrevendo claramente a alteração realizada, impactos nos datasets ou na API e evidências de testes locais.
