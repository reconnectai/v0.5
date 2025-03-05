-- Reconnect.ai v0.5 Schema (Non-RAG)
-- Members, Personae, Artifacts tables for Postgres

CREATE TABLE members (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    subscription_status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE personae (
    id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE artifacts (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL,
    content TEXT,                    -- Extracted text (v0.5), NULL for non-text later
    link VARCHAR(255),               -- File path (e.g., "/files/123.txt")
    type VARCHAR(20) DEFAULT 'text', -- text, pdf, docx, audio, video
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (persona_id) REFERENCES personae(id) ON DELETE CASCADE
);

CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_personae_member_id ON personae(member_id);
CREATE INDEX idx_artifacts_persona_id ON artifacts(persona_id);

-- Sample Data
INSERT INTO members (id, email, role, subscription_status)
VALUES (1, 'test@reconnect.ai', 'premium', 'active');

INSERT INTO personae (member_id, name)
VALUES (1, 'Grandpa Joe');

INSERT INTO artifacts (persona_id, content, link, type)
VALUES (1, 'I love telling war stories.', '/files/grandpa_story.txt', 'text');