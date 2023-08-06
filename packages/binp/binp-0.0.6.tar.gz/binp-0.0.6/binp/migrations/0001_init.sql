CREATE TABLE journal
(
    id          INTEGER   NOT NULL PRIMARY KEY AUTOINCREMENT,
    operation   TEXT      NOT NULL,
    description TEXT      NOT NULL,
    started_at  TIMESTAMP NOT NULL DEFAULT current_timestamp,
    error       TEXT,
    duration    DOUBLE PRECISION,
    finished_at TIMESTAMPTZ
);

CREATE TABLE record
(
    id         INTEGER   NOT NULL PRIMARY KEY AUTOINCREMENT,
    journal_id BIGINT    NOT NULL REFERENCES journal (id),
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    message    TEXT      NOT NULL
);


CREATE TABLE record_field
(
    record_id BIGINT NOT NULL REFERENCES record (id),
    name      TEXT   NOT NULL,
    value     TEXT,
    PRIMARY KEY (record_id, name)
);

CREATE TABLE kv
(
    namespace TEXT NOT NULL,
    key       TEXT NOT NULL,
    value     TEXT,
    PRIMARY KEY (namespace, key)
);

CREATE INDEX record_journal_idx ON record (journal_id);
CREATE INDEX record_field_record_idx ON record_field (record_id);