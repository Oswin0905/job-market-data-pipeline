-- Job Market Data Pipeline Schema

CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS locations (
    location_id INTEGER PRIMARY KEY,
    location_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY,
    job_title TEXT NOT NULL,
    company_id INTEGER NOT NULL,
    location_id INTEGER,
    description TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_jobs_company_id ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_location_id ON jobs(location_id);
CREATE INDEX IF NOT EXISTS idx_jobs_title ON jobs(job_title);
