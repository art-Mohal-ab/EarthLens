# TODO: Configure Flask App for PostgreSQL on Render

## Steps to Complete

1. **Update server/app/config.py** ✅
   - Modified `ProductionConfig.SQLALCHEMY_DATABASE_URI` to read from `DATABASE_URL` environment variable without a hardcoded fallback.

2. **Update server/.env** ✅
   - Set `DATABASE_URL` to the provided PostgreSQL connection string: `postgresql://earthlens_user:WXXEok6HdaeluZdzOpOrGKmenCTUK3Uw@dpg-d41dii75r7bs739d32gg-a.oregon-postgres.render.com/earthlens`

3. **Run Migrations on Render Database**
   - Set `FLASK_ENV=production`
   - Run `flask db migrate` to generate new migration if needed
   - Run `flask db upgrade` to apply migrations to the remote database

4. **Test Connection and Basic Operations**
   - Verify the app connects to the PostgreSQL database
   - Test basic CRUD operations to ensure tables are created and accessible
