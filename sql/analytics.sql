-- Job Market Analytics Queries

-- 1. Jobs per company
SELECT 
    c.company_name,
    COUNT(j.job_id) AS job_count
FROM companies c
LEFT JOIN jobs j ON c.company_id = j.company_id
GROUP BY c.company_id, c.company_name
ORDER BY job_count DESC;

-- 2. Jobs per location
SELECT 
    l.location_name,
    COUNT(j.job_id) AS job_count
FROM locations l
LEFT JOIN jobs j ON l.location_id = j.location_id
GROUP BY l.location_id, l.location_name
ORDER BY job_count DESC;

-- 3. Top hiring companies
SELECT 
    c.company_name,
    COUNT(j.job_id) AS total_jobs
FROM companies c
INNER JOIN jobs j ON c.company_id = j.company_id
GROUP BY c.company_id, c.company_name
ORDER BY total_jobs DESC
LIMIT 10;

-- 4. Jobs by company and location
SELECT 
    c.company_name,
    l.location_name,
    COUNT(j.job_id) AS job_count
FROM jobs j
INNER JOIN companies c ON j.company_id = c.company_id
LEFT JOIN locations l ON j.location_id = l.location_id
GROUP BY c.company_id, l.location_id
ORDER BY c.company_name, job_count DESC;

-- 5. Jobs with full details (denormalized view)
SELECT 
    j.job_id,
    j.job_title,
    c.company_name,
    l.location_name,
    j.description
FROM jobs j
INNER JOIN companies c ON j.company_id = c.company_id
LEFT JOIN locations l ON j.location_id = l.location_id
ORDER BY c.company_name, j.job_title;
