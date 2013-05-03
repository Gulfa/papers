CREATE TABLE papers(
       id INTEGER NOT NULL PRIMARY KEY,
       title TEXT(300),
       authors TEXT(300),
       inspires_id INTERGER,
       arxiv_id TEXT(20),
       summary TEXT(1000),
       bibtex TEXT(3000),
       UNIQUE(title)
);
CREATE TABLE keywords(
       id INTEGER NOT NULL,
       keyword TEXT(100),
       paper_id INTEGER NOT NULL,
       PRIMARY KEY(id)
);