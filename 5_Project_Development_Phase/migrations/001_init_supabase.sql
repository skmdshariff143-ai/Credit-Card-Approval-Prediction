-- Migration: Initial Supabase Postgres Schema Setup
-- Translated from SQLite schema definitions to be fully compatible with PostgreSQL.

-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    full_name VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'User',
    created_at VARCHAR(100) NOT NULL DEFAULT TO_CHAR(CURRENT_TIMESTAMP AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI:SS'),
    last_login VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    is_admin INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- 2. Create Prediction History Table
CREATE TABLE IF NOT EXISTS prediction_history (
    id SERIAL PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL UNIQUE,
    timestamp VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    income DOUBLE PRECISION NOT NULL,
    employment VARCHAR(100) NOT NULL,
    experience DOUBLE PRECISION NOT NULL,
    children INTEGER NOT NULL,
    debt DOUBLE PRECISION NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    probability DOUBLE PRECISION NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    model VARCHAR(100) NOT NULL,
    recommendation TEXT NOT NULL,
    raw_input TEXT,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    explanation TEXT
);

CREATE INDEX IF NOT EXISTS idx_pred_hist_app_id ON prediction_history(application_id);
CREATE INDEX IF NOT EXISTS idx_pred_hist_timestamp ON prediction_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_pred_hist_income ON prediction_history(income);
CREATE INDEX IF NOT EXISTS idx_pred_hist_risk ON prediction_history(risk_level);

-- 3. Create Predictions Table (Compatibility layer)
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    timestamp VARCHAR(100) NOT NULL,
    input_features TEXT NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    probability DOUBLE PRECISION NOT NULL,
    model VARCHAR(100),
    explanation TEXT
);

-- 4. Create Reports Table
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    application_id VARCHAR(50) NOT NULL UNIQUE REFERENCES prediction_history(application_id) ON DELETE CASCADE,
    timestamp VARCHAR(100) NOT NULL,
    inputs TEXT NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    model_used VARCHAR(100) NOT NULL,
    explanation TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_reports_app_id ON reports(application_id);
