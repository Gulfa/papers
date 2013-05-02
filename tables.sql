CREATE TABLE papers(
       id INTEGER NOT NULL,
       title TEXT(300),
       authors TEXT(300),
       spires_id INTERGER,
       arxiv_id TEXT(20),
       summary TEXT(1000),
       bibtex TEXT(3000),
       PRIMARY KEY (id),
       UNIQUE(title)
);
CREATE TABLE keywords(
       id INTEGER NOT NULL,
       keyword TEXT(100),
       paper_id INTEGER NOT NULL,
       PRIMARY KEY(id)
);